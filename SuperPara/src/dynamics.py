from constants import *
from pyatmos import coesa76
import numpy as np
from scipy.integrate import solve_ivp
from model import model


class DynamicsReentry:

    def __init__(self, final_time, x0, z0, vx0, vz0, mainpara_obj, drogue_obj, rocket_obj):
        """
            Constructor of object DynamicsReentry.

            :param final_time: Final time for the simulation.
            :param x0: Initial x-coordinate of the rocket.
            :param z0: Initial z-coordinate of the rocket.
            :param vx0: Initial velocity in the x-direction.
            :param vz0: Initial velocity in the z-direction.
            :param mainpara_obj: Object of the class MainPara representing main parachute parameters.
            :param drogue_obj: Object of the class Drogue representing drogue parachute parameters.
            :param rocket_obj: Object of the class Rocket representing rocket parameters.
        """
        self.t_vect = np.linspace(0, final_time, int(1e4))
        self.z_vect = [z0, ]
        self.x_vect = [x0]
        self.vx_vect = [vx0, ]
        self.vz_vect = [vz0, ]
        self.drogue = drogue_obj  # drogue_parachute is an object of the class Drogue
        self.rocket = rocket_obj
        self.mainpara = mainpara_obj
        self.az_vect = []
        self.ax_vect = []
        self.g_vect = []
        self.mach_vect = []

    def solve_dynamics(self, ):
        """
            Solve the dynamics of the rocket during reentry.
        """

        y0 = [self.z_vect[0], self.vz_vect[0], self.x_vect[0], self.vx_vect[0]]

        def hit_ground(t, y, arg1, arg2, arg3):
            return y[0]

        hit_ground.terminal = True

        result = solve_ivp(model, [self.t_vect[0], self.t_vect[-1]], y0, events=hit_ground,
                           args=(self.mainpara, self.drogue, self.rocket), method='LSODA', first_step=0.01, max_step=0.015)
        self.t_vect = result.t
        self.z_vect = result.y[0, :]
        self.vz_vect = result.y[1, :]
        self.x_vect = result.y[2, :]
        self.vx_vect = result.y[3, :]

        self.az_vect = np.zeros_like(self.vz_vect)
        self.ax_vect = np.zeros_like(self.vx_vect)

        # 2nd order accuracy approximation of the derivative of the velocity (accelaration)
        self.az_vect[0] = (-3 * self.vz_vect[0] + 4 * self.vz_vect[1] - self.vz_vect[2]) / (
            (self.t_vect[2] - self.t_vect[0]))
        self.ax_vect[0] = (-3 * self.vx_vect[0] + 4 * self.vx_vect[1] - self.vx_vect[2]) / (
            (self.t_vect[2] - self.t_vect[0]))
        self.az_vect[1:-1] = (self.vz_vect[2:] - self.vz_vect[0:-2]) / (
                self.t_vect[2:] - self.t_vect[0:-2])  # approximation of the acceleration
        self.ax_vect[1:-1] = (self.vx_vect[2:] - self.vx_vect[0:-2]) / (self.t_vect[2:] - self.t_vect[0:-2])

        self.az_vect[-1] = (3 * self.vz_vect[-1] - 4 * self.vz_vect[-2] + self.vz_vect[-3]) / (
                    self.t_vect[-1] - self.t_vect[-3])
        self.ax_vect[-1] = (3 * self.vx_vect[-1] - 4 * self.vx_vect[-2] + self.vx_vect[-3]) / (
                    self.t_vect[-1] - self.t_vect[-3])

        # 1st order accuracy
        # self.az_vect[0:-1] = (self.vz_vect[1:] - self.vz_vect[0:-1]) /  (self.t_vect[1:] - self.t_vect[0:-1])
        # self.ax_vect[0:-1] = (self.vx_vect[1:] - self.vx_vect[0:-1]) / (self.t_vect[1:] - self.t_vect[0:-1])
        # self.az_vect[-1] = self.az_vect[-2]
        # self.ax_vect[-1] = self.ax_vect[-2]

        self.g_vect = self.az_vect / GRAVITY
        self.mach_vect = np.sqrt(self.vx_vect[0:] ** 2 + self.vz_vect[0:] ** 2) / np.sqrt(
            (GAMMA * R_AIR * coesa76(self.z_vect / 1000).T))
