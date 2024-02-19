import glob
import zlib
import sys

for item in list(glob.iglob(sys.argv[1] + "/??/*")):
    with open(item, "rb") as f:
        print(zlib.decompress(f.read()))    