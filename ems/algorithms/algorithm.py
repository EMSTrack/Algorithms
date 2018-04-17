def kmeans_init_bases (data):
    print("Kmeans init bases")

def random_ambulance_placements (data):
    print("Random Ambulance Placements")

def fastest_traveltime (data):
    print("Fastest Traveltime")

class DispatcherAlgorithm():

    def __init__ (self, 
        init_bases=kmeans_init_bases, 
        init_ambulance_placements=random_ambulance_placements, 
        select_ambulance=fastest_traveltime):

        # TODO type checking
        self.init_bases = init_bases
        self.init_ambulance_placements = init_ambulance_placements
        self.select_ambulance = select_ambulance



da = DispatcherAlgorithm()

da.init_bases(None)
da.init_ambulance_placements(None)
da.select_ambulance(None)

