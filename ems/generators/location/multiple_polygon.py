from numpy.random import choice
from typing import List
import yaml

from geopy import Point

from ems.generators.location.location import LocationGenerator
from ems.generators.location.polygon import PolygonLocationGenerator


class MultiPolygonLocationGenerator(LocationGenerator):
    """
    A region is divided into a set of regions so that the region can simulate certain zones
    having more cases occurring than others.
    """
    def __init__(self,
                 each_polygons_longitudes: List[List[float]] = None,
                 each_polygons_latitudes: List[List[float]] = None,
                 longitudes_file: str = None,
                 latitudes_file: str = None,
                 densities: List[float] = None):
        """
        Asserts correct assumptions about multi-polygon, like sum(probabilities) = 100 %
        :param polygons: Set of polygons denoted as a list of list of points.
        :param densities: The probability for each polygon respectively to each polygon.
        """

        if not any([each_polygons_latitudes and each_polygons_longitudes, longitudes_file and latitudes_file]):
            raise Exception("Either pass in the lats and lons as list of list of floats or as file names")

        if not each_polygons_longitudes:
            with open(longitudes_file, 'r') as lons_file:
                each_polygons_longitudes = yaml.load(lons_file)

        if not each_polygons_latitudes:
            with open(latitudes_file, 'r') as lats_file:
                each_polygons_latitudes = yaml.load(lats_file)

        # Check all the assumptions in the beginning of the function.
        assert len(each_polygons_longitudes) == len(each_polygons_latitudes)
        for i in range(len(each_polygons_longitudes)):
            assert len(each_polygons_longitudes[i]) == len(each_polygons_latitudes[i])
            for f in each_polygons_longitudes[i]:
                assert isinstance(f, float)
            for f in each_polygons_latitudes[i]:
                assert isinstance(f, float)


        if densities is None:
            self.densities = [1 / len(each_polygons_longitudes) for _ in each_polygons_longitudes]

        else:
            assert(sum(densities) == 1.0) # Sum of probabilities should add up to 100%
            assert len(densities) == len(each_polygons_longitudes)

            self.densities = densities

        # self.polygon_generators = self.create_generators(each_polygons_longitudes, each_polygons_latitudes)
        self.polygon_generators = [PolygonLocationGenerator(each_polygons_longitudes[i], each_polygons_latitudes[i])
                                   for i in range(len(each_polygons_longitudes))]


    def generate(self, timestamp=None):
        """
        Choose a polygon based on the probability distribution.

        :param timestamp: The time at which this case starts
        :return:
        """
        generator = choice(self.polygon_generators, 1, p=self.densities)[0]
        return generator.generate(timestamp)


    @staticmethod # Why is this a static method?
    def create_generators(list_lons, list_lats):
        """
        One uniform distribution random location generator per region.

        :param polygons:
        :return:
        """
        return
        # polygon_generators = []
        # for points in polygons:
        #     polygon_generator = PolygonLocationGenerator(points)
        #     polygon_generators.append(polygon_generator)
        # return polygon_generators
