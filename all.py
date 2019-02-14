from os import system

bases = 12000
demands = 1500
cpus = 8


comms = \
[
    'python3.7 examples/synthesize_data.py {} {} {} '.format(bases, demands, cpus ),
    'python3.7 run.py configurations/experiment.yaml ',
    'open results/metrics.csv results/initial_coverage.txt '
]

for c in comms:
    print(c)
    system(c)