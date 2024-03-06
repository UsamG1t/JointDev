import cowsay
import io

custom_monster = cowsay.read_dot_cow(io.StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
"""))

class Player:
    def __init__(self):
        self.x = self.y = 0

class Game:

    def __init__(self):
        # self.field = [[' ' for i in range(self.field_size)] for j in range(self.field_size)]
        self.field_size = 10
        self.monsters = {}
        self.player  = Player()

    def key(self, a, b):
        return b * self.field_size + a

    def encounter(self, x, y):
        monster = self.monsters[self.key(x, y)]
        if monster['name'] == 'jgsbat':
            print(cowsay.cowsay(monster["message"], cowfile=custom_monster))
        else:
            print(cowsay.cowsay(monster["message"], cow=monster["name"]))

    def Play(self):

        while inp := input().split():
            match inp:
                case ['up' | 'down' | 'left' | 'right']:
                    self.player.y = (self.player.y + self.field_size \
                                     - (inp[0] == 'up') + (inp[0] == 'down')) \
                                     % self.field_size
                    self.player.x = (self.player.x + self.field_size \
                                     - (inp[0] == 'left') + (inp[0] == 'right')) \
                                     % self.field_size
                    
                    print(f'Moved to ({self.player .x}, {self.player .y})')

                    if self.monsters.setdefault(self.key(self.player.x, self.player.y), None) != None:
                        self.encounter(self.player.x, self.player.y)

                case ['addmon', *args]:
                    if  len(args) != 4 \
                            or not isinstance(args[0], str) \
                            or not args[1].isdigit() \
                            or not args[2].isdigit() \
                            or not isinstance(args[3], str):
                        print('Invalid arguments')
                    elif args[0] not in cowsay.list_cows() \
                            and args[0] != 'jgsbat':
                        print('Cannot add unknown monster')
                    else:
                        args[1] = int(args[1])
                        args[2] = int(args[2])
                        print(f'Added monster {args[0]} to ({args[1]}, {args[2]}) saying {args[3]}')
                        if self.monsters.setdefault(self.key(args[1], args[2]), None) != None:
                            print("Replaced the old monster")

                        self.monsters[self.key(args[1], args[2])] = {"name": args[0], "message": args[3]}

                case _:
                    print("Invalid command")


Game().Play()