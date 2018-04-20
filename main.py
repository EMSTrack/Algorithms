from ems.algorithms.algorithm import DispatcherAlgorithm

from ems.settings import Settings
from ems.data import CSVTijuanaData

file_path = '/Users/timothylam/Documents/school/ENG100L/data-cruz-roja/'
bases_filepath = file_path + 'bases.csv'
demands_filepath = file_path + 'demand_points.csv'
cases_filepath = file_path + 'calls.csv'
traveltimes_filepath = file_path + 'times.csv'

settings = Settings (debug=False, 
                demands_file=demands_filepath,
                bases_file=bases_filepath,
                cases_file=cases_filepath,
                traveltimes_file=traveltimes_filepath)

data = CSVTijuanaData(settings)

da = DispatcherAlgorithm()

b = da.init_bases(data)
print(b)

# Call simulator