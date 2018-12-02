import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from geopy import Point

class Path:
    """ This class will make possible the ability to determine velocity. """

    def __init__(self, start, end, pieces=100, display=10):
        """
        A path is defined by their endpoints.
        :param start:
        :param end:
        :param pieces:
        :param display:
        """
        assert type(start) == Point
        assert type(end) == Point
        assert isinstance(pieces, int)
        assert isinstance(display, int)

        d_lon = (end.longitude - start.longitude) / pieces
        d_lat = (end.latitude - start.latitude) / pieces

        self.points = [ Point(

            start.latitude + m * d_lat,
            start.longitude + m * d_lon
            )
            for m in range(0, pieces)
        ]

        self.position = 0
        self.length = 1
        self.display = display


    def __str__(self):
        return "[{}]".format("\n".join([str(p.longitude) + " " + str(p.latitude) for p in self.points]))


    def display_points(self):

        start_pos = self.position
        end_pos = self.position + self.length

        if end_pos > len(self.points):
            end_pos = len(self.points)

        disp_points = self.points[start_pos: end_pos]

        # Grow the line or increase the start
        if self.length < self.display:
            self.length += 1
        else:
            self.position += 1

        return disp_points

def update_line(num, line, path):
    # unpack_me = [[p.longitude, p.latitude] for p in path.display_points()]
    ps = path.display_points()
    xs = [p.longitude for p in ps]
    ys = [p.latitude for p in ps]
    # if len(unpack_me) == 1:
    #     unpack_me = unpack_me[0]
    # print(unpack_me)
    line.set_data(
        [xs, ys]
    )

def main():

    p3 = Path(Point(0, 0), Point(1, 1), pieces=50, display=5)

    fig1 = plt.figure()

    # data = np.random.rand(2, 25)
    line, = plt.plot([], [], 'b-')
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    line_ani = ani.FuncAnimation(
        fig1,
        update_line,
        2000,
        # 0,
        fargs=(line, p3),
        interval = 100,
        blit=False
    )

    # To save the animation, use the command: line_ani.save('lines.mp4')
    # line_ani.save('line.mp4', fps=30)
    plt.show()


if __name__ == "__main__":
    main()