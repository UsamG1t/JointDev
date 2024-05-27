import threading
import socket
import sys

from . import MUDcmd, msg_sendreciever

def client():
    if sys.argv[1] == '--file':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 1337))

        with open(sys.argv[2]) as file:
            scr = MUDcmd(s, stdin=file)
            scr.prompt = ''
            scr.use_rawinput = False
            scr.cmdloop()
    else:
        host = "localhost" if len(sys.argv) < 3 else sys.argv[2]
        port = 1337 if len(sys.argv) < 4 else int(sys.argv[3])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(f'register {sys.argv[1]}\n'.encode())
            response = s.recv(1024).rstrip().decode()
            if response[0] == '0':
                print(response[2:])
                cli = MUDcmd(s)
                request = threading.Thread(target=msg_sendreciever, args=(cli, cli.socket))
                request.start()
                cli.cmdloop()
            else:
                print(response)

if __name__ == "__main__":
    client()
