import os

commands = [
    'time pyreverse -o jpg -p ems_analysis ems.algorithms.analysis',
    'mv classes_ems_analysis.jpg uml/',
    'mv packages_ems_analysis.jpg uml/',

    'time pyreverse -o jpg -p ems_selection ems.algorithms.selection ',
    'mv classes_ems_selection.jpg uml/',
    'mv packages_ems_selection.jpg uml/',

    'time pyreverse -o jpg -p ems_data ems.data ',
    'mv classes_ems_data.jpg uml/',
    'mv packages_ems_data.jpg uml/',

    'time pyreverse -o jpg -p ems_models ems.models ',
    'mv classes_ems_models.jpg uml/',
    'mv packages_ems_models.jpg uml/',

    'time pyreverse -o jpg -p ems_simulators ems.simulators ',
    'mv classes_ems_simulators.jpg uml/',
    'mv packages_ems_simulators.jpg uml/',

    'time pyreverse -o jpg -p ems ems ',
    'mv classes_ems.jpg uml/',
    'mv packages_ems.jpg uml/',


    # 'ls -l',

    # 'git add ems',
    # 'git add *.jpg'

]

# print("There are {} pyreverse processes, make sure they finish.".format(len(commands)))

for command in commands:
    print(command)
    # call (command.split(' '))
    os.system(command)
    print()
