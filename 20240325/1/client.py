import sys
import cmd
import io
import socket
import shlex
import cowsay

addmon_errors = {
    '1' : 'Invalid arguments (count of elements)',
    '2' : 'Invalid arguments (type of name)', 
    '3' : 'Cannot add unknown monster', 
    '4' : 'Invalid arguments (type of message)', 
    '5' : 'Invalid arguments (type of hp)', 
    '6' : 'Invalid arguments (value of hp)', 
    '7' : 'Invalid arguments (type of coord x', 
    '8' : 'Invalid arguments (value of coord x)', 
    '9' : 'Invalid arguments (type of coord y', 
    '10': 'Invalid arguments (value of coord y)'
}

weapons = {
'sword': 10,
'spear': 15,
'axe'  : 20
}

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


def move_answer(x, y, name=None, message=None):
    print(f'Moved to ({x}, {y})')

    if name:
        if name == 'jgsbat':
            print(cowsay.cowsay(message, cowfile=custom_monster))
        else:
            print(cowsay.cowsay(message, cow=name))

def addmon_answer(code, name = None, x = None, y = None, msg = None, replace_check=None):
    if code != '0':
        print(addmon_errors[code])
        return

    print(f'Added monster {name} to ({x}, {y}) saying {msg}')
    if replace_check:
        print(replace_check)

def attack_answer(name, code, dmg = None, hp = None):
    if code == '1':
        print(f'No {name} here')
        return

    print(f'Attacked {name}, damage {dmg} hp')

    if hp != '0':
        print(f'{name} now has {hp}')
    else:
        print(f'{name} died')


class  MUDcmd(cmd.Cmd):

    def __init__(self, socket):
        self.field_size = 10
        self.socket = socket
        print("<<< Welcome to Python-MUD 0.1 >>>")
        return super().__init__()

    prompt = ">> "

    def do_EOF(self, args):
        'Stops game by ^D combination'
        return 1
    def emptyline(self):
        'auto-repeat of last command OFF'
        return
    
    def do_up(self, args):
        'one step UP on field'
        
        self.socket.sendall(f'move up\n'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        move_answer(*response)
    
    def do_down(self, args):
        'one step DOWN on field'
        
        self.socket.sendall(f'move down\n'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        move_answer(*response)
    
    def do_left(self, args):
        'one step LEFT on field'
        
        self.socket.sendall(f'move left\n'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        move_answer(*response)
    
    def do_right(self, args):
        'one step RIGHT on field'
        
        self.socket.sendall(f'move right\n'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        move_answer(*response)
    
    def do_addmon(self, args):
        '''
        Add monster on the position

        first argument is a name of monster from [cowsay.list_cows() | 'jgsbat']

        Other required args (their order is not important):
        
        1. coord <int[0...field_size)> <int[0...field_size)>
        2. hp <int[0...inf)>
        3. hello <string (with quotation for more than one word)>
        '''
        
        args = shlex.split(args)
        broken = False

        if len(args) != 8:
            broken = True
            print('client: Invalid arguments (count of elements)')

        elif not isinstance(args[0], str):
            broken = True
            print('client: Invalid arguments (type of name)')

        elif args[0] not in cowsay.list_cows() \
                and args[0] != 'jgsbat':
            broken = True
            print('client: Cannot add unknown monster')

        else:
            monster = {"name": args[0]}

            for i in range(1, len(args)):
                match args[i]:
                    case 'hello':
                        if not isinstance(args[i+1], str):
                            broken = True
                            print('client: Invalid arguments (type of message)')
                            break
                        monster["message"] = args[i+1]
                    case 'hp':
                        if not args[i+1].isdigit():
                            broken = True
                            print('client: Invalid arguments (type of hp)')
                            break
                        if int(args[i+1]) <= 0:
                            broken = True
                            print('client: Invalid arguments (value of hp)')
                            break
                        monster["hp"] = int(args[i+1])
                    case 'coord':
                        if not args[i+1].isdigit():
                            broken = True
                            print('client: Invalid arguments (type of coord x')
                            break
                        if int(args[i+1]) < 0 \
                                or int(args[i+1]) >= self.field_size:
                            broken = True
                            print('client: Invalid arguments (value of coord x)')
                            break
                        if not args[i+2].isdigit():
                            broken = True
                            print('client: Invalid arguments (type of coord y')
                            break
                        if int(args[i+2]) < 0 \
                                or int(args[i+2]) >= self.field_size:
                            broken = True
                            print('client: Invalid arguments (value of coord y)')
                            break
                        m_x = int(args[i+1])
                        m_y = int(args[i+2])
                    case _: continue
        if not broken:
            self.socket.sendall(f'addmon {monster["name"]} hp {monster["hp"]} coord {m_x} {m_y} hello "{monster["message"]}"\n'.encode())
            response = self.socket.recv(1024).rstrip().decode()
            response = shlex.split(response)
            addmon_answer(*response)


    def do_attack(self, args):
        'Attack the monster in current position'

        weapon = None
        args = shlex.split(args)
        
        match args:
            case [name, 'with', weapon_type]:
                if weapon_type not in weapons.keys():
                    print('client: Unknown weapon')
                else:
                    weapon = {'type'  : weapon_type,
                              'damage': weapons[weapon_type]}
            case [name]:
                weapon = {'type'  : 'sword',
                          'damage': weapons['sword']}
            case _:
                print('client: Invalid command')

        if weapon:
            self.socket.sendall(f'attack {args[0]} {weapon["damage"]}\n'.encode())
            response = self.socket.recv(1024).rstrip().decode()
            response = shlex.split(response)
            attack_answer(args[0], *response)


    def complete_attack(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        DICT = []
        match len(words):
            case 2:
                DICT = cowsay.list_cows() + ['jgsbat']
            case 4:
                if words[2].startswith('with'):
                    DICT = weapons.keys()
        return [c for c in DICT if c.startswith(text)]




if __name__ == '__main__':
    # host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    # port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    host = "localhost"
    port = 1337
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(f'register {sys.argv[1]}\n'.encode())
        response = s.recv(1024).rstrip().decode()
        if response[0] == '0':
            print(response[2:])
            MUDcmd(s).cmdloop()
        else:
            print(response)