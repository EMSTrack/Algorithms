from datetime import datetime
from typing import List

from ems.analysis.metric import Metric

import pandas as pd


class MetricAggregator:

    # TODO -- enforce metric tags unique
    def __init__(self,
                 metrics: List[Metric] = None):

        if metrics is None:
            metrics = []

        self.metrics = metrics
        self.results = {}

        for metric in metrics:
            self.results[metric.tag] = []

    def add_metric(self, metric: Metric):

        if metric in self.metrics:
            # TODO custom exception
            raise Exception("Metric with tag '{}' already exists".format(metric.tag))

        self.metrics.append(metric)
        self.results[metric.tag] = []

    def remove_metric(self, metric: Metric):
        self.metrics.remove(metric)
        self.results.pop(metric.tag)

    def calculate(self,
                  timestamp: datetime,
                  **kwargs):

        d = {}
        for metric in self.metrics:

            calculation = metric.calculate(timestamp, **kwargs)

            if calculation is not None:
                self.results[metric.tag].append(calculation)
                d[metric.tag] = calculation

        return d

    def write_to_file(self, output_directory):

        for metric in self.metrics:
            metric_results = self.results[metric.tag]
            df = pd.DataFrame(metric_results)

            # Write results to CSV
            df.to_csv(output_directory + '/' + metric.tag + '.csv')

