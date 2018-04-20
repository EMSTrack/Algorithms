
# Define the Ambulance model. 

class Ambulance():
    def __init__(self, 
    			id, 
    			base, 
    			unit="XXX-XXXX",
    			deployed=False,
    			location=None,
    			deployed_time=None,
    			end_time=None):

    	# TODO tyoe checking

    	self.id               	= None
    	self.unit				= "XXX-XXXX"
    	self.deployed         	= False
    	self.base				= None
    	self.location			= None
    	self.deployed_time    	= None
    	self.end_time			= None
