from parachute import Parachute
from pyatmos import coesa76
import numpy as np

class Hemisflo(Parachute):
    """Class Hemisflo. It contains all the parameters that characterize the preliminary design of the hemisflo drouge parachute"""

    def __init__(self, z_deploy, x1_factor = 0.95, cx_factor = 1.25):
        # default values for the factors are taken from Knacke's book
        cd0_parachute = 0.35
        type_str = "hemisflo"
        Parachute.__init__(self,cd0_parachute, z_deploy, x1_factor, cx_factor, type_str)

    def compute_cd(self, mach):

        """ This function returns a plausible value of the drag coefficient for a hemisflo parachute
                operating at M >> 0.3 (compressibility effects not negligible). The implemented law
                 is taken from the plot in "Parachute recovery systems design manual", Section 5"""

        if mach < 1.9:
            self.cd = 0.35
        else:
            self.cd = -1 / 9 * mach + 0.561  # data from Pepper 1986

    def compute_delta_t_infl(self, v):
        """
        This method overrides mother-method. It computes the delta time for the
        inflation of a ribbon parachute. The used empirical formula depends
        on the type of parachute. See Knacke's book page 5-42 for details.
        :param v: current velocity [m/s]


        """
        self.delta_t_infl = 0.65*self.lambda_t*2*np.sqrt(self.surface/(4*np.pi))/np.abs(v)

    def compute_dragArea_chute(self, t, z, v, mach):
        """

        :param t: current instant of time [s]
        :param z: current altitude [m]
        :param v: current velocity [m/s]
        :param mach: current Mach number
        """
        self.compute_cd(mach)

        if z <= self.z_deploy:  # if we have reached the altitude of deployment

            if self.flag_infl == 0:
                # If the inflation has not occurred yet, then it is taking place at this precise instant t
                self.flag_infl = 1
                self.t_infl = t
                print("The inflation of the hemisflo takes place at v = %.2f, mach = %,2f", v, mach)
                self.compute_delta_t_infl(v)
                self.compute_opening_load(z,v)
                self.slope_infl = (self.cd) * (self.surface) / self.delta_t_infl

            if (t - self.t_infl) <= self.delta_t_infl:  # if the chute is inflating
                self.drag_area = self.slope_infl * (t - self.t_infl)
            else:
                self.drag_area = self.cd * self.surface


