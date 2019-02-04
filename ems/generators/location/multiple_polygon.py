from numpy.random import choice
from typing import List

from geopy import Point

from ems.generators.location.location import LocationGenerator
from ems.generators.location import PolygonLocationGenerator


class MultiPolygonLocationGenerator(LocationGenerator):

    def __init__(self,
                 polygons: List[List[Point]],
                 densities: List[float] = None):

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

    def generate(self, timestamp):
        generator = choice(self.polygon_generators, 1, p=self.densities)[0]
        return generator.generate(timestamp)

    @staticmethod
    def create_generators(polygons):
        polygon_generators = []
        for points in polygons:
            polygon_generator = PolygonLocationGenerator(points)
            polygon_generators.append(polygon_generator)
        return polygon_generators
