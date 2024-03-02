import cowsay

class Player:
    def __init__(self):
        self.x = self.y = 0

def encounter(x, y):
    name, message = monsters[y*10 + x]
    print(cowsay.cowsay(message, cow=name))


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
            if  len(args) != 4 \
                    or not isinstance(args[0], str) \
                    or not args[1].isdigit() \
                    or not args[2].isdigit() \
                    or not isinstance(args[3], str):
                print('Invalid arguments')
                
            else:
                args[1] = int(args[1])
                args[2] = int(args[2])
                print(f'Added monster {args[0]} to ({args[1]}, {args[2]}) saying {args[3]}')
                if monsters.setdefault(args[2] * 10 + args[1], None) != None:
                    print("Replaced the old monster")

                monsters[args[2]*10 + args[1]] = [args[0], args[3]]

        case _:
            print("Invalid command")
