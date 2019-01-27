#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import numpy as np

test_figs = True

def test():
	t1 = np.arange(0.0, 5.0, 0.1)
	t2 = np.arange(0.0, 5.0, 0.02)

	plt.plot(np.cos(2 * np.pi * t2), 'r--')
	plt.plot(np.sin(2 * np.pi * t2), 'b+')

def preconfigurations():
	plt.xlim(0, 75)
	plt.ylim(-1, 1)


def set_polygon(filename):
	pass

def set_points(filename, color='b'):
	""" Use with real points as well as sim points"""
	pass


def main():

	if test_figs: test()

	preconfigurations()					# Rectangle, xlim, name, etc
	set_polygon("")						# Read the polygon coordinates into the vis
	set_points("", color="yo")			# Read the simulator points
	set_points("", color="ro")			# Read the generated points (real)

	plt.show()							# Go.

if __name__ == "__main__" : 
	main()