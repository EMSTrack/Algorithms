from datetime import timedelta

import pandas as pd
from typing import List
import bisect

from ems.analysis.records.case_record import CaseRecord
from ems.models.events.event_type import EventType


class CaseRecordSet:

    # TODO -- test sort case records
    def __init__(self,
                 case_records: List[CaseRecord] = None):

        if case_records is None:
            case_records = []

        self.case_records = case_records
        self.case_records.sort()

    def add_case_record(self, case_record: CaseRecord):
        bisect.insort(self.case_records, case_record)

    def write_to_file(self, output_filename):
        a = []
        for case_record in self.case_records:

            d = {"id": case_record.case.id,
                 "date recorded": case_record.case.date_recorded,
                 "case latitude": case_record.case.incident_location.latitude,
                 "case longitude": case_record.case.incident_location.longitude,
                 "priority": case_record.case.priority,
                 "ambulance": case_record.ambulance.id,
                 "start time": case_record.start_time}

            total_durations_other = timedelta(minutes=0)
            for event in case_record.event_history:

                if event == EventType.OTHER:
                    total_durations_other += event.duration
                else:

                    d[event.event_type.name + " duration"] = event.duration

                    if event.event_type == EventType.TO_HOSPITAL:
                        d["hospital latitude"] = event.destination.latitude
                        d["hospital longitude"] = event.destination.longitude

            d["OTHER duration"] = total_durations_other

            a.append(d)

        event_labels = [event_type.name + " duration" for event_type in EventType]

        df = pd.DataFrame(a, columns=["id", "date recorded", "case latitude", "case longitude",
                                      "priority", "ambulance", "start time"] + event_labels +
                                     ["hospital latitude", "hospital longitude"])
        df.to_csv(output_filename, index=False)
