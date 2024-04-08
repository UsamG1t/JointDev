import cmd
import sys
import time

class scripter(cmd.Cmd):
    def precmd(self, line):
        time.sleep(1)
        return super().precmd(line)

    def do_EOF(self, args):
        return 1
    def emptyline(self):
        pass

    def do_bless(self, arg):
        print("Be blessed,", arg)

    def do_sendto(self, arg):
        print("G0 to", arg)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as file:
            scr = scripter(stdin=file)
            scr.prompt = ''
            scr.use_rawinput = False
            scr.cmdloop()
    else:
        scr = scripter()
        scr.cmdloop()