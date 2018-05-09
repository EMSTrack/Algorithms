from subprocess import call

commands = [
	'pyreverse -o jpg -p ems_algorithms ems.algorithms',
	'pyreverse -o jpg -p ems_data ems.data',
	'pyreverse -o jpg -p ems_models ems.models',
	'pyreverse -o jpg -p ems_simulators ems.simulators',

	'ls -l',

	# 'git add ems',
	'git add *.jpg'

]

for command in commands:

	print (command)
	call (command.split(' '))
	print()
