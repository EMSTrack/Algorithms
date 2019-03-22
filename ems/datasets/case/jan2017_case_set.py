# Implementation of a case set which is instantiated from a list of already known cases
from datetime import datetime

from geopy import Point

from ems.datasets.case.case_set import CaseSet
from ems.models.cases.defined_case import DefinedCase
from ems.models.events.event import Event
from ems.models.events.event_type import EventType
from ems.utils import parse_headered_csv


class Jan2017CaseSet(CaseSet):

    def __init__(self,
                 filename: str):
        self.filename = filename
        self.cases = self.read_cases(filename)
        super().__init__(self.cases[0].date_recorded)

    def iterator(self):
        return iter(self.cases)

    def __len__(self):
        return len(self.cases)

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

            ### Events
            events = []

            # Event capturing ambulance travelling from base to incident
            base_to_incident_event = Event(destination=Point(latitude=row["Latitud llegada incidente"],
                                                             longitude=row["Longitud llegada incidente"]),
                                           event_type=EventType.TO_INCIDENT,
                                           duration=incident_arrival_dt - base_depart_dt)
            events.append(base_to_incident_event)

            if row["Latitud salida al hospital"] != 0:
                # Event capturing patient pickup
                # TODO -- When there is no patient to bring to hospital, no information provided on incident departure
                at_incident_event = Event(destination=Point(latitude=row["Latitud llegada incidente"],
                                                            longitude=row["Longitud llegada incidente"]),
                                          event_type=EventType.AT_INCIDENT,
                                          duration=incident_depart_dt - incident_arrival_dt)
                events.append(at_incident_event)

                # Event capturing ambulance travelling from incident to hospital
                incident_to_hospital_event = Event(destination=Point(latitude=row["Latitud arribo al hospital"],
                                                                     longitude=row['Longitud arribo al hospital']),
                                                   event_type=EventType.TO_HOSPITAL,
                                                   duration=hospital_arrival_dt - incident_depart_dt)
                events.append(incident_to_hospital_event)

                # Event capturing ambulance travelling from hospital to base
                hospital_to_base_event = Event(destination=Point(latitude=row["Latitud salida"],
                                                                 longitude=row["Longitud salida"]),
                                               event_type=EventType.TO_BASE)
                events.append(hospital_to_base_event)

            else:
                # Event capturing ambulance travelling from incident to base
                incident_to_base_event = Event(destination=Point(latitude=row["Latitud salida"],
                                                                 longitude=row["Longitud salida"]),
                                               event_type=EventType.TO_BASE)
                events.append(incident_to_base_event)

            # Generate a case from events
            case = DefinedCase(id=index,
                               date_recorded=base_depart_dt,
                               incident_location=Point(latitude=row["Latitud llegada incidente"],
                                                       longitude=row["Longitud llegada incidente"]),
                               events=events)

            cases.append(case)

        # Sort all cases by the departure time from base
        cases.sort(key=lambda case: case.date_recorded)

        return cases
