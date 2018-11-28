from datetime import datetime


class Metric:

    def __init__(self, tag: str):
        self.tag = tag

    def __eq__(self, other):
        return self.tag == self.tag

    def calculate(self,
                  timestamp: datetime,
                  **kwargs):
        raise NotImplementedError()
