import pandas as pd

from geopy import Point

from ems.data.dataset import Dataset
from ems.data.travel_times import TravelTimes
from ems.models.case import ListCase
from ems.models.event import Event
from ems.models.event_type import EventType
from ems.models.location_point import LocationPoint
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

        # Sort cases by their departure times
        cases_df = cases_df.sort_values('depart_dt', ascending=True)

        # Generate list of models from dataframe
        cases = []
        for index, row in cases_df.iterrows():

            # LocationPoint capturing when ambulance departed from base
            base_lp_departure = LocationPoint(location=Point(latitude=row["Latitud salida"],
                                                             longitude=row["Longitud salida"]),
                                              timestamp=row['depart_dt'])

            # LocationPoint capturing when ambulance arrived (and departed) from incident
            # TODO -- No event capturing the time to attend to patient at incident; not included in dataset
            incident_lp = LocationPoint(location=Point(latitude=row["Latitud llegada incidente"],
                                                       longitude=row["Longitud llegada incidente"]),
                                        timestamp=row["incident_arrival_dt"])

            # LocationPoint capturing when ambulance arrived (and departed) from incident
            hospital_lp = LocationPoint(location=Point(latitude=row["Latitud arribo al hospital"],
                                                       longitude=row['Longitud arribo al hospital']),
                                        timestamp=row["hospital_arrival_dt"])

            # LocationPoint capturing when ambulance returned to original base
            # Timestamp of return not provided; may not be a necessary event
            base_lp_return = LocationPoint(location=Point(latitude=row["Latitud salida"],
                                                          longitude=row["Longitud salida"]),
                                           timestamp=None)

            # Event capturing ambulance travelling from base to incident
            base_to_incident_event = Event(origin=base_lp_departure,
                                           destination=incident_lp,
                                           event_type=EventType.INCIDENT)

            # Event capturing ambulance travelling from incident to hospital
            incident_to_hospital_event = Event(origin=incident_lp,
                                               destination=hospital_lp,
                                               event_type=EventType.HOSPITAL)

            # Event capturing ambulance travelling from hospital to base
            hospital_to_base_event = Event(origin=hospital_lp,
                                           destination=base_lp_return,
                                           event_type=EventType.BASE)

            # Generate a case from events
            events = [base_to_incident_event, incident_to_hospital_event, hospital_to_base_event]
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