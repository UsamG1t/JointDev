import sys
import socket
import threading
import readline

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])


def rsv(socket, ):
    while mesag := socket.recv(1024).rstrip().decode():
        print(f"\n{mesag}\n{readline.get_line_buffer()}", end="", flush=True)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    timer = threading.Thread(target=rsv, args=(s,)).start()
    while msg := sys.stdin.buffer.readline():
        s.sendall(msg)
