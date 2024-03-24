import sys
import cmd
import io
import socket
import shlex
import cowsay

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


class  MUDcmd(cmd.Cmd):

    def __init__(self, socket):
        # self.game = Game()
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
        # self.game.move('up', args)
        self.socket.sendall(f'move up'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        move_answer(*response)
    
    def do_down(self, args):
        'one step DOWN on field'
        # self.game.move('down', args)
        self.socket.sendall(f'move down'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        move_answer(*response)
    
    def do_left(self, args):
        'one step LEFT on field'
        # self.game.move('left', args)
        self.socket.sendall(f'move left'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        move_answer(*response)
    
    def do_right(self, args):
        'one step RIGHT on field'
        # self.game.move('right', args)
        self.socket.sendall(f'move right'.encode())
        response = self.socket.recv(1024).rstrip().decode()
        response = shlex.split(response)
        move_answer(*response)
    
    # def do_addmon(self, args):
    #     '''
    #     Add monster on the position

    #     first argument is a name of monster from [cowsay.list_cows() | 'jgsbat']

    #     Other required args (their order is not important):
        
    #     1. coord <int[0...field_size)> <int[0...field_size)>
    #     2. hp <int[0...inf)>
    #     3. hello <string (with quotation for more than one word)>
    #     '''
    #     self.game.addmon(args)

    # def do_attack(self, args):
    #     'Attack the monster in current position'

    #     self.game.attack(args)

    # def complete_attack(self, text, line, begidx, endidx):
    #     words = (line[:endidx] + ".").split()
    #     DICT = []
    #     match len(words):
    #         case 2:
    #             DICT = cowsay.list_cows() + ['jgsbat']
    #         case 4:
    #             if words[2].startswith('with'):
    #                 DICT = self.game.player.weapons.keys()
    #     return [c for c in DICT if c.startswith(text)]




if __name__ == '__main__':
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        MUDcmd(s).cmdloop()
    
    # while msg := sys.stdin.buffer.readline():
    #     s.sendall(msg)
    #     print(s.recv(1024).rstrip().decode())