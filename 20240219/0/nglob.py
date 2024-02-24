import glob
import zlib
import sys

for item in glob.glob(sys.argv[1] + "/??/*"):
    with open(item, "rb") as f:
        print(zlib.decompress(f.read()), '\n\n')
        
