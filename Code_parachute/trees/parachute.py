from abc import abstractmethod
from constants import *
from pyatmos import coesa76
import numpy as np
import pandas as pd

class Parachute:

    def __init__(self, cd0_parachute, z_deploy, x1_factor, cx_factor, type_string):

        """Constuctor for object Parachute"""
        self.drag_area = 0.0
        self.cd0 = cd0_parachute
        self.cd = 0.0
        self.t_infl = 0.0  # The following parameters describe the inflation process
        self.delta_t_infl = 1.0
        self.slope_infl = 1.0
        self.z_deploy = z_deploy
        self.lambda_t = 0.0  # total porosity. In Knacke's book there are plots with suggested values
        self.surface = 0.0
        self.flag_infl = 0  # it allows to check whether the inflation has taken place or not yet
        self.x1_factor = x1_factor   # default value based on reasonable value suggested by Kancke  (see 7.39)
        self.cx_factor = cx_factor   #  default value based on reasonable value suggested by Kancke (see 7.39)
        self.opening_force = 0.0
        self.type_chute = type_string  # store the name of the type of parachute (e.g. "hemisflo", "conical ribbon",)
        self.suspension_lines = 0.0
        self.D_0 = 0.0
        self.D_p = 0.0       # diameter after inflation
        self.h_s = 0.0      # gore height
    @abstractmethod
    def compute_cd(self, mach):
        pass

    @abstractmethod
    def compute_delta_t_infl(self, v):
        pass

    @abstractmethod
    def compute_dragArea_chute(self, t, z, v, mach):
        pass

    def compute_opening_load(self, z, v):
        """
        This method computes a likely value of the force at parachute deployment.
        The used formula is given by Knacke's book, see pages 5-53 5-54.
        The member *self.opening_force* is set accordingly.

        :param z : current altitude
        :param v : current velocity

        """
        rho = coesa76(z / 1000).rho
        self.opening_force = float(self.cd * self.surface * (
                    1 / 2 * rho * v**2) * self.cx_factor * self.x1_factor)


    def required_S0(self, val_max, mass, z, option):

        """
        This method computes the necessary nominal canopy area for both the main
        and the drogue parachute. For the main, given a desired final descent rate,
        we compute *self.surface* as shown in Knacke's book, page 7-37. For the drogue, we start
        from the Mach at which we want to deploy the main parachute, we then recover the corresponding
        velocity at the altitude for the deployment of the main, and hence we compute with the same
        procedure the value of *self.surface* for the drogue itself.

        :param val_max : either the final descent velocity that the main parachute must reach (option == 1)
        or the Mach number that the drogue chute must reach for the deployment of the main (option == 2)
        :param mass : mass of payload [kg]
        :param z : current altitude [m]
        :param option: int, 1 or 2
        """

        if option == 1: # in this case, val_max is the final descent velocity required (for the main parachute)
            CD_S0 = mass * GRAVITY / (0.5 * RHO_0 * val_max ** 2)
            self.surface = CD_S0 / self.cd0
        elif option == 2: # in this case val_max is the Mach number that the drogue must reach by deceleration
            rho = coesa76(z/1000).rho
            v = val_max * np.sqrt(GAMMA * R_AIR * coesa76(z/1000).T)
            CD_S0 = mass * GRAVITY / (0.5 * rho * v ** 2)
            self.surface = CD_S0/self.cd0
        else:
            print("Please enter a valid option (1 -> val_max = final descent velocity, 2->  val_max = desired Mach number")



    def compute_porosity(self, type_chute):
        """
        This function interpolates the plot 6-23 in Knacke's book to compute
        the required total porosity for a given application. The parameter *type_chute*
        selects the right curve from the plot, depending on the type of parachute employed.
        See table 6-3 in Knacke for details about different applications.
        It requires access to the directory Porosity_plot which contains the csv files of the digitised
        plot.

        :param type_chute: int. 2-> stabilization chute, 3-> drogue chute.
        """
        D0_feet = np.sqrt(4*self.surface/np.pi)*3.281  # [ft] D0 in feet
        if type_chute == 3: # drogue
            lambda_csv = np.loadtxt("./Porosity_plot/plot6_23_III.csv",  delimiter=",")
            self.lambda_t = np.interp(D0_feet, lambda_csv[:,0], lambda_csv[:,1])
        elif type_chute == 2:
            lambda_csv = np.loadtxt("./Porosity_plot/plot6_23_II.csv",  delimiter=",")
            self.lambda_t = np.interp(D0_feet, lambda_csv[:,0 ], lambda_csv[:,1])
