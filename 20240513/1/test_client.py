import unittest
from unittest.mock import MagicMock
import shlex
import cowsay
import threading
import time

from mood.server import Monster
from mood.client import MUDcmd
from mood.common import steps, addmon_errors, custom_monster

res = []

class MyMock(MagicMock):
    def key(self, position):
        return position[1] * self.field_size + position[0]

    def move(self, direction):
        response = []
        
        self.pos[0] = (self.pos[0] + self.field_size +
                  steps[direction]['x']) % self.field_size
        self.pos[1] = (self.pos[1] + self.field_size +
                  steps[direction]['y']) % self.field_size
        
        response.append(f'Moved to ({self.pos[0]}, {self.pos[1]})')

        key = self.key(self.pos)
        if self.monsters.setdefault(key, None) is not None:
            result = self.monsters[key].encounter()
            if result[0] == 'jgsbat':
                response.append(cowsay.cowsay(result[1], cowfile=custom_monster))
            else:
                response.append(cowsay.cowsay(result[1], cow=result[0]))
        else:
            del self.monsters[key]

        return '\n'.join(response)

    def addmon(self, args):
        response = []
        monster = {}
        args = shlex.split(args)

        if len(args) != 8:
            return addmon_errors['1']

        elif not isinstance(args[0], str): # name
            return addmon_errors['2']
        elif args[0] not in cowsay.list_cows() \
                and args[0] != 'jgsbat':
            print('~3~')
            return addmon_errors['3']

        elif not args[2].isdigit(): # hp
            return addmon_errors['5']
        elif int(args[2]) <= 0:
            return addmon_errors['6'] 
        
        elif not args[4].isdigit(): # x
            return addmon_errors['7']
        elif int(args[4]) < 0 \
                or int(args[4]) >= self.field_size:
            return addmon_errors['8']
        
        elif not args[5].isdigit(): # y
            return addmon_errors['9']
        elif int(args[5]) < 0 \
                or int(args[4]) >= self.field_size:
            return addmon_errors['10']
        
        elif not isinstance(args[7], str): # message
            return addmon_errors['4']
        
        response.append(f'Added monster {args[0]} with {args[2]} hp')

        key = self.key((int(args[4]), int(args[5])))
        if self.monsters.setdefault(key, None) is not None:
            del self.monsters[key]
            response.append("Replaced the old monster")

        self.monsters[key] = Monster(
            args[0],
            int(args[2]),
            args[7])

        return '\n'.join(response)

    def attack(self, args):
        response = []
        key = self.key(self.pos)
        args = shlex.split(args)

        if self.monsters.setdefault(key, None) is None \
                or self.monsters[key].name != args[0]:
            
            return f'No {args[0]} here'

        name, dmg, hp = self.monsters[key].damage(int(args[1]))
        
        response.append(f'Attacked {name}, damage {dmg} hp')

        if hp == 0:
            response.append(f'{name} died')
            del self.monsters[key]
        else:
            response.append(f'{name} now has {hp} hp')

        return '\n'.join(response)

    def sendall(self, s):
        global res
        match shlex.split(s.decode()):
            case ['addmon', *args]:
                res.append(self.addmon(shlex.join(args)))
            case ['move', direction]:
                res.append(self.move(direction))
            case ['attack', *args]:
                res.append(self.attack(shlex.join(args)))
            case _:
                pass

         
class TestClient(unittest.TestCase):

    def setUp(self):
        self.mocker = MyMock()

    def test_mocker_moving(self):
        global res
        self.mocker = MyMock()
        self.mocker.pos = [0, 0]
        self.mocker.field_size = 10
        self.mocker.monsters = {}

        with open("test_mocker_moving.mood") as file:
            scr = MUDcmd(self.mocker, stdin=file)
            scr.prompt = ''
            scr.use_rawinput = False
            scr.cmdloop()

        self.assertEqual(len(res), 4)
        self.assertEqual(res, ['Moved to (0, 9)', 'Moved to (0, 0)', 'Moved to (9, 0)', 'Moved to (0, 0)'])
        res = []

    def test_mocker_addmon(self):
        global res
        self.mocker = MyMock()
        self.mocker.pos = [0, 0]
        self.mocker.field_size = 10
        self.mocker.monsters = {}
        
        with open("test_mocker_addmon.mood") as file:
            scr = MUDcmd(self.mocker, stdin=file)
            scr.prompt = ''
            scr.use_rawinput = False
            scr.cmdloop()
        
        self.assertEqual(len(res), 4)
        self.assertEqual(res,
            [
                'Added monster default with 19 hp',
                '''Added monster default with 19 hp
Replaced the old monster''',
                'Moved to (0, 1)',
                '''Moved to (0, 0)
 ___ 
< U >
 --- 
        \\   ^__^
         \\  (oo)\\_______
            (__)\\       )\\/\\
                ||----w |
                ||     ||'''
            ])
        res = []

    def test_mocker_attack(self):
        global res
        self.mocker = MyMock()
        self.mocker.pos = [0, 0]
        self.mocker.field_size = 10
        self.mocker.monsters = {}

        with open("test_mocker_attack.mood") as file:
            scr = MUDcmd(self.mocker, stdin=file)
            scr.prompt = ''
            scr.use_rawinput = False
            scr.cmdloop()
        
        self.assertEqual(len(res), 4)
        self.assertEqual(res,
            [
                'Added monster default with 19 hp',
                '''Attacked default, damage 15 hp
default now has 4 hp''',
                '''Attacked default, damage 4 hp
default died''',
                'No default here'
            ])
        res = []
