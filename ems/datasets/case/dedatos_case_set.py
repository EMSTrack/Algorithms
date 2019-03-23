# Implementation of a case set which is instantiated from a list of already known cases
import pandas as pd
from geopy import Point

from ems.datasets.case.case_set import CaseSet
from ems.generators.event.event_generator import EventGenerator
from ems.models.cases.random_case import RandomCase
from ems.utils import parse_headered_csv


class DeDatosCaseSet(CaseSet):

    def __init__(self,
                 filename: str,
                 event_generator: EventGenerator):
        self.filename = filename
        self.event_generator = event_generator
        self.cases = self.read_cases()
        super().__init__(self.cases[0].date_recorded)

    def iterator(self):
        return iter(self.cases)

    def __len__(self):
        return len(self.cases)

    def read_cases(self):

        # Read cases from CSV into a pandas dataframe
        case_headers = ["id", "latitud", "longitud", "fecha", "dia_semana", "hora_llamada", "vprioridad"]
        cases_df = parse_headered_csv(self.filename, case_headers)

        # Aggregates columms 'date' and 'time' to produce a column for datetime objects
        # TODO -- SLOW OPERATION - find a better way to parse date and time to datetime object
        cases_df["datetime"] = pd.to_datetime(cases_df.fecha + ' ' + cases_df.hora_llamada)

        # Sorts all cases by their datetimes (REQUIRED BY SIMULATOR)
        cases_df = cases_df.sort_values('datetime', ascending=True)

        cases_df = cases_df[:100]

        # Generate list of models from dataframe
        cases = []
        for index, row in cases_df.iterrows():
            case = RandomCase(id=row["id"],
                              date_recorded=row["datetime"],
                              incident_location=Point(row["latitud"], row["longitud"]),
                              event_generator=self.event_generator,
                              priority=row["vprioridad"])
            cases.append(case)

        return cases
