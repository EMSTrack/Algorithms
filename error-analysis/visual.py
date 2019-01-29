#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import yaml
from IPython import embed

test_figs = False

def test():
	t1 = np.arange(0.0, 5.0, 0.1)
	t2 = np.arange(0.0, 5.0, 0.02)

	plt.plot(np.cos(2 * np.pi * t2), 'r--')
	plt.plot(np.sin(2 * np.pi * t2), 'b+')

def read_data(filename):
	with open(filename) as input_yaml:
		return yaml.load(input_yaml.read())

def preconfigurations():
	# plt.xlim(0, 75)
	# plt.ylim(-1, 1)
	img = plt.imread("tijuana.png")
	plt.figure(figsize=(10, 8))
	plt.imshow(img, extent=[-117.124533, -116.804590, 32.405490, 32.563261])
	pass

def set_polygon(coordinates):
	ys = coordinates['latitude']
	xs = coordinates['longitude']

	xs.append(xs[0])
	ys.append(ys[0])

	plt.plot(xs, ys, 'black')

def set_points(coordinates, label, style='b'):
	""" Use with real points as well as sim points"""
	ys = coordinates['latitude']
	xs = coordinates['longitude']

	plt.plot(xs, ys, style, label=label)



def main():

	if test_figs: test()

	data = read_data('./error-coordinates.yaml')

	preconfigurations()									# Rectangle, xlim, name, etc
	set_polygon(data['polygon'])						# Read the polygon coordinates into the vis

	set_points(data['incident_locs'], "Incidents",  style="bo")
	set_points(data['sim_locs'], "Travel Time Points", style="ro")
	set_points(data["hospital_locs"], "Hospitals", style="go")
	set_points(data["base_locs"], "Bases", style="yo")

	plt.legend(loc="upper right")
	plt.show()							# Go.

if __name__ == "__main__" : 
	main()