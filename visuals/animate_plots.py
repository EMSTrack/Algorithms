import matplotlib.pyplot as plt
import matplotlib.animation as animation

import random

from IPython import embed  # TODO remove later


class Animator:
    def __init__(self,
                 start_time,
                 end_time,
                 ambulance_locations,
                 bases,
                 hospitals,
                 ambulance_trips):

        time_delta = (end_time - start_time)
        duration = round(time_delta.seconds / 60) + time_delta.days * 24 * 60
        frames = [[[[], []] for _ in range(len(ambulance_locations))] for _ in range(duration)]

        self.ambulance_locations = ambulance_locations  # This is actually a bit of a misnomer.
        self.bases = bases
        self.hospitals = hospitals

        event_count = 0

        for ambulance in ambulance_trips:
            for trip in ambulance:
                ambulance_id = trip.ambulance_id
                for event in trip.events:
                    index_start = round((event.starting_time - start_time).seconds / 60)
                    xs = [point.longitude for point in event.dots]
                    ys = [point.latitude for point in event.dots]
                    self.set_frames(frames, index_start, ambulance_id, xs, ys)

                    event_count += 1

        for curr_index in range(len(frames)):
            for ambulance_id in range(len(ambulance_locations)):
                # If no position was specified, then it is at base and stationary.
                if not frames[curr_index][ambulance_id][0]:
                    frames[curr_index][ambulance_id][0] += [self.ambulance_locations[ambulance_id].longitude] * 2
                    frames[curr_index][ambulance_id][1] += [self.ambulance_locations[ambulance_id].latitude] * 2
        self.frames = frames
        self.duration = duration

        # Random color generator
        r = lambda: random.randint(0, 226)
        self.ambulance_colors = ['#%02X%02X%02X' % (r(), r(), r()) for _ in range(len(ambulance_locations))]

        if True:
            print('frames: {}\nambs: {}\nevents: {}\n'.format(
                len(self.frames), len(ambulance_locations), event_count
            ))

    def set_frames(self, frames, index_start, ambulance_id, xs, ys, display=10):
        """
        Take the coordinates from the events and enumerate them frame by frame.
        The [display] most recent coordinates are used.
        :param frames:
        :param index_start:
        :param ambulance_id:
        :param xs:
        :param ys:
        :param display:
        :return:
        """

        if not xs: return

        curr_index = index_start
        start_position = 0
        end_position = 1
        last_position = len(xs)

        # Enumerate the historically most recent coordinates.
        while start_position < end_position:

            frames[curr_index][ambulance_id][0] += xs[start_position: end_position]
            frames[curr_index][ambulance_id][1] += ys[start_position: end_position]

            if end_position < last_position:
                end_position += 1

            if end_position - start_position > display or end_position == last_position:
                start_position += 1

            curr_index += 1

    def run_animation(self):
        """ Define a new update function and use it as the update function
         for the matplotlib.  """

        def _get_frame(frame_index, plots):
            """ Should be called by run_animations only. """

            # TODO Using the indices of the self.frames, plot in correct location.
            # Okay right now there is a problem where it's unknown whether the set of coordinates
            # is a line or a dot -- that info got lost up there

            for amb_index in range(len(self.frames[frame_index])):
                xs = self.frames[frame_index][amb_index][0]
                ys = self.frames[frame_index][amb_index][1]

                # if len(xs) > 1:
                #     if xs[0] == xs[1]:
                #         plots[amb_index][1].set_data([xs[0]], [ys[0]])
                #     if xs[-2] == xs[-1]:
                #         plots[amb_index][1].set_data([xs[-1]], [ys[-1]])

                plots[amb_index][0].set_data(xs, ys)

            print(plots[len(self.ambulance_locations)])

            return plots,

        fig = plt.figure(figsize=(14, 8))

        # TODO need [number of ambulances] x [number of states]

        plots = []
        for i in range(len(self.ambulance_locations)):
            new_color = self.ambulance_colors[i]

            line_plot, = plt.plot([], [],
                                  marker='+',
                                  linestyle='',
                                  markerfacecolor=new_color,
                                  markeredgecolor=new_color,
                                  label="Ambulance {} Path".format(i + 1))

            # dot_plot, = plt.plot([], [],
            #                      marker='o',
            #                      linestyle='',
            #                      markerfacecolor=new_color,
            #                      markeredgecolor=new_color)

            # plots.append([line_plot, dot_plot])

            plots.append([line_plot])

        base_plot = plt.scatter([base.longitude for base in self.bases],
                                [base.latitude for base in self.bases],
                                marker="D", color="black", label="Bases")
        hospital_plot = plt.scatter([hospital.longitude for hospital in self.hospitals],
                                    [hospital.latitude for hospital in self.hospitals],
                                    marker="P", color="r", label="Hospitals")

        plots.append(base_plot)
        plots.append(hospital_plot)

        # TODO Make boundaries parameters

        img = plt.imread("./visuals/simple.png")
        plt.imshow(img, extent=[-117.017637, -117.167672, 32.710484, 32.823033])
        plt.legend(loc="upper right")
        print("draw the animation")
        ani = animation.FuncAnimation(fig, _get_frame, len(self.frames),
                                      fargs=(plots,), interval=50)

        plt.show()

        # fps = 15
        # print('save the animation')
        # print("it may take up to {}".format(len(self.frames)/fps))
        # ani.save('regional_vis6.mp4', fps=fps, dpi=150)
