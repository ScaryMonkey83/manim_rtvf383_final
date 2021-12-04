import logging
from math import sin, cos

import soundfile as sf
from manim import *
import numpy as np
from manim._config import config
from manim_music import frame_rate, file_to_var

logger = logging.getLogger(__name__)

# also constants
circumference = 3
multiplier = 3
rot_speed = 0.05

# constant lists
colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]
locs = [[-3 * circumference, 0 * circumference, 0],
        [-2 * circumference, 0 * circumference, 0],
        [-1 * circumference, 0 * circumference, 0],
        [0 * circumference, 0 * circumference, 0],
        [1 * circumference, 0 * circumference, 0],
        [2 * circumference, 0 * circumference, 0],
        [3 * circumference, 0 * circumference, 0]]


class Video(ThreeDScene):
    @staticmethod
    def getline(sphere1, sphere2):
        start_point = sphere1.get_center()
        end_point = sphere2.get_center()
        line = Line3D(
            start_point,
            end_point)
        return line

    def define_pyramid(self, color: color.Color, xyz: list):
        """This function defines a pyramid to be manipulated and returns"""
        sphere1 = Sphere().set_color(color).scale(0.2).move_to((1 + xyz[0]) * RIGHT + (1 + xyz[1]) * UP + (-2 + xyz[2]) * OUT)
        sphere2 = sphere1.copy().move_to((-1 + xyz[0]) * RIGHT + (1 + xyz[1]) * UP + (-2 + xyz[2]) * OUT)
        sphere3 = sphere1.copy().move_to((-1 + xyz[0]) * RIGHT + (-1 + xyz[1]) * UP + (-2 + xyz[2]) * OUT)
        sphere4 = sphere1.copy().move_to((1 + xyz[0]) * RIGHT + (-1 + xyz[1]) * UP + (-2 + xyz[2]) * OUT)
        sphere5 = sphere1.copy().move_to(xyz[0] * RIGHT + xyz[1] * UP + (-2 + xyz[2]) * OUT)
        sphere6 = sphere5.copy().set_opacity(0).scale(0.1).move_to(xyz[0] * RIGHT + xyz[1] * UP + (-2 + xyz[2]) * OUT)

        line1 = self.getline(sphere1, sphere2)
        line1.add_updater(lambda mob: mob.become(self.getline(sphere1, sphere2)))
        line2 = self.getline(sphere2, sphere3)
        line2.add_updater(lambda mob: mob.become(self.getline(sphere2, sphere3)))
        line3 = self.getline(sphere3, sphere4)
        line3.add_updater(lambda mob: mob.become(self.getline(sphere3, sphere4)))
        line4 = self.getline(sphere4, sphere1)
        line4.add_updater(lambda mob: mob.become(self.getline(sphere4, sphere1)))

        line5 = self.getline(sphere5, sphere1)
        line5.add_updater(lambda mob: mob.become(self.getline(sphere5, sphere1)))
        line6 = self.getline(sphere5, sphere2)
        line6.add_updater(lambda mob: mob.become(self.getline(sphere5, sphere2)))
        line7 = self.getline(sphere5, sphere3)
        line7.add_updater(lambda mob: mob.become(self.getline(sphere5, sphere3)))
        line8 = self.getline(sphere5, sphere4)
        line8.add_updater(lambda mob: mob.become(self.getline(sphere5, sphere4)))

        spheres = [sphere1, sphere2, sphere3, sphere4, sphere5, sphere6]
        lines = [line1, line2, line3, line4, line5, line6, line7, line8]

        [self.add(line) for line in lines]
        [self.add(sphere) for sphere in spheres]

        return spheres

    def construct(self):
        c = lambda deg: np.array([[cos(deg), -sin(deg), 0],
                                  [sin(deg), cos(deg), 0],
                                  [0, 0, 1]])

        def rotate(*points, rotation_mat=None, animate=True):
            assert rotation_mat is not None
            do = []
            if animate:
                for point in points:
                    do.append(point.animate.move_to(np.matmul(point.get_center, rotation_mat)))
            else:
                for point in points:
                    point.move_to(np.matmul(point.get_center, rotation_mat))
            return do

        def process_one(pyramids: List[List[Sphere]], drum, rand_func, play=True, inv=False):
            # cross product to get the perpendicular unit vector (for each track)
            cp0 = np.cross(pyramids[0][1].get_center() - pyramids[0][0].get_center(),
                           pyramids[0][3].get_center() - pyramids[0][0].get_center())
            cp1 = np.cross(pyramids[1][1].get_center() - pyramids[1][0].get_center(),
                           pyramids[1][3].get_center() - pyramids[1][0].get_center())
            cp2 = np.cross(pyramids[2][1].get_center() - pyramids[2][0].get_center(),
                           pyramids[2][3].get_center() - pyramids[2][0].get_center())
            cp3 = np.cross(pyramids[3][1].get_center() - pyramids[3][0].get_center(),
                           pyramids[3][3].get_center() - pyramids[3][0].get_center())
            cp4 = np.cross(pyramids[4][1].get_center() - pyramids[4][0].get_center(),
                           pyramids[4][3].get_center() - pyramids[4][0].get_center())
            cp5 = np.cross(pyramids[5][1].get_center() - pyramids[5][0].get_center(),
                           pyramids[5][3].get_center() - pyramids[5][0].get_center())
            cp6 = np.cross(pyramids[6][1].get_center() - pyramids[6][0].get_center(),
                           pyramids[6][3].get_center() - pyramids[6][0].get_center())

            # add the resulting unit vector to the center point on the base for each pyramid and animate it!
            loc1 = pyramids[0][5].get_center() + (cp0 / np.linalg.norm(cp0)) * multiplier * (-drum[0] if inv else drum[0])
            loc2 = pyramids[1][5].get_center() + (cp1 / np.linalg.norm(cp1)) * multiplier * (-drum[1] if inv else drum[1])
            loc3 = pyramids[2][5].get_center() + (cp2 / np.linalg.norm(cp2)) * multiplier * (-drum[2] if inv else drum[2])
            loc4 = pyramids[3][5].get_center() + (cp3 / np.linalg.norm(cp3)) * multiplier * (-drum[3] if inv else drum[3])
            loc5 = pyramids[4][5].get_center() + (cp4 / np.linalg.norm(cp4)) * multiplier * (-drum[4] if inv else drum[4])
            loc6 = pyramids[5][5].get_center() + (cp5 / np.linalg.norm(cp5)) * multiplier * (-drum[5] if inv else drum[5])
            loc7 = pyramids[6][5].get_center() + (cp6 / np.linalg.norm(cp6)) * multiplier * (-drum[6] if inv else drum[6])

            if play:
                return [
                    pyramids[0][4].animate.move_to(loc1),
                    pyramids[1][4].animate.move_to(loc2),
                    pyramids[2][4].animate.move_to(loc3),
                    pyramids[3][4].animate.move_to(loc4),
                    pyramids[4][4].animate.move_to(loc5),
                    pyramids[5][4].animate.move_to(loc6),
                    pyramids[6][4].animate.move_to(loc7)
                ]
            else:
                return loc1, loc2, loc3, loc4, loc5, loc6, loc7

        # load designated data
        drum_idx: int
        data: np.ndarray
        drum_idx, data = file_to_var(config.music_file)

        # init scene data
        light = self.camera.light_source
        light.move_to([-25, -20, 20])

        # introduction
        if config.first:
            self.set_camera_orientation(0, 0, zoom=4)
            pyramids1 = [self.define_pyramid(col, loc) for (col, loc) in zip(colors, locs)]
            pyramids2 = [self.define_pyramid(col, loc + 4 * OUT) for (col, loc) in zip(colors, locs)]
            self.wait(4)
            self.move_camera(0.45 * np.pi, -0.1 * np.pi, zoom=0.6)
        else:
            # if not the first chunk, run it like this
            self.set_camera_orientation(0.45 * np.pi, -0.1 * np.pi, zoom=0.6)
            pyramids1 = [self.define_pyramid(col, loc) for (col, loc) in zip(colors, locs)]
            pyramids2 = [self.define_pyramid(col, loc + 4 * OUT) for (col, loc) in zip(colors, locs)]
            v0_1, v1_1, v2_1, v3_1, v4_1, v5_1, v6_1 = process_one(pyramids1, data[0, :], None, play=False)
            v0_2, v1_2, v2_2, v3_2, v4_2, v5_2, v6_2 = process_one(pyramids2, data[0, :], None, play=False, inv=True)
            data = data[1:, :]

            pyramids1[0][4].move_to(v0_1)
            pyramids1[1][4].move_to(v1_1)
            pyramids1[2][4].move_to(v2_1)
            pyramids1[3][4].move_to(v3_1)
            pyramids1[4][4].move_to(v4_1)
            pyramids1[5][4].move_to(v5_1)
            pyramids1[6][4].move_to(v6_1)

            pyramids2[0][4].move_to(v0_2)
            pyramids2[1][4].move_to(v1_2)
            pyramids2[2][4].move_to(v2_2)
            pyramids2[3][4].move_to(v3_2)
            pyramids2[4][4].move_to(v4_2)
            pyramids2[5][4].move_to(v5_2)
            pyramids2[6][4].move_to(v6_2)

        # main loop
        all_the_points = []
        [[all_the_points.append(point) for point in pyramid] for pyramid in pyramids1]
        [[all_the_points.append(point) for point in pyramid] for pyramid in pyramids2]
        if not config.first:
            rotate(*all_the_points, rotation_mat=c(rot_speed * drum_idx), animate=False)

        for sample in range(data.shape[0]):
            # sample = sample + int(2 * data.shape[0] / 3)
            d = data[sample, :]
            p1 = process_one(pyramids1, d, None)
            p2 = process_one(pyramids2, d, None, inv=True)
            p3 = rotate(*all_the_points, rotation_mat=c(rot_speed))
            self.play(
                *p1,
                *p2,
                *p3,
                run_time=1 / frame_rate,
                rate_func=rate_functions.linear
            )
