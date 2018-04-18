# Framework for using algorithms and allowing for replacement

from ems.data import Base # Only for type checking

# The following functions define default algorithms for the DispatchAlgorithm class.
def kmeans_init_bases (data):
    print("Default init_bases(): Kmeans init bases")

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

        def init_bases_typecheck():
            output = init_bases()
            assert isinstance(output, list)
            for element in output:
                assert isinstance(element, Base)


