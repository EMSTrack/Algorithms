from os import system
from pprint import PrettyPrinter
pprint = PrettyPrinter(indent=2).pprint
from multiprocessing import Pool

# bases = 12000
# demands = 1500
# cpus = 8

path = "configurations/experiment/"

case_intensity = [
	'low-freq',
	'med-freq',
	'very-freq',
]

policies = [
	'least-disruption',
]

parallel_processes = []

for intensity in case_intensity:
	first = '/usr/local/bin/python3 run.py {}{}-best-travel-times.yaml'.format(path, intensity)
	others = []
	for policy in policies:
		others.append('/usr/local/bin/python3 run.py  {}{}-{}.yaml'.format(path, intensity, policy))

	parallel_processes.append(first + " ".join(others))

pprint(parallel_processes)
print(len(parallel_processes))

for command in parallel_processes: 
	subprocess.Popen(command)

# for policy in policies:
	# system('python3.7 run.py  {}{}-best-travel-times.yaml'.format(path, case_intensity))



# Run all the best travel times first

# Run the following sims next.

# best = '"Experimenting with Original Dibene Setup - Best Travel Times"'
# least = '"Experimenting with Original Dibene Setup - Least Disruption"'

# names = " ".join(names)

# comms = \
# [
#     # 'python3.7 examples/synthesize_data.py {} {} {} '.format(bases, demands, cpus ),

#     'python3.7 run.py configurations/experiment-best-travel.yaml ',
#     'python3.7 analysis/graph_traveltimes.py {} &'.format(best),
#     'python3.7 analysis/graph_coverage.py {} &'.format(best),

#     'python3.7 run.py configurations/experiment-least-disruption.yaml ',
#     'python3.7 analysis/graph_traveltimes.py {} &'.format(least),
#     'python3.7 analysis/graph_coverage.py {} &'.format(least)
# ]


