import cowsay
import shlex
import cmd

import socket
import sys
import multiprocessing

import asyncio

Users = {}

class Player:
    steps = {
    'up'   : {'x': 0, 'y':-1},
    'down' : {'x': 0, 'y': 1},
    'left' : {'x':-1, 'y': 0},
    'right': {'x': 1, 'y': 0}
    }

    weapons = {
    'sword': 10,
    'spear': 15,
    'axe'  : 20
    }

    def __init__(self):
        self.x = self.y = 0
        self.field_size = 10

    def position(self):
        return (self.x, self.y)

    def move(self, method, args):
        self.x = (self.x + self.field_size
                 + self.steps[method]['x']) % self.field_size
        self.y = (self.y + self.field_size
                 + self.steps[method]['y']) % self.field_size

        return self.position()

class Monster:
    def __init__(self, name, hp, message):
        self.name = name
        self.hp = hp
        self.message = message
    
    def encounter(self):
        return (self.name, self.message)

    def damage(self, damage):
        dmg = min([self.hp, damage])
        self.hp = self.hp - dmg

        return (self.name, dmg, self.hp)

class Game:

    def __init__(self):
        self.field_size = 10
        self.monsters = {} # key(x, y) -> Monster()
        
    def key(self, position):
        return position[1] * self.field_size + position[0]
    
    def move(self, player, method, args):
        response = []
        print("LOG: ", 'move', method, args)

        position = player.move(method, args)

        response.append(str(position[0]))
        response.append(str(position[1]))

        key = self.key(position)
        if self.monsters.setdefault(key, None) != None:
            result = self.monsters[key].encounter()
            response.append(result[0])
            response.append(result[1])

        print("LOG: response", response)
        return response

    def addmon(self, args):
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
                        if not isinstance(args[i+1], str):
                            broken = True
                            response.append('4')
                            break
                        monster["message"] = args[i+1]
                    case 'hp':
                        if not args[i+1].isdigit():
                            broken = True
                            response.append('5')
                            break
                        if int(args[i+1]) <= 0:
                            broken = True
                            response.append('6')
                            break
                        monster["hp"] = int(args[i+1])
                    case 'coord':
                        if not args[i+1].isdigit():
                            broken = True
                            response.append('7')
                            break
                        if int(args[i+1]) < 0 \
                                or int(args[i+1]) >= self.field_size:
                            broken = True
                            response.append('8')
                            break
                        if not args[i+2].isdigit():
                            broken = True
                            response.append('9')
                            break
                        if int(args[i+2]) < 0 \
                                or int(args[i+2]) >= self.field_size:
                            broken = True
                            response.append('10')
                            break
                        m_x = int(args[i+1])
                        m_y = int(args[i+2])
                    case _: continue

        if not broken:
            response.append('0')
            response.append(monster["name"])
            response.append(str(m_x))
            response.append(str(m_y))
            response.append(monster["message"])
            
            key = self.key((m_x, m_y))
            if self.monsters.setdefault(key, None) != None:
                del self.monsters[key]
                response.append("Replaced the old monster")

            self.monsters[key] = Monster(monster['name'], monster['hp'], monster['message'])

        print("LOG: response", response)
        return response

    def attack(self, player, args):
        response = []
        position = player.position()
        key = self.key(position)
        args = shlex.split(args)
        print("LOG: ", 'attack', args)

        if self.monsters.setdefault(key, None) == None \
        or self.monsters[key].name != args[0]:
            response.append('1')
            return response
        print("LOG: ", 'attack | after exist_check')

        name, dmg, hp = self.monsters[key].damage(int(args[1]))
        response.append('0')
        response.append(str(dmg))
        response.append(str(hp))
        
        if not hp:
            del self.monsters[key]

        print("LOG: response", response)
        return response

# def handler(conn, addr):
#     with conn:
#         print("LOG: ", 'Connected by', addr)
#         game = Game()
#         while data := conn.recv(1024).decode():
#             cmd, *args = shlex.split(data)
#             print("LOG: ", addr, data)
#             print("LOG: ", args)
#             match cmd:
#                 case 'move':
#                     method, *args = args
#                     response = game.move(method, shlex.join(args))
#                     conn.sendall(shlex.join(response).encode())
#                 case 'addmon':
#                     response = game.addmon(shlex.join(args))
#                     conn.sendall(shlex.join(response).encode())
#                 case 'attack':
#                     response = game.attack(shlex.join(args))
#                     conn.sendall(shlex.join(response).encode())
#         print("LOG: client has left")
        
# host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
# port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((host, port))
#     s.listen()
#     conn, addr = s.accept()
#     multiprocessing.Process(target=handler, args=(conn, addr)).start()
#     print("LOG: Server stop listening for new connections")

#     # while True:
#     #     conn, addr = s.accept()
#     #     multiprocessing.Process(target=handler, args=(conn, addr)).start()

# # ______________________________________________

MUD_GAME = Game()
users = dict()

async def handler(reader, writer):
    client = writer.get_extra_info("peername")
    print(f'New Client on {client}')
    my_id = None
    my_player = None
    my_queue = asyncio.Queue()
    my_cmd = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(my_queue.get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([my_cmd, receive], return_when=asyncio.FIRST_COMPLETED)

        for request in done:
            if request is my_cmd:
                my_cmd = asyncio.create_task(reader.readline())
                print(f'{client}: {request.result()}')
                cmd, *args = shlex.split(request.result().decode())
                print("LOG: ", client, request.result().decode())
                print("LOG: ", args)
                match cmd:
                    case 'register':
                        if args[0] in users.keys():
                            writer.write('LoginError: Exists user with this id\n'.encode())
                            done = None
                            break

                        writer.write(f'0:You are logged in with  id {args[0]}\n'.encode())
                        my_id = args[0]
                        my_player = Player()
                        users[my_id] = my_queue
                        print(f"{client} logs in as {my_id}\n")

                    case 'move':
                        method, *args = args
                        response = MUD_GAME.move(my_player, method, shlex.join(args))
                        writer.write(shlex.join(response).encode())
                    case 'addmon':
                        response = MUD_GAME.addmon(shlex.join(args))
                        writer.write(shlex.join(response).encode())
                    case 'attack':
                        response = MUD_GAME.attack(my_player, shlex.join(args))
                        writer.write(shlex.join(response).encode())
                    
                    # case ['yield', msg]:
                    #     if not my_id:
                    #         writer.write('NoAccessError: You are non-authorized client, please log in\n'.encode())
                    #         break
                        
                    #     for user in users.values():
                    #         if user is not my_queue:
                    #             await user.put(f'{cowsay.cowsay(msg, cow=my_id)}')                    
                    
                    # case ['quit']:
                    #     if not my_id:
                    #         writer.write('NoAccessError: You are non-authorized client, please log in\n'.encode())
                    #         break

                    #     client = writer.get_extra_info("peername")
                    #     print(f"{client} logs out from {my_id}\n")
                    #     del users[my_id]
                    #     my_id = None
                    
                    case _:
                        continue
                    

            if request is receive:
                receive = asyncio.create_task(my_queue.get())
                writer.write(f"{request.result()}\n".encode())
                await writer.drain()

    my_cmd.cancel()
    receive.cancel()
    if my_id:
        del users[my_id]
    writer.close()
    await writer.wait_closed()
    print(f'{client} left')

async def main():
    print('Start working')
    server = await asyncio.start_server(handler, '0.0.0.0', 1337)
    print('activate server')
    async with server:
        print('Server Forever')
        await server.serve_forever()

asyncio.run(main())