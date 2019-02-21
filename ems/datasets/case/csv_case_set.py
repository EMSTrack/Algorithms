# Interface for a "set" of cases
from datetime import datetime

from geopy import Point

from ems.datasets.case.case_set import CaseSet
from ems.generators.event.event_generator import EventGenerator
from ems.models.cases.random_case import RandomCase
from ems.utils import parse_headered_csv


class CSVCaseSet(CaseSet):

    def __init__(self,
                 filename: str,
                 event_generator: EventGenerator,
                 headers=None):

        if headers is None:
            headers = ["id", "date", "latitude", "longitude", "priority"]

        self.headers = headers
        self.filename = filename
        self.event_generator = event_generator
        self.cases = self.read_cases()

    def iterator(self):
        return iter(self.cases)

    def __len__(self):
        return len(self.cases)

    def read_cases(self):

        # Read cases from CSV into a pandas dataframe
        cases_df = parse_headered_csv(self.filename, self.headers)

        # TODO -- Pass in dict or find another way to generalize ordering of headers
        id_key = self.headers[0]
        timestamp_key = self.headers[1]
        latitude_key = self.headers[2]
        longitude_key = self.headers[3]
        priority_key = self.headers[4] if len(self.headers) > 3 else None

        # Generate list of models from dataframe
        cases = []
        for index, row in cases_df.iterrows():
            case = RandomCase(id=row[id_key],
                              date_recorded=datetime.strptime(row[timestamp_key], '%Y-%m-%d %H:%M:%S.%f'),
                              incident_location=Point(row[latitude_key], row[longitude_key]),
                              event_generator=self.event_generator,
                              priority=row[priority_key] if priority_key is not None else None)
            cases.append(case)

        cases.sort(key=lambda x: x.date_recorded)

        return cases
