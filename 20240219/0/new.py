import sys, zlib

with open(sys.argv[1], "rb") as f:
    content = f.read()
    dcr = zlib.decompress(content)

print(dcr)
