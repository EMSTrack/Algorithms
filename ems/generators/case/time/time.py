from datetime import datetime


# Interface for a case time generator; should randomly generate the next datetime of an incident
class CaseTimeGenerator:

    def generate(self,
                 time: datetime):
        raise NotImplementedError()
