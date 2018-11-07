# Interface for a "set" of cases
class CaseSet:

    def iterator(self):
        raise NotImplementedError()