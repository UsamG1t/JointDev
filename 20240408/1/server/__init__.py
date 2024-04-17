'''Main logic of server program'''
import cowsay
import shlex
import asyncio
import random
from copy import copy

from common import *


def move_answer(x, y, name=None, message=None):
    '''Preprocessing of move response.'''
    response = []
    response.append(f'Moved to ({x}, {y})')

    if name:
        if name == 'jgsbat':
            response.append(cowsay.cowsay(message, cowfile=custom_monster))
        else:
            response.append(cowsay.cowsay(message, cow=name))

    return '\n'.join(response)


def encounter_answer(name, message):
    '''Preprocessing of encounter response.'''
    if name == 'jgsbat':
        return cowsay.cowsay(message, cowfile=custom_monster)
    return cowsay.cowsay(message, cow=name)


def addmon_answer(code, name=None, hp=None, replace_check=None):
    '''Preprocessing of addmon response.'''
    response = []

    if code != '0':
        response.append(addmon_errors[code])
        return '\n'.join(response)

    response.append(f'Added monster {name} with {hp} hp')
    if replace_check:
        response.append(replace_check)

    return '\n'.join(response)


def attack_answer(name, code, dmg=None, hp=None):
    '''Preprocessing of attack response.'''
    response = []

    if code == '1':
        response.append(f'No {name} here')
        return '\n'.join(response)

    response.append(f'Attacked {name}, damage {dmg} hp')

    if hp != '0':
        response.append(f'{name} now has {hp}')
    else:
        response.append(f'{name} died')

    return '\n'.join(response)


class Player:
    '''Main actions of Player.'''

    def __init__(self):
        '''Creating base data for player.'''
        self.x = self.y = 0
        self.field_size = 10

    def position(self):
        '''return coordinates of player.'''
        return (self.x, self.y)

    def move(self, method, args):
        '''do one step with direction.'''
        self.x = (self.x + self.field_size +
                  steps[method]['x']) % self.field_size
        self.y = (self.y + self.field_size +
                  steps[method]['y']) % self.field_size

        return self.position()


class Monster:
    '''Main actions of Player.'''

    def __init__(self, name, hp, message):
        '''Creating base data for monster.'''
        self.name = name
        self.hp = hp
        self.message = message

    def encounter(self):
        '''return response for \"move_answer\".'''
        return (self.name, self.message)

    def damage(self, damage):
        '''return response for \"attack_answer\".'''
        dmg = min([self.hp, damage])
        self.hp = self.hp - dmg

        return (self.name, dmg, self.hp)


class Game:
    '''Main game logic.'''

    def __init__(self):
        '''Creating base data for game.'''
        self.field_size = 10
        self.monsters = {}  # key(x, y) -> Monster()

    def key(self, position):
        '''Taking a key for monsters` map.'''
        return position[1] * self.field_size + position[0]

    def move(self, player, method, args):
        '''Processing of move request from client.'''
        response = []
        print("LOG: ", 'move', method, args)

        position = player.move(method, args)

        response.append(str(position[0]))
        response.append(str(position[1]))

        key = self.key(position)
        if self.monsters.setdefault(key, None) is not None:
            result = self.monsters[key].encounter()
            response.append(result[0])
            response.append(result[1])
        else:
            del self.monsters[key]

        print("LOG: response", response)
        return response

    def addmon(self, args):
        '''Processing of addmon request from client.'''
        response = []
        broken = False
        monster = {}
        args = shlex.split(args)

        print("LOG: ", 'addmon', args)

        if len(args) != 8:
            broken = True
            response.append('1')

        elif not isinstance(args[0], str):
            broken = True
            response.append('2')

        elif args[0] not in cowsay.list_cows() \
                and args[0] != 'jgsbat':
            broken = True
            response.append('3')
        else:
            monster = {"name": args[0]}

            for i in range(1, len(args)):
                match args[i]:
                    case 'hello':
                        if not isinstance(args[i + 1], str):
                            broken = True
                            response.append('4')
                            break
                        monster["message"] = args[i + 1]
                    case 'hp':
                        if not args[i + 1].isdigit():
                            broken = True
                            response.append('5')
                            break
                        if int(args[i + 1]) <= 0:
                            broken = True
                            response.append('6')
                            break
                        monster["hp"] = int(args[i + 1])
                    case 'coord':
                        if not args[i + 1].isdigit():
                            broken = True
                            response.append('7')
                            break
                        if int(args[i + 1]) < 0 \
                                or int(args[i + 1]) >= self.field_size:
                            broken = True
                            response.append('8')
                            break
                        if not args[i + 2].isdigit():
                            broken = True
                            response.append('9')
                            break
                        if int(args[i + 2]) < 0 \
                                or int(args[i + 2]) >= self.field_size:
                            broken = True
                            response.append('10')
                            break
                        m_x = int(args[i + 1])
                        m_y = int(args[i + 2])
                    case _: continue

        if not broken:
            response.append('0')
            response.append(monster["name"])
            response.append(monster["hp"])
            key = self.key((m_x, m_y))
            if self.monsters.setdefault(key, None) is not None:
                del self.monsters[key]
                response.append("Replaced the old monster")

            self.monsters[key] = Monster(
                monster['name'],
                monster['hp'],
                monster['message'])

        print("LOG: response", response)
        return response

    def attack(self, player, args):
        '''Processing of attack request from client.'''
        response = []
        position = player.position()
        key = self.key(position)
        args = shlex.split(args)
        print("LOG: ", 'attack', args)

        if self.monsters.setdefault(key, None) is None \
                or self.monsters[key].name != args[0]:
            response.append(str(args[0]))
            response.append('1')
            return response

        name, dmg, hp = self.monsters[key].damage(int(args[1]))
        response.append(str(name))
        response.append('0')
        response.append(str(dmg))
        response.append(str(hp))

        if not hp:
            del self.monsters[key]

        print("LOG: response", response)
        return response


