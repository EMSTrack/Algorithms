
from geopy.distance import distance
import random
from multiprocessing import cpu_count
from multiprocessing import Pool
from functools import reduce
from timeit import default_timer as timer
from datetime import timedelta
import sys

multicpu = True

# Coordinate range for Tijuana, Mexico
# lat1 = 32.4008
# lat2 = 32.5534
# lon1 = -117.1233
# lon2 = -116.777

lat1 = 32.823033
lon1 = -117.167672
lat2 = 32.710484
lon2 = -117.017637

try:
    bases_num   = int(sys.argv[1])
    demands_num = int(sys.argv[2])
    cpu = int(sys.argv[3])
    if cpu > cpu_count(): raise Exception()

except:
    raise Exception("\n\nRequired Arguments: \n" 
                    "1) Number of potential bases\n" 
                    "2) Number of demand points.\n" 
                    "3) Number of CPUs on the job. Maximum: {}\n".format(cpu_count())
                    )


# assume kilometer per second is at 60 MPH
kmps = 0.0268224


# Functions that generate new points, and new lists of points , and the times between
# the points.
# Outputs a pair of doubles as a coordinate point.
def new_point():
    return (random.uniform(lat1, lat2), random.uniform(lon1, lon2))

# Returns a size num list of new points
def generate_points(num):
    return [new_point() for _ in range(num)]

# Map all possible bases to all destinations, resulting in a list of list of times as
# ints.
def generate_times(bases):
    global demand_locations

    unit =  len(bases)
    percentages = [r for r in range(100, 0, -10)]

    dists = []
    i = 0

    start_time = timer()
    for base in bases:
        dist = [distance(base, dest).km for dest in demand_locations]
        dists.append(dist)

        percent_done = i / unit * 100
        if percent_done >= percentages[-1]:

            time_progress = timer()
            elapsed_time = time_progress - start_time
            remaining_time = elapsed_time * (100.0 - percent_done)/percent_done

            print(percentages.pop(), "%. ", "{}/{} bases. ".format(i, unit),
                  "Elapsed: {}.  Remains: {}.  Total: {}.".format(
                    str(timedelta(seconds=elapsed_time)),
                    str(timedelta(seconds=remaining_time)),
                    str(timedelta(seconds=(elapsed_time + remaining_time)))
            ))

        i += 1

    # dists = [[distance(base, dest).km for dest in demand_locations] for base in bases]
    times = [[str(int(dist//kmps)) for dist in base_list] for base_list in dists]

    return times

# Flatten a list of lists to a list.
def flatten(l_of_l):
    return reduce(lambda l1, l2: l1 + l2, l_of_l)


def main():

    global demand_locations, bases_num

    start_time = timer()

    demand_locations =      generate_points(demands_num)
    base_locations =        generate_points(bases_num)

    if not multicpu:
        base_locations =    generate_points(bases_num)
        times =             generate_times(base_locations)

    else: # TODO still a problem here with off by ones.
        list_base_locations = [base_locations[ int(i * len(base_locations)/cpu):
                                              int((i + 1)* len(base_locations)/cpu)]
                               for i in range(cpu)]

        with Pool(cpu) as p:
            list_of_times = p.map(generate_times, list_base_locations)

        times =             flatten(list_of_times)
        base_locations =    flatten(list_base_locations)

    bases_string =  ["latitude,longitude\n"] + ["{},{}\n".format(b[0], b[1]) for b in base_locations]
    demands_string = ["latitude,longitude\n"] + ["{},{}\n".format(d[0], d[1]) for d in demand_locations]
    times_string = [",".join(b) + "\n" for b in times]


    print("Write to files.")

    if len(bases_string) != 1 + len(times_string): raise Exception("Unequal Dimensions {} {}".format(
        len(bases_string), len(times_string)
    ))

    with open('./examples/bases.csv', 'w') as file:
        file.writelines(bases_string)
    with open('./examples/demand_points.csv', 'w') as file:
        file.writelines(demands_string)
    with open('./examples/times.csv', 'w') as file:
        file.writelines(times_string)

    end_time = timer()

    print("Total Duration:", str(timedelta(seconds=(end_time - start_time))))


if __name__ == "__main__": main()
