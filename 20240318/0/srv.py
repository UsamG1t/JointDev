import socket
import sys
import multiprocessing

def serve(conn, addr):
    with conn:
      print('Connected by', addr)
      while data := conn.recv(1024):
            conn.sendall(data.swapcase())

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    while True:
        conn, addr = s.accept()
        multiprocessing.Process(target=serve, args=(conn, addr)).start()