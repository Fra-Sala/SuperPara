from parachute import Parachute
from pyatmos import coesa76
import numpy as np


class ConicalRibbon(Parachute):
    """Class ConicalRibbon (i.e. main parachute). It contains all the parameters that characterize the main parachute.
        This allows to properly estimate when to deploy the drogue parachute"""

    def __init__(self, z_deploy, x1_factor=0.9, cx_factor=1.05):
        # default values for the factors are taken from Knacke's book
        cd0_parachute = 0.5
        type_str = "conical ribbon"
        Parachute.__init__(self, cd0_parachute, z_deploy, x1_factor, cx_factor, type_str)

    def compute_cd(self, mach):

        """
        This function returns a plausible value of the drag coefficient for a hemisflo drogue parachute
        operating at M >> 0.3 (compressibility effects not negligible). The implemented law
        is taken from the plot in "Parachute recovery systems design manual", Section 5

        :param mach {float}: current Mach number
        """

        self.cd = self.cd0 + 0.0 * mach  # The main parachute is expected to work at M < 0.3,
        # therefore we approximate its cd as constant with the mach number

    def compute_delta_t_infl(self, v):
        """
        This method overrides mother-method. It computes the delta time for the
        inflation of a ribbon parachute. The used empirical formula depends
        on the type of parachute. See Knacke's book page 5-42 for details.
        :param v: current velocity [m/s]
        """
        self.delta_t_infl = (8 * np.sqrt(4 * self.surface / np.pi) / (np.abs(v) ** 0.9))

    def compute_dragArea_chute(self, t, z, v, mach):

        """ This method computes the product cD*S of the parachute during the inflation and after it.
            A linear inflation is supposed to take place. This method makes use of *self.compute_delta_t_infl*
            to compute the delta time required for the inflation of the parachute. See pages 5-45 in Knacke's book
            for details.

            :param t {float}: current time instant [s]
            :param z {float}: current altitude [m]
            :param v {float}: current velocity [m/s]
            :param mach {float}: current Mach number
        
        """

        self.compute_cd(mach)

        if z <= self.z_deploy:  # if we have reached the altitude of deployment

            if self.flag_infl == 0:
                # If the inflation has not occurred yet, then it is taking place at this precise instant t
                self.flag_infl = 1
                self.t_infl = t
                self.compute_delta_t_infl(v)
                self.compute_opening_load(z, v)
                self.slope_infl = self.cd * (self.surface) / self.delta_t_infl

            if (t - self.t_infl) <= self.delta_t_infl:  # if the chute is inflating
                self.drag_area = self.slope_infl * (t - self.t_infl)
            else:
                self.drag_area = self.cd * self.surface

