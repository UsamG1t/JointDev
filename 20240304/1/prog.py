import cowsay

class Player:
    def __init__(self):
        self.x = self.y = 0

class Game:

    def __init__(self):
        # self.field = [[' ' for i in range(10)] for j in range(10)]
        self.monsters = {}
        self.player  = Player()

    def encounter(self, x, y):
        name, message = self.monsters[y*10 + x]
        print(cowsay.cowsay(message, cow=name))

    def Play(self):

        while inp := input().split():
            match inp:
                case ['up' | 'down' | 'left' | 'right']:
                    self.player .y = (self.player .y + 10 - (inp[0] == 'up')) % 10
                    self.player .y = (self.player .y + 10 + (inp[0] == 'down')) % 10
                    self.player .x = (self.player .x + 10 - (inp[0] == 'left')) % 10
                    self.player .x = (self.player .x + 10 + (inp[0] == 'right')) % 10
                    print(f'Moved to ({self.player .x}, {self.player .y})')

                    if self.monsters.setdefault(self.player .y*10 + self.player .x, None) != None:
                        self.encounter(self.player .x, self.player .y)

                case ['addmon', *args]:
                    if  len(args) != 4 \
                            or not isinstance(args[0], str) \
                            or not args[1].isdigit() \
                            or not args[2].isdigit() \
                            or not isinstance(args[3], str):
                        print('Invalid arguments')
                    elif args[0] not in cowsay.list_cows():
                        print('Cannot add unknown monster')
                    else:
                        args[1] = int(args[1])
                        args[2] = int(args[2])
                        print(f'Added monster {args[0]} to ({args[1]}, {args[2]}) saying {args[3]}')
                        if self.monsters.setdefault(args[2] * 10 + args[1], None) != None:
                            print("Replaced the old monster")

                        self.monsters[args[2]*10 + args[1]] = [args[0], args[3]]

                case _:
                    print("Invalid command")


Game().Play()