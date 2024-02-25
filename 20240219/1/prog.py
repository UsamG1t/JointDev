import sys
import glob
import zlib
import os

def tree_parsing(commit_tree):
    with open(sys.argv[1] + '/.git/objects/' + 
              commit_tree[0:2] + '/' + commit_tree[2:], 'rb') as tree:
        tree_data = zlib.decompress(tree.read()).partition(b'\00')[2]
    
    while tree_data:
        item_name = tree_data.partition(b'\00')[0].split(b' ')[-1].decode()
        item_id = tree_data.partition(b'\00')[2][:20].hex()
        
        with open(sys.argv[1] + '/.git/objects/' + 
                  item_id[0:2] + '/' + item_id[2:], 'rb') as item:
            item_type = zlib.decompress(item.read()).partition(b' ')[0].decode()

        tree_data = tree_data.partition(b'\00')[2][20:]
        print(f'{item_type} {item_id}\t{item_name}')
    

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
