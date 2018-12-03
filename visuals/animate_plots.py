import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np

from IPython import embed # TODO remove later

class Animator:
    def __init__(self, start_time, end_time, ambulance_bases, ambulance_trips):

        time_delta = (end_time - start_time)
        duration = round(time_delta.seconds / 60) + time_delta.days * 24 * 60
        frames = [[[[],[]] for _ in range(len(ambulance_bases))] for _ in range(duration)]

        for ambulance in ambulance_trips:
            for trip in ambulance:
                ambulance_id = trip.ambulance_id
                for event in trip.events:
                    index_start = round((event.starting_time - start_time).seconds/60)
                    xs = [point.longitude for point in event.dots]
                    ys = [point.latitude for point in event.dots]
                    self.set_frames(frames, index_start, ambulance_id, xs, ys)
                    # print(index_start, ambulance_id, xs, ys)

        self.frames = frames
        self.duration = duration
        self.ambulance_bases = ambulance_bases

    def set_frames(self, frames, index_start, ambulance_id, xs, ys, display=5):

        if not xs: return

        curr_index = index_start
        start_position = 0
        end_position = 1
        last_position = len(xs) - 1


        while start_position < end_position:
            # from IPython import embed; embed()
            # TODO something is wrong with the way I'm enumerating this.
            # TODO starting with one case.
            print(curr_index, ambulance_id)
            print(start_position, end_position)
            print(len(frames))
            print()
            frames[curr_index][ambulance_id][0] += xs[start_position: end_position]
            frames[curr_index][ambulance_id][1] += ys[start_position: end_position]

            if end_position < last_position:
                end_position += 1
            if end_position - start_position > display or end_position == last_position:
                start_position += 1

            curr_index += 1
            # embed()



    def run_animation(self):

        def _get_frame(index, plot):
            """ Should be called by run_animations only. """

            # TODO for now all the ambulances are the same color
            # [amb for amb in self.frames[index]]
            xs = [amb[0] for amb in self.frames[index]]
            ys = [amb[1] for amb in self.frames[index]]
            accum_x = []
            accum_y = []
            for x in xs:
                accum_x += x
            for y in ys:
                accum_y += y
            # print("Do I at least get here?")
            # d = np.array([xs, ys])
            plot.set_data(accum_x, accum_y)
            # embed()
            # plot.set_data(d)
            return plot,


        fig = plt.figure()
        plot, = plt.plot([], [], 'b+')
        plt.xlim(-117.173017, -116.744906)
        plt.ylim(32.367460, 32.619161)
        print("do I get here?")
        ani = animation.FuncAnimation(fig, _get_frame, len(self.frames),
                                      fargs=(plot,), interval=50)
        # plt.show()
        ani.save('regional_vis.mp4', fps=15)

