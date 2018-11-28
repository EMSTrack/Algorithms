from datetime import datetime
from typing import List

from ems.analysis.metrics.metric import Metric

import pandas as pd


class MetricAggregator:

    # TODO -- enforce metric tags unique
    def __init__(self,
                 metrics: List[Metric] = None):

        if metrics is None:
            metrics = []

        self.metrics = metrics
        self.results = []

    def add_metric(self, metric: Metric):

        if metric in self.metrics:
            # TODO custom exception
            raise Exception("Metric with tag '{}' already exists".format(metric.tag))

        self.metrics.append(metric)

    def remove_metric(self, metric: Metric):
        self.metrics.remove(metric)

    def calculate(self,
                  timestamp: datetime,
                  **kwargs):

        d = {"timestamp": timestamp}
        for metric in self.metrics:
            calculation = metric.calculate(timestamp, **kwargs)
            if calculation is not None:
                d[metric.tag] = calculation

        self.results.append(d)
        return d

    def write_to_file(self, output_filename):
        df = pd.DataFrame(self.results, columns=["timestamp"] + [metric.tag for metric in self.metrics])
        df.to_csv(output_filename, index=False)
