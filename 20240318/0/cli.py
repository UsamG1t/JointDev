import sys
import socket
import cmd


class clicmd(cmd.Cmd):

    def __init__(self, socket):
        self.s = socket
        return super().__init__()

    prompt = ">> "

    def do_EOF(self, args):
        return 1

    def emptyline(self):
        pass

    def do_print(self, args):
        self.s.sendall(("print " + args).encode())
        print(self.s.recv(1024).rstrip().decode())

    def do_info(self, args):
        self.s.sendall(("info " + args).encode())
        print(self.s.recv(1024).rstrip().decode())

    def complete_info(self, text, line, begidx, endidx):
        words = (line[:endidx] + '.').split()

        if len(words) == 2:
            return [c for c in ["host", "port"] if c.startswith(text)]
    

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    clicmd(s).cmdloop()