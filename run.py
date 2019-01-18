import argparse
from datetime import timedelta, datetime

import numpy as np
from geopy import Point

from ems.algorithms.hospital_selectors.select_fastest import FastestHospitalSelector
from ems.algorithms.selection.dispatch_fastest import BestTravelTimeAlgorithm
from ems.analysis.metrics.count_pending import CountPending
from ems.analysis.metrics.coverage.percent_coverage import PercentCoverage
from ems.analysis.metrics.coverage.radius_coverage import RadiusCoverage
from ems.analysis.metrics.metric_aggregator import MetricAggregator
from ems.analysis.metrics.total_delay import TotalDelay
from ems.datasets.ambulance.custom_ambulance_set import CustomAmbulanceSet
from ems.datasets.case.random_case_set import RandomCaseSet
from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.datasets.location.location_set import LocationSet
from ems.datasets.location.base.tijuana_base_set import TijuanaBaseSet
from ems.datasets.location.demand.tijuana_demand_set import TijuanaDemandSet
from ems.datasets.travel_times.tijuana_travel_times import TijuanaTravelTimes
from ems.generators.case.location.multiple_polygon import MultiPolygonLocationGenerator
from ems.generators.case.location.polygon import PolygonLocationGenerator
from ems.generators.case.time.poisson_time import PoissonCaseTimeGenerator
from ems.generators.event.duration.random_duration import RandomDurationGenerator
from ems.generators.event.duration.travel_time_duration import TravelTimeDurationGenerator
from ems.algorithms.base_selectors.round_robin_selector import RoundRobinBaseSelector
from ems.generators.event.event_generator import EventGenerator
from ems.settings import Settings
from ems.simulators.event_simulator import EventDispatcherSimulator

import os

os.system("python examples/simple.py --settings hans")