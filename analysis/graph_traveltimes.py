import pandas
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from functools import reduce
import numpy as np
from sys import argv
# results_path = "results/Experimenting with Original Dibene Setup/"

def graph(results_path):

	contents = pandas.read_csv(results_path + "processed_cases.csv")

	# times = np.array([[pandas.to_timedelta(td).total_seconds()/60 for td in contents.values[i][7:12]] for i in range(len(contents.values))])

	# Only the to incident
	times = np.array([[pandas.to_timedelta(td).total_seconds()/60 for td in [contents.values[i][7]]] for i in range(len(contents.values))])


	case_durations = [reduce(lambda a, b: a + b, p, 0.0) for p in times]

	plt.figure(results_path + "Case Durations in Minutes")
	plt.ylim(-5, 45)
	plt.plot(case_durations, 'o')
	plt.plot([0, len(case_durations)], [10, 10], 'r-')
	plt.show()

def main():
	results_path = ["results/{}/".format(name) for name in argv[1:]]
	# print (results_path)
	for path in results_path:
		graph(path)
main()