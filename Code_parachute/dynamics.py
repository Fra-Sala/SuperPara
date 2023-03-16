from constants import *
from pyatmos import coesa76
import numpy as np
from parachute import Parachute
from rocket import Rocket
from scipy.integrate import solve_ivp
from model import model

class DynamicsReentry:

    def __init__(self, final_time, x0, z0, vx0, vz0, drogue_obj, rocket_obj):
        """Constructor of object DynamicsReentry. The reentry of the rocket is modelled as a 2D
            motion (planar), described by the x-z plane. The equation of motion are:
            \begin{cases}


            \end{cases}

            The members are:
            t_vect: numpy array of the discretized times
            x_vect: numpy array of the x-positioin"""
        self.t_vect = np.linspace(0, final_time, int(1e4))
        self.z_vect = [z0, ]
        self.x_vect = [x0]
        self.vx_vect = [vx0, ]
        self.vz_vect = [vz0, ]
        self.drogue = drogue_obj  # drogue_parachute is an object of the class Drogue
        self.rocket = rocket_obj
        self.az_vect = []
        self.ax_vect = []
        self.g_vect = []


    def solve_dynamics(self, ):
        y0 = [self.z_vect[0], self.vz_vect[0], self.x_vect[0], self.vx_vect[0]]

        def hit_ground(t,y, arg1, arg2):

            return y[0]


        hit_ground.terminal = True


        result = solve_ivp(model, [self.t_vect[0], self.t_vect[-1]], y0, events=hit_ground, args=(self.drogue, self.rocket), method='LSODA', first_step = 0.01, max_step = 0.02)
        self.t_vect = result.t
        self.z_vect = result.y[0,:]
        self.vz_vect = result.y[1,:]
        self.x_vect = result.y[2,:]
        self.vx_vect = result.y[3,:]
        self.az_vect = (self.vz_vect[1:] - self.vz_vect[0:-1]) / (self.t_vect[1] - self.t_vect[0]) #approzimation of the acceleration
        self.ax_vect= (self.vx_vect[1:] - self.vx_vect[0:-1]) / (self.t_vect[1] - self.t_vect[0])
        self.g_vect = -self.az_vect/GRAVITY

