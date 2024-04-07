import cowsay
import io


addmon_errors = {
    '1' : 'Invalid arguments (count of elements)',
    '2' : 'Invalid arguments (type of name)',
    '3' : 'Cannot add unknown monster',
    '4' : 'Invalid arguments (type of message)',
    '5' : 'Invalid arguments (type of hp)',
    '6' : 'Invalid arguments (value of hp)',
    '7' : 'Invalid arguments (type of coord x',
    '8' : 'Invalid arguments (value of coord x)',
    '9' : 'Invalid arguments (type of coord y',
    '10': 'Invalid arguments (value of coord y)'
}

steps = {
    'up'   : {'x': 0, 'y':-1},
    'down' : {'x': 0, 'y': 1},
    'left' : {'x':-1, 'y': 0},
    'right': {'x': 1, 'y': 0}
}

weapons = {
    'sword': 10,
    'spear': 15,
    'axe'  : 20
}

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
