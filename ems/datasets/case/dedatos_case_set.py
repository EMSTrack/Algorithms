# Implementation of a case set which is instantiated from a list of already known cases
import pandas as pd
from geopy import Point

from ems.datasets.case.case_set import CaseSet
from ems.generators.event.random_duration import RandomDurationGenerator
from ems.models.cases.random_case import RandomCase
from ems.utils import parse_headered_csv


class DeDatosCaseSet(CaseSet):

    def __init__(self,
                 filename: str):
        self.filename = filename
        self.cases = self.read_cases(filename)

    def iterator(self):
        return iter(self.cases)

    def __len__(self):
        return len(self.cases)

    def read_cases(self, filename):

        # Read cases from CSV into a pandas dataframe
        case_headers = ["id", "lat", "long", "date", "weekday", "time", "priority"]
        cases_df = parse_headered_csv(filename, case_headers)

        # Aggregates columms 'date' and 'time' to produce a column for datetime objects
        # TODO -- SLOW OPERATION - find a better way to parse date and time to datetime object
        cases_df["datetime"] = pd.to_datetime(cases_df.date + ' ' + cases_df.time)

        # Sorts all cases by their datetimes (REQUIRED BY SIMULATOR)
        cases_df = cases_df.sort_values('datetime', ascending=True)

        cases_df = cases_df[:100]

        # Generate list of models from dataframe
        cases = []
        for index, row in cases_df.iterrows():
            case = RandomCase(id=row["id"],
                              date_recorded=row["datetime"],
                              incident_location=Point(row["lat"], row["long"]),
                              event_duration_generator=RandomDurationGenerator(),
                              priority=row["priority"])
            cases.append(case)

        return cases
