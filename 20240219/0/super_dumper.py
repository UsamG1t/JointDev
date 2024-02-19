import sys, zlib, glob

for name in glob.iglob(sys.argv[1] + "/??/*"):
    with open(name, "rb") as f:
        bulk = zlib.decompress(f.read())

    kindsize, _, content = bulk.partition(b'\x00')
    kind, size = kindsize.decode().split()

    match kind:
        case "commit":
            print("\tCommit:")
            print(content.decode().rstrip())
        case "tree":
            while content:
                namesize, _, content = content.partition(b'\x00')
                content = content[20:]
                print(namesize.decode())
        case _:
            print("\tother", kind)
            print(content)