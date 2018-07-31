from geopy import Point

from ems.data.dataset import Dataset
from ems.data.travel_times import TravelTimes
from ems.models.case import ListCase
from ems.models.event import Event
from ems.models.location_set import LocationSet
from ems.utils import parse_headered_csv, parse_unheadered_csv


class Jan2017Dataset(Dataset):

    def __init__(self,
                 demands_file_path: str,
                 bases_file_path: str,
                 cases_file_path: str,
                 travel_times_file_path: str,
                 ):

        # Read files into pandas dataframes and lists of objects
        self.demands = self.read_demands(demands_file_path)
        self.bases = self.read_bases(bases_file_path)
        self.cases = self.read_cases(cases_file_path)

        travel_times_df = self.read_times_df(travel_times_file_path)

        self.travel_times = TravelTimes(loc_set_1=self.bases,
                                        loc_set_2=self.demands,
                                        times=travel_times_df.as_matrix())

    # Helper functions
    def read_cases(self, filename):
        # Read cases from CSV into a pandas dataframe
        case_headers = ["Fecha", "No_unidad", "Dia_semana", "Latitud salida", "Longitud salida",
                        "Hora_salida", "Latitud llegada incidente" ,"Longitud llegada incidente",
                        "Hora_llegada incidente" , "Latitud salida al hospital", "Longitud  salida al hospital",
                        "Hora_salida al hospital" , "Latitud arribo al hospital", "Longitud arribo al hospital",
                        "Hora_arribo al hospital", "Tiempo_base_incidente", "Tiempo dando atencion pre-hospitalaria ",
                        "Tiempo_incidente_hospital", "tiempo_total base-hospital"]
        cases_df = parse_headered_csv(filename, case_headers)

        cases_df["depart_dt"] = pd.to_datetime(cases_df['Fecha'] + ' ' + cases_df['Hora_salida'])
        cases_df["incident_arrival_dt"] = pd.to_datetime(cases_df['Fecha'] + '' + cases_df['Hora_llegada incidente'])
        cases_df["hospital_arrival_dt"] = pd.to_datetime(cases_df['Fecha'] + '' + cases_df['Hora_arribo al hospital'])

        cases_df = cases_df.sort_values('datetime', ascending=True)

        # Generate list of models from dataframe
        cases = []
        for index, row in cases_df.iterrows():

            # Timestamp of case start, destination is the incident destination
            base_to_incident_event = Event(timestamp=row['depart_dt'],
                                           destination=Point(latitude=row['Latitud llegada incidente'],
                                                             longitude=row['Longitud llegada incidente']),
                                           label="Travelling to Incident")

            # Timestamp of incident arrival, destination is the hospital destination
            incident_to_hospital_event = Event(timestamp=row['incident_arrival_dt'],
                                               destination=Point(latitude=row['Latitud arribo al hospital'],
                                                                 longitude=row['Longitud arribo al hospital']),
                                               label="Travelling to Hospital")

            # Timestamp of hospital arrival, destination is the base destination
            hospital_to_base_event = Event(timestamp=row['hospital_arrival_dt'],
                                           destination=Point(latitude=row['Latitud salida'],
                                                             longitude=row['Longitud salida']),
                                           label="Travelling to Base")

            # Timestamp of arrival back to base, no set destination
            # TODO -- no timestamp of arrival provided
            base_arrival_event = Event(timestamp=None,
                                       destination=None,
                                       label="Arrived Back to Base")

            events = [base_to_incident_event, incident_to_hospital_event, hospital_to_base_event, base_arrival_event]

            # Create case
            case = ListCase(id=row['id'],
                            events=events)

            cases.append(case)

        return cases

    def read_bases(self, filename):
        # Read bases from an unheadered CSV into a pandas dataframe
        base_col_positions = [4, 5]
        base_headers = ["lat", "long"]
        bases_df = parse_unheadered_csv(filename, base_col_positions, base_headers)

        # Generate list of models from dataframe
        bases = []
        for index, row in bases_df.iterrows():
            base = Point(row["lat"], row["long"])
            bases.append(base)

        return LocationSet(bases)

    def read_demands(self, filename):
        # Read demands from an unheadered CSV into a pandas dataframe
        demand_col_positions = [0, 1]
        demand_headers = ["lat", "long"]
        demands_df = parse_unheadered_csv(filename, demand_col_positions, demand_headers)

        # Generate list of models from dataframe
        demands = []
        for index, row in demands_df.iterrows():
            demand = Point(row["lat"], row["long"])
            demands.append(demand)

        return LocationSet(demands)

    def read_times_df(self, filename):
        # Read travel times from CSV file into a pandas dataframe
        travel_times_df = pd.read_csv(filename)

        return travel_times_df

    # Implementation
    def get_cases(self):
        return self.cases