# Experiment

Run the simulator under varying circumstances and policies to produce different scenarios.

## Determine the average rate of emergencies

Using the calls CSV, calculate how rapidly the cases occur depend on the time of day. 
This will create a set of scenarios. Since the simulator is not affected by the time of day,
and is only affected by this average rate for the Poisson distribution, we really only need 
the average rate.

## Run them all!

For each rate at which cases occur, run the different policies (1 best time, 2 least disruption, 
3 a mixture of both.)

This will result in 9 different results: 3 scenarios x 3 policies.