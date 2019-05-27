#TODO PYDOC

from datetime import datetime
from typing import List

from ems.analysis.metrics.metric import Metric

import pandas as pd


class MetricAggregator:
    """ TODO """ 
    def __init__(self,
                 metrics: List[Metric] = None):

        if metrics is None:
            metrics = []

        tags = []
        for metric in metrics:
            # Allow for a tag to be a list of tags.
            if isinstance(metric.tag, list):
                for each_tag in metric.tag:
                    if each_tag in tags: 
                        raise Exception("Metric with tag '{}' already exists".format(each_tag))
                    tags.append(each_tag) 
            else:
                if metric.tag in tags:
                    raise Exception("Metric with tag '{}' already exists".format(metric.tag))
                tags.append(metric.tag)

        self.tags = tags # The flattened list of tag strings.
        self.metrics = metrics
        self.results = []

    def add_metric(self, metric: Metric):
        """TODO"""

        if metric in self.metrics:
            # TODO custom exception
            raise Exception("Metric with tag '{}' already exists".format(metric.tag))

        self.metrics.append(metric)

    def remove_metric(self, metric: Metric):
        """TODO"""
        self.metrics.remove(metric)

    def calculate(self,
                  timestamp: datetime,
                  **kwargs):
        #TODO 
        d = {"timestamp": timestamp}
        for metric in self.metrics:
            calculation = metric.calculate(timestamp, **kwargs)
            # If a calculation is returned, at least one metric exists.
            if calculation is not None:
                if isinstance(metric.tag, list):
                    for i in range(len(metric.tag)):
                        d[metric.tag[i]] = calculation[i]
                else:
                    d[metric.tag] = calculation

        self.results.append(d)
        return d

    def write_to_file(self, output_filename):
        #TODO 
        df = pd.DataFrame(self.results, columns=["timestamp"] + self.tags)
        df.to_csv(output_filename, index=False)
