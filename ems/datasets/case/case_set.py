# Interface for a "set" of cases
class CaseSet:

    def __len__(self):
        raise NotImplementedError()

    def iterator(self):
        raise NotImplementedError()
