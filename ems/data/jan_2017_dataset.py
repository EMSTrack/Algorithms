from datetime import datetime

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
                        "Hora_salida", "Latitud llegada incidente", "Longitud llegada incidente",
                        "Hora_llegada incidente", "Latitud salida al hospital", "Longitud  salida al hospital",
                        "Hora_salida al hospital", "Latitud arribo al hospital", "Longitud arribo al hospital",
                        "Hora_arribo al hospital", "Tiempo_base_incidente", "Tiempo dando atencion pre-hospitalaria ",
                        "Tiempo_incidente_hospital", "tiempo_total base-hospital"]
        cases_df = parse_headered_csv(filename, case_headers)

        # Datetime format
        dt_format = "%m/%d/%Y %H:%M:%S"

        # Generate list of models from dataframe
        cases = []
        for index, row in cases_df.iterrows():

            ### Datetimes

            # Create strings for dates; used to convert to datetimes
            base_depart_dt_str = row["Fecha"] + " " + row["Hora_salida"]
            incident_arrival_dt_str = row["Fecha"] + " " + row["Hora_llegada incidente"]
            incident_depart_dt_str = row["Fecha"] + " " + row["Hora_salida al hospital"]
            hospital_arrival_dt_str = row["Fecha"] + " " + row["Hora_arribo al hospital"]

            # Generate datetimes
            base_depart_dt = datetime.strptime(base_depart_dt_str, dt_format)
            incident_arrival_dt = datetime.strptime(incident_arrival_dt_str, dt_format)
            incident_depart_dt = datetime.strptime(incident_depart_dt_str, dt_format)
            hospital_arrival_dt = datetime.strptime(hospital_arrival_dt_str, dt_format)

            ### Location Points

            # LocationPoint capturing when ambulance departed from base
            base_depart_lp = LocationPoint(location=Point(latitude=row["Latitud salida"],
                                                          longitude=row["Longitud salida"]),
                                           timestamp=base_depart_dt)

            # LocationPoint capturing when ambulance arrived to incident
            incident_arrival_lp = LocationPoint(location=Point(latitude=row["Latitud llegada incidente"],
                                                               longitude=row["Longitud llegada incidente"]),
                                                timestamp=incident_arrival_dt)

            incident_depart_lp = None
            hospital_arrival_lp = None

            if row["Latitud salida al hospital"] != 0:
                # LocationPoint capturing when ambulance left incident for hospital
                incident_depart_lp = LocationPoint(location=Point(latitude=row["Latitud llegada incidente"],
                                                                  longitude=row["Longitud llegada incidente"]),
                                                   timestamp=incident_depart_dt)

                # LocationPoint capturing when ambulance arrived to hospital
                hospital_arrival_lp = LocationPoint(location=Point(latitude=row["Latitud arribo al hospital"],
                                                                   longitude=row['Longitud arribo al hospital']),
                                                    timestamp=hospital_arrival_dt)

                # TODO -- No information on length of stay at hospital - no event for hospital stay length

            # LocationPoint capturing when ambulance returned to original base (no timestamp provided by dataset)
            base_return_lp = LocationPoint(location=Point(latitude=row["Latitud salida"],
                                                          longitude=row["Longitud salida"]),
                                           timestamp=None)

            ### Events
            events = []

            # Event capturing ambulance travelling from base to incident
            base_to_incident_event = Event(origin=base_depart_lp,
                                           destination=incident_arrival_lp,
                                           event_type=EventType.TO_INCIDENT)
            events.append(base_to_incident_event)

            if incident_depart_lp is not None:
                # Event capturing patient pickup
                # TODO -- When there is no patient to bring to hospital, no information provided on incident departure
                at_incident_event = Event(origin=incident_arrival_lp,
                                          destination=incident_depart_lp,
                                          event_type=EventType.AT_INCIDENT)
                events.append(at_incident_event)

                # Event capturing ambulance travelling from incident to hospital
                incident_to_hospital_event = Event(origin=incident_depart_lp,
                                                   destination=hospital_arrival_lp,
                                                   event_type=EventType.TO_HOSPITAL)
                events.append(incident_to_hospital_event)

                # Event capturing ambulance travelling from hospital to base
                # TODO -- May not be necessary; ambulances free as soon as they leave hospital
                hospital_to_base_event = Event(origin=hospital_arrival_lp,
                                               destination=base_return_lp,
                                               event_type=EventType.TO_BASE)
                events.append(hospital_to_base_event)

            else:
                # Event capturing ambulance travelling from incident to base
                # TODO -- May not be necessary; ambulances free as soon as they leave incident
                incident_to_base_event = Event(origin=incident_arrival_lp,
                                               destination=base_return_lp,
                                               event_type=EventType.TO_BASE)
                events.append(incident_to_base_event)

            # Generate a case from events
            case = ListCase(id=index,
                            events=events)

            cases.append(case)

        # Sort all cases by the departure time from base
        cases.sort(key=lambda case: case.events[0].origin.timestamp)

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
