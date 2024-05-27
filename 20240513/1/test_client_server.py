import unittest
import socket
import multiprocessing
import time

from mood.server import start
from mood.client import MUDcmd


class TestRoot(unittest.TestCase):

    def test_creating_monster(self):
        proc = multiprocessing.Process(target=start, args=(1234,))
        proc.start()
        time.sleep(1)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 1234))
            tst = MUDcmd(s)
            tst.prompt = ''
            tst.do_register("test_creating_monster")
            response = s.recv(1024).rstrip().decode()

            tst.do_addmon("milk coord 0 0 hp 19 hello U")
            expected_response = 'Added monster milk with 19 hp'
            self.assertEqual(s.recv(1024).rstrip().decode(), expected_response)

        proc.terminate()

    def test_move_to_monster(self):
        proc = multiprocessing.Process(target=start, args=(1235,))
        proc.start()
        time.sleep(1)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 1235))
            tst = MUDcmd(s)
            tst.prompt = ''
            tst.do_register("test_move_to_monster")
            response = s.recv(1024).rstrip().decode()
            tst.do_addmon("default coord 1 0 hp 19 hello u")
            response = s.recv(1024).rstrip().decode()

            tst.do_right('')
            expected_response = '''Moved to (1, 0)
 ___ 
< u >
 --- 
        \   ^__^
         \  (oo)\_______
            (__)\       )\\/\\
                ||----w |
                ||     ||'''
            self.assertEqual(s.recv(1024).rstrip().decode(), expected_response)

        proc.terminate()

    def test_attack_monster(self):
        proc = multiprocessing.Process(target=start, args=(11111,))
        proc.start()
        time.sleep(1)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 11111))
            tst = MUDcmd(s)
            tst.prompt = ''
            tst.do_register("test_attack_monster")
            response = s.recv(1024).rstrip().decode()
            tst.do_addmon("milk coord 0 0 hp 19 hello U")
            response = s.recv(1024).rstrip().decode()

            tst.do_attack("milk with spear")
            expected_response = '''Attacked milk, damage 4 hp
milk now has 4'''
            self.assertEqual(s.recv(1024).rstrip().decode(), expected_response)

        proc.terminate()