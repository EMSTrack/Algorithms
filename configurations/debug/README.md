# New kind of error. 


Two scenarios as seen in `debug-disaster.yaml`. Both have interval of 3 hours but 
the simulator can't seem to determine the scenario.

```
================================================================================
Current Time: 2019-03-22 05:22:33.561031
Processing ongoing case: 37
Finished event: Dropping off Patient at Hospital
Started new event: Returning to Base
Destination: 32.50691, -116.964
Duration: 0:05:48
Distance Difference: 2.59%
Busy ambulances: ['0', '1', '10', '11', '2', '3', '4', '5', '6', '7', '8', '9']
Ongoing cases: [38, 40, 32, 42, 41, 37, 39, 33, 29, 35, 36, 34]
Pending cases: [43, 44, 45]

Metrics
timestamp: 2019-03-22 05:22:33.561031
primary_coverage: 0.0
secondary_coverage: 0.0
total_delay: 1:20:25.019716
count_pending: 3
================================================================================
Current Time: 2019-03-22 05:24:01.519173
New case arrived but no available ambulance; Case pending
Traceback (most recent call last):
  File "./run-simulation", line 59, in <module>
    case_record_set, metric_aggregator = sim.run()
  File "/Users/vectflux/ReEMS/Algorithms/ems/simulators/event_simulator.py", line 99, in run
    next_case = next(case_iterator, None)
  File "/Users/vectflux/ReEMS/Algorithms/ems/datasets/case/scenario_case_set.py", line 59, in iterator
    next_scenario, next_time = self.scenario_controller.retrieve_next_scenario(new_case.date_recorded)
  File "/Users/vectflux/ReEMS/Algorithms/ems/scenarios/scenario_controller.py", line 111, in retrieve_next_scenario
    raise Exception("No scenario can be chosen")
Exception: No scenario can be chosen
```