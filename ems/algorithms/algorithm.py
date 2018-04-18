# Framework for using algorithms and allowing for replacement

from ems.data import Base # Only for type checking

# from datetime import timedelta
import copy
import numpy as np

# The following functions define default algorithms for the DispatchAlgorithm class.
def kmeans_init_bases (data):
    
    # This function happens to require the original Cruz Roja dataset. It doesn't necessarily need to. 
    # For example, we could randomly choose bases.

    print("Default init_bases(): Kmeans init bases")

    # Read the travel times. This does not necessarily need to be here.
    import pandas as pd 
    times = pd.read_csv("/Users/vectflux/Documents/Data/times.csv", header = None)
    # times[col][row] (different from before)
    # times[demand point][base]
    chosen_bases, demands_covered =  pick_starting_bases (times, 12, 600)
    converted_bases = [Base(data.bases.iloc[chosen_base]) for chosen_base in chosen_bases]
    return converted_bases
    # import IPython; IPython.embed()

# Refactor TODO. I can't believe I just shoved this in and it worked.
def pick_starting_bases(traveltimes, num_bases, required_traveltime):

    assert isinstance(required_traveltime, int)

    traveltimes = copy.deepcopy (traveltimes)
    traveltimes = np.array (traveltimes)
    chosen_bases = []
    demands_covered = 0

    for _ in range(num_bases):

        # Make a True/False table of the times and then count how many covered. 
        covered = [[t<required_traveltime for t in row] for row in traveltimes]
        count_covered = [(index, covered[index].count(True)) for index in range(len(covered))]
        d = [('index', int), ('covered', int)]
        count_covered = np.array(count_covered, d)

        # Sort the table by row and grab the last element (the base with the most coverage)
        (best_base, count) = np.sort(count_covered, order='covered', kind='mergesort')[-1]
        chosen_bases.append(best_base)
        demands_covered += count
        demand_coverage = covered[best_base]

        # Delete the covered columns 
        delete_cols = [d for d in range(len(demand_coverage)) if demand_coverage[d]]
        traveltimes = np.delete(traveltimes, delete_cols, axis=1)

    return chosen_bases, demands_covered


def random_ambulance_placements (data):
    print("Default init_ambulance_placements(): Random Ambulance Placements")

def fastest_traveltime (data):
    print("Default select_ambulance(): Fastest Traveltime")


# This class is used by the sim to run.
class DispatcherAlgorithm ():

    def __init__ (self, 
        init_bases                 = kmeans_init_bases, 
        init_ambulance_placements  = random_ambulance_placements, 
        select_ambulance           = fastest_traveltime ):

        assert callable(init_bases)
        assert callable(init_ambulance_placements)
        assert callable(select_ambulance)

        # TODO type checking
        self.init_bases                  = init_bases
        self.init_ambulance_placements   = init_ambulance_placements
        self.select_ambulance            = select_ambulance

    def init_bases_typecheck(self, data):
        """ Runs init_bases, but makes sure the return type is correct """
        output = self.init_bases (data)
        assert isinstance (output, list)
        for element in output:
            assert isinstance (element, Base)
