import numpy as np


def kmeans_select_bases(bases, traveltimes):
    # This function happens to require the original Cruz Roja dataset. It doesn't necessarily need to.
    # For example, we could randomly choose bases.

    print("Default init_bases(): Kmeans init bases")

    # times[demand point][base] if using the pandas way
    # Using pandas dataframe
    chosen_base_indices, demands_covered = pick_starting_bases(traveltimes, 12, 600)

    # Returns object list
    chosen_bases = [bases[index] for index in chosen_base_indices]

    return chosen_bases


# Refactor TODO. I can't believe I just shoved this in and it worked.
def pick_starting_bases(traveltimes, num_bases, required_traveltime):
    np_traveltimes = np.array(traveltimes.times)
    chosen_bases = []
    demands_covered = 0

    for _ in range(num_bases):
        # Make a True/False table of the times and then count how many covered.
        covered = [[t < required_traveltime for t in row] for row in np_traveltimes]
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
        np_traveltimes = np.delete(np_traveltimes, delete_cols, axis=1)

    return chosen_bases, demands_covered