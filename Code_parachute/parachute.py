import numpy as np
from pyatmos import coesa76
from constants import *
from abc import abstractmethod


class Parachute:

    def __init__(self, cd0_parachute, z_deploy, s_chute, lambda_t, x1_factor, cx_factor):

        """Constuctor for object Parachute"""
        self.drag_area = 0.0
        self.cd0 = cd0_parachute
        self.cd = 0.0
        self.t_infl = 0.0  # The following parameters describe the inflation process
        self.delta_t_infl = 1.0
        self.slope_infl = 1.0
        self.z_deploy = z_deploy
        self.lambda_t = lambda_t  # total porosity. In Knacke's book there are plots with suggested values
        self.surface = s_chute
        self.flag_infl = 0  # it allows to check whether the inflation has taken place or not yet
        self.x1_factor = x1_factor   # default value based on reasonable value suggested by Kancke  (see 7.39)
        self.cx_factor = cx_factor   #  default value based on reasonable value suggested by Kancke (see 7.39)
        self.opening_force = 0.0

    @abstractmethod
    def compute_cd(self, mach):
        pass

    @abstractmethod
    def compute_delta_t_infl(self, v):
        pass

    @abstractmethod
    def compute_dragArea_chute(self, t, z, v, mach):
        pass

    @abstractmethod
    def compute_opening_load(self, t, z, v, mach):
        pass

