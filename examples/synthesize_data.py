
from geopy.distance import distance
import random
from multiprocessing import cpu_count
from multiprocessing import Pool
from functools import reduce
from timeit import default_timer as timer
from datetime import timedelta

multicpu = True

# Coordinate range for Tijuana, Mexico
lat1 = 32.4008
lat2 = 32.5534
lon1 = -117.1233
lon2 = -116.777

# Number of bases and demands
cpu = cpu_count()

# cpu = 1
# cpu = cpu // 2
# cpu = cpu * 3 // 4

cpu = int(cpu)

print("Processes:", cpu)

bases_num   = 400
demands_num = 400

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

    if not multicpu:
        base_locations =    generate_points(bases_num)
        times =             generate_times(base_locations)

    else:
        list_base_locations = [generate_points(bases_num // cpu) for _ in range(cpu)]

        with Pool(cpu) as p:
            list_of_times = p.map(generate_times, list_base_locations)

        times =             flatten(list_of_times)
        base_locations =    flatten(list_base_locations)

    baseline = "'id','name','type','vics',"
    bases_string = ["{}{},{}\n".format(baseline, b[0], b[1]) for b in base_locations]
    demands_string = ["{},{}\n".format(d[0], d[1]) for d in demand_locations]
    times_string = [",".join(b) + "\n" for b in times]

    print("Write to files.")

    with open('bases.csv', 'w') as file:            file.writelines(bases_string)
    with open('demand_points.csv', 'w') as file:    file.writelines(demands_string)
    with open('times.csv', 'w') as file:            file.writelines(times_string)

    end_time = timer()

    print("Total Duration:", str(timedelta(seconds=(end_time - start_time))))


if __name__ == "__main__": main()
