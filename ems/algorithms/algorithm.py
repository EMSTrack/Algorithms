# Framework for using algorithms and allowing for replacement

# from datetime import timedelta
import copy
import numpy as np

# The following functions define default algorithms for the DispatchAlgorithm class.
def kmeans_init_bases (dataset):
    
    # This function happens to require the original Cruz Roja dataset. It doesn't necessarily need to. 
    # For example, we could randomly choose bases.

    print("Default init_bases(): Kmeans init bases")

    # times[demand point][base] if using the pandas way
    chosen_base_indices, demands_covered =  pick_starting_bases (dataset.traveltimes, 12, 600)
    chosen_bases = dataset.bases_df.iloc[chosen_base_indices]
    return chosen_bases

# Refactor TODO. I can't believe I just shoved this in and it worked.
def pick_starting_bases(traveltimes, num_bases, required_traveltime):

    assert isinstance(required_traveltime, int)

    traveltimes         = copy.deepcopy (traveltimes)
    traveltimes         = np.array (traveltimes)
    chosen_bases        = []
    demands_covered     = 0

    for _ in range(num_bases):

        # Make a True/False table of the times and then count how many covered. 
        covered         = [[t<required_traveltime for t in row] for row in traveltimes]
        count_covered   = [(index, covered[index].count(True)) for index in range(len(covered))]
        d               = [('index', int), ('covered', int)]
        count_covered   = np.array(count_covered, d)

        # Sort the table by row and grab the last element (the base with the most coverage)
        (best_base, count)  = np.sort(count_covered, order='covered', kind='mergesort')[-1]
        chosen_bases.append(best_base)
        demands_covered     += count
        demand_coverage     = covered[best_base]

        # Delete the covered columns 
        delete_cols     = [d for d in range(len(demand_coverage)) if demand_coverage[d]]
        traveltimes     = np.delete(traveltimes, delete_cols, axis=1)

    return chosen_bases, demands_covered


def random_ambulance_placements (dataset):
    print("Default init_ambulance_placements(): Random Ambulance Placements")

def fastest_traveltime (dataset):
    print("Default select_ambulance(): Fastest Traveltime")


# This class is used by the sim to run.
class DispatcherAlgorithm ():

    # To instantiate this object, three function pointers must have been passed in.
    def __init__ (self, 
        init_bases                 = kmeans_init_bases, 
        init_ambulance_placements  = random_ambulance_placements, 
        select_ambulance           = fastest_traveltime ):

        assert callable(init_bases)
        assert callable(init_ambulance_placements)
        assert callable(select_ambulance)

        self.init_bases                  = init_bases
        self.init_ambulance_placements   = init_ambulance_placements
        self.select_ambulance            = select_ambulance

    def init_bases_typecheck(self, dataset):
        """ Runs init_bases, but makes sure the resulting data.chosen_bases is right type """
        self.init_bases (dataset)
        assert isinstance (dataset.chosen_bases, list)
        for element in dataset.chosen_bases:
            assert isinstance (element, Base)


    def init_ambulance_placements_typecheck(self, dataset):
        """ Runs init_ambulance_placements, but makes sure the resulting ___ is right type or state"""
        pass 

    def select_ambulance_typecheck(self, dataset):
        """ Runs select_ambulance, but makes sure the resulting ___ is right type or state"""
        pass





