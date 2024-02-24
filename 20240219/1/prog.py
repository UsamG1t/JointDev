import sys
import glob
import zlib
import os

if len(sys.argv) == 2:
    for heads in glob.iglob(sys.argv[1] + '/.git/refs/heads'):
        with os.scandir(heads) as dr:
            for item in dr:
                print(item.name)
