import sys
import glob
import zlib
import os

if len(sys.argv) == 2:
    for heads in glob.iglob(sys.argv[1] + '/.git/refs/heads'):
        with os.scandir(heads) as dr:
            for item in dr:
                print(item.name)
elif len(sys.argv) == 3:
    with open(sys.argv[1] + '/.git/refs/heads/' + sys.argv[2], 'r') as branch:
        last_commit = branch.read()[:-1]
    
    with open(sys.argv[1] + '/.git/objects/' + 
              last_commit[0:2] + '/' + last_commit[2:], 'rb') as commit:
        commit_data = zlib.decompress(commit.read()).partition(b'\00')[2].split(b'\n')
    print(commit_data[0].decode())
    print(commit_data[1].decode())
    print(*commit_data[2].decode().split(' ')[:-2])
    print(*commit_data[3].decode().split(' ')[:-2])
    