# ASSUMPTIONS
# (1a) The average person does NOT want to view a year's worth of simulation.
# (2a) The number of dots in total should be directly proportional to the number of seconds
# (2b) The number of dots visible should be constant to show velocity.
# (3a) There's a fixed number of ambulances

# ALLOWANCES
# (1a) I CAN enumerate every second of the simulation here.
# (2a) num_dots = num_seconds * rate of change
# (2b) It'll probably be 200 or something.
# (3a) Each ambulance can have its own color that it retains for duration of the visualization.

# The Visualizer should:
    # Know the total number of seconds of the entire simulation.
        # Make a list length num_seconds
    # Define a function to convert seconds into dots. We can set the frame rate later.
    # Make sure to know what color each ambulance is.


# Start:
    # Start time for the ambulance
    # Start and end positions, and the time it takes to reach from s to e.

# End:
    # Using the start time for the amb, calculate the number of dots to reach the end
    # Using the duration and the start time, calculate the new start time. Repeat until
    # no more paths to take.



srcfile = '../results/processed_cases.csv'

class PathVisualizer:
    """ Each case should have three instances of these enumerated.
    Takes the data from the CSV and changes into start dot, end dot, and
    range of dots that is going to be displayed at each second of the simulation.

    The number of dots won't work anymore.

    Let's say one dot per minute?
    """

    pass

class RegionalVisualizer:
    """ Total number of cases """
    def __init__(self, source_file):
        pass
