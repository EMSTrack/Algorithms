from os import system

bases = 1500
demands = 120
cpus = 7


comms = \
[
    'python3 examples/synthesize_data {} {} {} '.format(bases, demands, cpus ),
    'python3 run.py configurations/experiment.yaml ',
    'open results/*.csv '
]

for c in comms:
    system(c)