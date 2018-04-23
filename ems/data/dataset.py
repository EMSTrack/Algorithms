# Model the data by their types.

class Dataset:

    def get_bases(self):
        raise NotImplementedError()

    def get_cases(self):
        raise NotImplementedError()

    def get_demands(self):
        raise NotImplementedError()
