import os

commands = [
    'time pyreverse -o jpg -p ems_algorithms ems.algorithms &',
    'time pyreverse -o jpg -p ems_data ems.data &',
    'time pyreverse -o jpg -p ems_models ems.models &',
    'time pyreverse -o jpg -p ems_simulators ems.simulators &',
    'time pyreverse -o jpg -p ems ems &',

    # 'ls -l',

    # 'git add ems',
    # 'git add *.jpg'

]

for command in commands:
    print(command)
    # call (command.split(' '))
    os.system(command)
    print()
