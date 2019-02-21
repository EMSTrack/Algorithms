import pandas
import matplotlib.pyplot as plt
from datetime import datetime
from sys import argv


def graph(results_path):
	contents = pandas.read_csv(results_path + "metrics.csv")

	pairs = [pair.replace("(", "").replace(")", "").split(',') for pair in contents['percent_coverage']]
	pairs = [(float(pair[0]), float(pair[1])) for pair in pairs]
	primary = [pair[0] for pair in pairs]
	secondary = [pair[1] for pair in pairs]

	datetimes = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f") for d in contents['timestamp']]
	primaries = [(datetimes[i], primary[i]) for i in range(len(datetimes))]
	secondaries = [(datetimes[i], secondary[i]) for i in range(len(datetimes))]

	primaries.sort()
	secondaries.sort()



	plt.figure(results_path + "Primary Coverage")
	plt.ylim(-5, 80)
	plt.plot([pair[0] for pair in primaries], [pair[1] for pair in primaries], 'b-')
	plt.plot([pair[0] for pair in primaries], [pair[1] for pair in primaries], 'bo')

	plt.figure(results_path + 'Secondary Coverage')
	plt.ylim(-5, 80)
	plt.plot([pair[0] for pair in secondaries], [pair[1] for pair in secondaries], 'r-')
	plt.plot([pair[0] for pair in secondaries], [pair[1] for pair in secondaries], 'ro')

	plt.figure(results_path + 'Coverages Overlayed')
	plt.ylim(-5, 80)
	plt.plot([pair[0] for pair in secondaries], [pair[1] for pair in secondaries], 'ro')
	plt.plot([pair[0] for pair in primaries], [pair[1] for pair in primaries], 'bo')
	plt.plot([pair[0] for pair in secondaries], [pair[1] for pair in secondaries], 'r-')
	plt.plot([pair[0] for pair in primaries], [pair[1] for pair in primaries], 'b-')

	plt.show()

def main():
	results_path = ["results/{}/".format(name) for name in argv[1:]]
	for path in results_path:
		graph(path)
main()