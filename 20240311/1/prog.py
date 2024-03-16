import cowsay
import shlex
import io
import cmd

custom_monster = cowsay.read_dot_cow(io.StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
"""))

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
        if self.name == 'jgsbat':
            print(cowsay.cowsay(self.message, cowfile=custom_monster))
        else:
            print(cowsay.cowsay(self.message, cow=self.name))

    def damage(self, damage):
        dmg = min([self.hp, damage])
        self.hp = self.hp - dmg

        return (self.name, dmg, self.hp)

class Game:

    def __init__(self):
        self.field_size = 10
        self.monsters = {} # key(x, y) -> Monster()
        self.player  = Player()
        
    def key(self, position):
        return position[1] * self.field_size + position[0]
    
    def move(self, method, args):
        position = self.player.move(method, args)

        print(f'Moved to ({position[0]}, {position[1]})')

        key = self.key(position)
        if self.monsters.setdefault(key, None) != None:
            self.monsters[key].encounter()


    def addmon(self, args):
        broken = False
        monster = {}

        args = shlex.split(args)

        if len(args) != 8:
            broken = True
            print('Invalid arguments (count of elements)')

        elif not isinstance(args[0], str):
            broken = True
            print('Invalid arguments (type of name)')

        elif args[0] not in cowsay.list_cows() \
                and args[0] != 'jgsbat':
            broken = True
            print('Cannot add unknown monster')
        else:
            monster = {"name": args[0]}

            for i in range(1, len(args)):
                match args[i]:
                    case 'hello':
                        if not isinstance(args[i+1], str):
                            broken = True
                            print('Invalid arguments (type of message)')
                            break
                        monster["message"] = args[i+1]
                    case 'hp':
                        if not args[i+1].isdigit():
                            broken = True
                            print('Invalid arguments (type of hp)')
                            break
                        if int(args[i+1]) <= 0:
                            broken = True
                            print('Invalid arguments (value of hp)')
                            break
                        monster["hp"] = int(args[i+1])
                    case 'coord':
                        if not args[i+1].isdigit():
                            broken = True
                            print('Invalid arguments (type of coord x')
                            break
                        if int(args[i+1]) < 0 \
                                or int(args[i+1]) >= self.field_size:
                            broken = True
                            print('Invalid arguments (value of coord x)')
                            break
                        if not args[i+2].isdigit():
                            broken = True
                            print('Invalid arguments (type of coord y')
                            break
                        if int(args[i+2]) < 0 \
                                or int(args[i+2]) >= self.field_size:
                            broken = True
                            print('Invalid arguments (value of coord y)')
                            break
                        m_x = int(args[i+1])
                        m_y = int(args[i+2])
                    case _: continue

        if not broken:
            print(f'Added monster {monster["name"]} to ({m_x}, {m_y}) saying {monster["message"]}')
            
            key = self.key((m_x, m_y))
            if self.monsters.setdefault(key, None) != None:
                del self.monsters[key]
                print("Replaced the old monster")

            self.monsters[key] = Monster(monster['name'], monster['hp'], monster['message'])

    def attack(self, args):
        position = self.player.position()
        key = self.key(position)
	weapon = None
        args = shlex.split(args)
        
	if self.monsters.setdefault(key, None) == None \
        or self.monsters[key].name != args[0]:
            print(f'No {args[0]} here')
            return

        match args:
            case [name, 'with', weapon_type]:
                if weapon_type not in self.player.weapons.keys():
                    print('Unknown weapon')
                else:
                    weapon = {'type'  : weapon_type,
                              'damage': self.player.weapons[weapon_type]}
            case [name]:
                weapon = {'type'  : 'sword',
                          'damage': self.player.weapons['sword']}
            case _:
                print('Invalid command')

        if not weapon:
            return

        name, dmg, hp = self.monsters[key].damage(weapon['damage'])
        print(f'Attacked {name},  damage {dmg} hp')
        
        if hp:
            print(f'{name} now has {hp}')
        else:
            print(f'{name} died')
            del self.monsters[key]



class MUDcmd(cmd.Cmd):

    def __init__(self):
        self.game = Game()
        print("<<< Welcome to Python-MUD 0.1 >>>")
        return super().__init__()

    prompt = ">> "

    def do_EOF(self, args):
        'Stops game by ^D combination'
        return 1
    def emptyline(self):
        'auto-repeat of last commend OFF'
        return
    
    def do_up(self, args):
        'one step UP on field'
        self.game.move('up', args)
    def do_down(self, args):
        'one step DOWN on field'
        self.game.move('down', args)
    def do_left(self, args):
        'one step LEFT on field'
        self.game.move('left', args)
    def do_right(self, args):
        'one step RIGHT on field'
        self.game.move('right', args)
    
    def do_addmon(self, args):
        '''
        Add monster on the position

        first argument is a name of monster from [cowsay.list_cows() | 'jgsbat']

        Other required args (their order is not important):
        
        1. coord <int[0...field_size)> <int[0...field_size)>
        2. hp <int[0...inf)>
        3. hello <string (with quotation for more than one word)>
        '''
        self.game.addmon(args)

    def do_attack(self, args):
        'Attack the monster in current position'

        self.game.attack(args)

    def complete_attack(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        DICT = []
        match len(words):
            case 2:
                DICT = cowsay.list_cows() + ['jgsbat']
            case 4:
                if words[2].startswith('with'):
                    DICT = self.game.player.weapons.keys()
        return [c for c in DICT if c.startswith(text)]

if __name__ == '__main__':
    MUDcmd().cmdloop()
