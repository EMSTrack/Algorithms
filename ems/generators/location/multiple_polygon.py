from numpy.random import choice
from typing import List

from geopy import Point

from ems.generators.location.location import LocationGenerator
from ems.generators.location.polygon import PolygonLocationGenerator


class MultiPolygonLocationGenerator(LocationGenerator):
    """
    A region is divided into a set of regions so that the region can simulate certain zones
    having more cases occurring than others.
    """
    def __init__(self,
                 polygons: List[List[Point]],
                 densities: List[float] = None):
        """
        Asserts correct assumptions about multi-polygon, like sum(probabilities) = 100 %
        :param polygons: Set of polygons denoted as a list of list of points.
        :param densities: The probability for each polygon respectively to each polygon.
        """
        if densities is None:
            self.densities = [1/len(polygons) for _ in polygons]

        else:
            if sum(densities) != 1:
                raise Exception('Densities do not sum to 1')

            elif len(densities) != len(polygons):
                raise Exception('Number of densities do not match number of polygons')

            else:
                self.densities = densities

        self.polygon_generators = self.create_generators(polygons)


    def generate(self, timestamp=None):
        """
        Choose a polygon based on the probability distribution.

        :param timestamp: The time at which this case starts
        :return:
        """
        generator = choice(self.polygon_generators, 1, p=self.densities)[0]
        return generator.generate(timestamp)


    @staticmethod # Why is this a static method?
    def create_generators(polygons):
        """
        One uniform distribution random location generator per region.

        :param polygons:
        :return:
        """
        polygon_generators = []
        for points in polygons:
            polygon_generator = PolygonLocationGenerator(points)
            polygon_generators.append(polygon_generator)
        return polygon_generators
