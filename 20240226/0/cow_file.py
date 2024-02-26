import cowsay
import sys
if sys.argv[1] in cowsay.list_cows():
    print(cowsay.cowsay(sys.argv[2], cow = sys.argv[1]))
else:
    with open(f'./{sys.argv[1]}.cow') as f:
        print(cowsay.cowsay(sys.argv[2], cowfile = cowsay.read_dot_cow(f)))