MUD_GAME = Game()
users = dict()
users_info = dict()


async def handler(reader, writer):
    '''Main async-handler logic.'''
    client = writer.get_extra_info("peername")
    print(f'New Client on {client}')
    my_id = None
    my_player = None
    my_queue = asyncio.Queue()
    my_cmd = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(my_queue.get())

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [my_cmd, receive],
            return_when=asyncio.FIRST_COMPLETED)

        for request in done:
            if request is my_cmd:
                my_cmd = asyncio.create_task(reader.readline())
                print(f'{client}: {request.result()}')
                if (not request.result()):
                    break

                cmd, *args = shlex.split(request.result().decode())
                print("LOG: ", client, request.result().decode())
                print("LOG: ", args)
                answer = ""
                match cmd:
                    case 'register':
                        if args[0] in users.keys():
                            writer.write(
                                'LoginError: Exists user with this id\n'
                                .encode())
                            done = None
                            break

                        writer.write(
                            f'0:You are logged in with  id {args[0]}\n'
                            .encode())
                        my_id = args[0]
                        my_player = Player()
                        users_info[my_id] = my_player
                        users[my_id] = my_queue
                        print(f"{client} logs in as {my_id}\n")

                        for user in users.values():
                            if user is not my_queue:
                                await user.put(f'{my_id} join the MUD')

                    case 'move':
                        method, *args = args
                        response = MUD_GAME.move(my_player, method, shlex.join(args))
                        answer = move_answer(*response)
                    case 'addmon':
                        response = MUD_GAME.addmon(shlex.join(args))
                        answer = addmon_answer(*response)

                        for user in users.values():
                            if user is not my_queue:
                                await user.put(f'{my_id} {answer}')
                    case 'attack':
                        response = MUD_GAME.attack(my_player, shlex.join(args))
                        answer = attack_answer(*response)

                        for user in users.values():
                            if user is not my_queue:
                                await user.put(f'{my_id} {answer}')
                    case 'sayall':
                        args = ' '.join(args)
                        for user in users.values():
                            if user is not my_queue:
                                await user.put(f'{my_id}: {args}')
                    case _:
                        continue
                writer.write(answer.encode())

            if request is receive:
                receive = asyncio.create_task(my_queue.get())
                writer.write(f"{request.result()}\n".encode())
                await writer.drain()

    for user in users.values():
        if user is not my_queue:
            await user.put(f'{my_id} left the MUD')

    my_cmd.cancel()
    receive.cancel()
    if my_id:
        del users[my_id]
    writer.close()
    await writer.wait_closed()
    print(f'{client} left')


async def move_monsters():
    while True:
        print("New Loop")
        if 0 < len(MUD_GAME.monsters) < MUD_GAME.field_size**2:
            print("Try")
            found = False
            while not found:
                key_before = random.choice(list(MUD_GAME.monsters.keys()))
                direction = random.choice(list(steps.keys()))
                pos = [MUD_GAME.field_size, MUD_GAME.field_size]
                pos[0] += key_before % MUD_GAME.field_size
                pos[1] += key_before // MUD_GAME.field_size

                pos[0] = (pos[0] + (direction == 'right') -
                                   (direction == 'left')) % MUD_GAME.field_size
                pos[1] = (pos[1] + (direction == 'down') -
                                   (direction == 'up')) % MUD_GAME.field_size
                key_after = MUD_GAME.key(pos)

                print(MUD_GAME.monsters)
                if MUD_GAME.monsters.setdefault(key_after, None) is None:
                    print(MUD_GAME.monsters)
                    MUD_GAME.monsters[key_after] = copy(MUD_GAME.monsters[key_before])
                    del MUD_GAME.monsters[key_before]
                    found = True

                    for user, queue in users.items():
                        await queue.put(
                            '{} moved one cell {}\n'.format(
                                MUD_GAME.monsters[key_after].name,
                                direction
                            )
                        )
                        print(users_info[user].position(), pos)
                        if users_info[user].position() == tuple(pos):
                            await queue.put(
                                encounter_answer(
                                    MUD_GAME.monsters[key_after].name,
                                    MUD_GAME.monsters[key_after].message
                                )
                            )
        print("Waiting")
        await asyncio.sleep(30)


async def main():
    '''Main async-server logic.'''
    print('Start working')
    server = await asyncio.start_server(handler, '0.0.0.0', 1337)
    print('activate server')
    move_operator = asyncio.create_task(move_monsters())
    await asyncio.sleep(0)
    async with server:
        print('Server Forever')
        await server.serve_forever()
