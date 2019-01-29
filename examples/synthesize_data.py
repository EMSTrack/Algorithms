#!/Users/vectflux/Documents/EMSTrack/Algorithms/venv/bin/python
from geopy.distance import distance
import random

lat1 = 32.4008
lat2 = 32.5534
lon1 = -117.1233
lon2 = -116.777

bases = 10
demands = 12

# assume kilometer per second is at 60 MPH
kmps = 0.0268224

def new_point():
    return random.uniform(lat1, lat2), random.uniform(lon1, lon2)

base_locations = [new_point() for _ in range(bases)]
demand_locations =[new_point() for _ in range(demands)]

dists = [[distance(b, d).km for d in demand_locations] for b in base_locations]
# print (dists)


times = list(map(lambda b: list(map(lambda dist: str(int(dist/kmps)), b)) , dists))
# print()
# print(times)

baseline = "'id','name','type','vics',"
bases_string = ["{}{},{}\n".format(baseline, b[0], b[1]) for b in base_locations]
demands_string = ["{},{}\n".format(d[0], d[1]) for d in demand_locations]

times_string = [",".join(b) + "\n" for b in times]

# print(times_string)



with open('bases.csv', 'w') as file:
    file.writelines(bases_string)

with open('demand_points.csv', 'w') as file:
    file.writelines(demands_string)

with open('times.csv', 'w') as file:
    file.writelines(times_string)