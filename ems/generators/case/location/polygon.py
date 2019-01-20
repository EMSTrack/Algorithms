import random
from typing import List

import numpy as np
from geopy import Point

from shapely import geometry
from shapely.ops import triangulate

from ems.generators.case.location.location import LocationGenerator


class PolygonLocationGenerator(LocationGenerator):

    def __init__(self,
                 vertices_latitude: List[float],
                 vertices_longitude: List[float]):

        self.vertices_latitude = vertices_latitude
        self.vertices_longitude = vertices_longitude
        self.polygon = geometry.Polygon([(latitude, longitude) for latitude, longitude in
                                         zip(vertices_latitude, vertices_longitude)])

    def generate(self, timestamp):
        triangles = triangulate(self.polygon)
        areas = [triangle.area for triangle in triangles]
        areas_normalized = [triangle.area / sum(areas) for triangle in triangles]

        t = np.random.choice(triangles, p=areas_normalized)
        a, b = sorted([random.random(), random.random()])

        coords = t.exterior.coords
        return Point(longitude=a * coords[0][0] + (b - a) * coords[1][0] + (1 - b) * coords[2][0],
                     latitude=a * coords[0][1] + (b - a) * coords[1][1] + (1 - b) * coords[2][1])
