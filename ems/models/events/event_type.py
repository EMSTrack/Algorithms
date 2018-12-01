from enum import Enum


class EventType(Enum):
    __order__ = 'TO_INCIDENT AT_INCIDENT TO_HOSPITAL AT_HOSPITAL TO_BASE OTHER'

    TO_INCIDENT = "Heading to Incident"
    AT_INCIDENT = "Attending to Incident"
    TO_HOSPITAL = "Heading to Hospital"
    AT_HOSPITAL = "Dropping off Patient at Hospital"
    TO_BASE = "Returning to Base"
    OTHER = "Other"

