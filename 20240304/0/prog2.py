import shlex

fio = input()
place = input()

print(shlex.join(['register', fio, place]))