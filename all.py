from os import system

bases = 12000
demands = 1500
cpus = 8

best = '"Experimenting with Original Dibene Setup - Best Travel Times"'
least = '"Experimenting with Original Dibene Setup - Least Disruption"'

# names = " ".join(names)

comms = \
[
    # 'python3.7 examples/synthesize_data.py {} {} {} '.format(bases, demands, cpus ),

    'python3.7 run.py configurations/experiment-best-travel.yaml ',
    'python3.7 analysis/graph_traveltimes.py {} &'.format(best),
    'python3.7 analysis/graph_coverage.py {} &'.format(best),

    'python3.7 run.py configurations/experiment-least-disruption.yaml ',
    'python3.7 analysis/graph_traveltimes.py {} &'.format(least),
    'python3.7 analysis/graph_coverage.py {} &'.format(least)
]

for c in comms:
    print(c)
    system(c)