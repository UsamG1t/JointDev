import cowsay

class Player:
    def __init__(self):
        self.x = self.y = 0

def encounter(x, y):
    print(cowsay.cowsay(monsters[y*10 + x]))


field = [[' ' for i in range(10)] for j in range(10)]
monsters = {}
player = Player()

while inp := input().split():
    match inp:
        case ['up' | 'down' | 'left' | 'right']:
            player.y = (player.y + 10 - (inp[0] == 'up')) % 10
            player.y = (player.y + 10 + (inp[0] == 'down')) % 10
            player.x = (player.x + 10 - (inp[0] == 'left')) % 10
            player.x = (player.x + 10 + (inp[0] == 'right')) % 10
            print(f'Moved to ({player.x}, {player.y})')

            if monsters.setdefault(player.y*10 + player.x, None) != None:
                encounter(player.x, player.y)

        case ['addmon', *args]:
            if  len(args) != 3 \
                    or not args[0].isdigit() \
                    or not args[1].isdigit() \
                    or not isinstance(args[2], str):
                print('Invalid arguments3')
                break
            
            args[0] = int(args[0])
            args[1] = int(args[1])
            print(f'Added monster to ({args[0]}, {args[1]}) saying {args[2]}')
            if monsters.setdefault(args[1] * 10 + args[0], None) != None:
                print("Replaced the old monster")

            monsters[args[1]*10 + args[0]] = args[2]

        case _:
            print("Invalid command")
