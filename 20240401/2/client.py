import cmd
import shlex

import cowsay
import io

import readline
import threading
import sys
import socket

def msg_sendreciever(client, socket):
    while response := socket.recv(1024).rstrip().decode():
        print(f"\n{response}\n{client.prompt}{readline.get_line_buffer()}", end="", flush=True)


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
        
    def do_down(self, args):
        'one step DOWN on field'
        
        self.socket.sendall(f'move down\n'.encode())
        
    def do_left(self, args):
        'one step LEFT on field'
        
        self.socket.sendall(f'move left\n'.encode())
        
    def do_right(self, args):
        'one step RIGHT on field'
        
        self.socket.sendall(f'move right\n'.encode())
        
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

    def do_sayall(self, args):
        self.socket.sendall(f'sayall {args}\n'.encode())


if __name__ == '__main__':
    host = "localhost" if len(sys.argv) < 3 else sys.argv[2]
    port = 1337 if len(sys.argv) < 4 else int(sys.argv[3])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(f'register {sys.argv[1]}\n'.encode())
        response = s.recv(1024).rstrip().decode()
        if response[0] == '0':
            print(response[2:])
            cli = MUDcmd(s)
            request = threading.Thread(target = msg_sendreciever, args = (cli, cli.socket))
            request.start()
            cli.cmdloop()
        else:
            print(response)