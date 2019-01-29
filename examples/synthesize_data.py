#!/Users/vectflux/Documents/EMSTrack/Algorithms/venv/bin/python
from geopy.distance import distance
import random
from multiprocessing import Process
from multiprocessing import cpu_count

lat1 = 32.4008
lat2 = 32.5534
lon1 = -117.1233
lon2 = -116.777

bases = 100
demands = 100

# assume kilometer per second is at 60 MPH
kmps = 0.0268224

cpus = cpu_count()

bases = int(bases/cpus)


def new_point():
    return random.uniform(lat1, lat2), random.uniform(lon1, lon2)

print('demands')
demand_locations =[new_point() for _ in range(demands)]



def generate_base_and_times(demand_locs, base_locs_arr, distances_arr, i):
    print("bases")
    for _ in range(bases):
        base_locs_arr[i].append(new_point())
        print(base_locs_arr[i])
    # base_locations = [new_point() for _ in range(bases)]

    print('dists')
    temp_dists = [[distance(base2, demand2).km for demand2 in demand_locs] for base2 in base_locs_arr[i]]

    for dist in temp_dists:
        distances_arr[i].append(dist)



base_locations_array = [[] for _ in range(cpus)]
dists_array = [[] for _ in range(cpus)]



processes = []
for i in range(cpus):
    processes.append(Process(target=generate_base_and_times, args=(demand_locations,
                                                                   base_locations_array,
                                                                   dists_array,
                                                                   i)))
for i in range(cpus):
    processes[i].start()

for i in range(cpus):
    processes[i].join()

from IPython import embed; embed()
base_locations = []
for b in base_locations_array:
    base_locations += b

dists = []
for d in dists_array:
    dists += d

# from IPython import embed; embed()

print('times')
times = list(map(lambda b: list(map(lambda dist: str(int(dist/kmps)), b)) , dists))
# print()
# print(times)


print('strings')
baseline = "'id','name','type','vics',"
bases_string = ["{}{},{}\n".format(baseline, b[0], b[1]) for b in base_locations]
demands_string = ["{},{}\n".format(d[0], d[1]) for d in demand_locations]

times_string = [",".join(b) + "\n" for b in times]

# print(times_string)

print('write to file')

with open('bases.csv', 'w') as file:
    file.writelines(bases_string)

with open('demand_points.csv', 'w') as file:
    file.writelines(demands_string)

with open('times.csv', 'w') as file:
    file.writelines(times_string)