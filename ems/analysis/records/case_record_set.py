import heapq
import pandas as pd
from typing import List

from ems.analysis.records.case_record import CaseRecord
from ems.models.events.event_type import EventType


class CaseRecordSet:

    # TODO enforce case_records sorted
    def __init__(self,
                 case_records: List[CaseRecord] = None):

        if case_records is None:
            case_records = []

        self.case_records = case_records

    def add_case_record(self, case_record: CaseRecord):
        heapq.heappush(self.case_records, case_record)

    def write_to_file(self, output_filename):
        a = []
        for case_record in self.case_records:

            d = {"id": case_record.case.id,
                 "date_recorded": case_record.case.date_recorded,
                 "incident_latitude": case_record.case.incident_location.latitude,
                 "incident_longitude": case_record.case.incident_location.longitude,
                 "priority": case_record.case.priority,
                 "ambulance": case_record.ambulance.id,
                 "start_time": case_record.start_time}

            for event in case_record.event_history:
                d[event.event_type.name + "_duration"] = event.duration

                if event.event_type == EventType.TO_HOSPITAL:
                    d["hospital_latitude"] = event.destination.latitude
                    d["hospital_longitude"] = event.destination.longitude

            a.append(d)

        event_labels = [event_type.name + "_duration" for event_type in EventType]

        df = pd.DataFrame(a, columns=["id", "date_recorded", "incident_latitude", "incident_longitude",
                                      "priority", "ambulance", "start_time"] + event_labels +
                                     ["hospital_latitude", "hospital_longitude"])
        df.to_csv(output_filename, index=False)
