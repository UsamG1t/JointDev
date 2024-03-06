import cowsay
import shlex
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

        print("<<< Welcome to Python-MUD 0.1 >>>")
        
        while inp := shlex.split(input()):
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
                    broken = False

                    if len(args) != 8:
                        broken = True
                        print('Invalid arguments')

                    elif not isinstance(args[0], str):
                        broken = True
                        print('Invalid arguments')

                    elif args[0] not in cowsay.list_cows() \
                            and args[0] != 'jgsbat':
                        broken = True
                        print('Cannot add unknown monster')
                    else:
                        monster = {"name": args[0]}

                        for i in range(1, len(args)):
                            match args[i]:
                                case 'hello':
                                    if not isinstance(args[i+1], str):
                                        broken = True
                                        print('Invalid arguments')
                                        break
                                    monster["message"] = args[i+1]
                                case 'hp':
                                    if  not args[i+1].isdigit() \
                                            or int(args[i+1]) <= 0:
                                        broken = True
                                        print('Invalid arguments')
                                        break
                                    monster["hp"] = int(args[i+1])
                                case 'coord':
                                    if  not args[i+1].isdigit() \
                                            or int(args[i+1]) < 0 \
                                            or not args[i+2].isdigit() \
                                            or int(args[i+2]) < 0:
                                        broken = True
                                        print('Invalid arguments')
                                        break
                                    m_x = int(args[i+1])
                                    m_y = int(args[i+2])
                                case _: continue

                    if not broken:
                        print(f'Added monster {monster["name"]} to ({m_x}, {m_y}) saying {monster["message"]}')
                        if self.monsters.setdefault(self.key(m_x, m_y), None) != None:
                            print("Replaced the old monster")

                        self.monsters[self.key(m_x, m_y)] = monster

                case _:
                    print("Invalid command")


Game().Play()