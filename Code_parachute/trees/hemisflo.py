from parachute import Parachute
from pyatmos import coesa76
import numpy as np


class Hemisflo(Parachute):
    """Class Hemisflo. It contains all the parameters that characterize the preliminary design of the hemisflo drouge parachute"""

    def __init__(self, z_deploy, x1_factor=0.95, cx_factor=1.25):
        # default values for the factors are taken from Knacke's book
        cd0_parachute = 0.35
        type_str = "hemisflo"
        Parachute.__init__(self, cd0_parachute, z_deploy, x1_factor, cx_factor, type_str)

        # Here the attributes that define the geometry of the hemisflo parachute
        #
        # Known values:
        self.a = 0.1
        self.n = 20
        self.b = 2
        self.B_HR = 2 * 0.0254  # [m] 2 inches is the typical width of the horiz ribbon
        self.B_VL = 0.75 * 0.0254  # [m]
        self.B_RR = 1.25 * 0.0254  # [m]
        self.B_VR = 0.25 * 0.0254  # [m]

        # Initially unknown values:
        self.gamma = 0.0
        self.D0 = 0.0

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
        self.delta_t_infl = 0.65 * self.lambda_t * 2 * np.sqrt(self.surface / (np.pi)) / np.abs(v)

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
                self.compute_opening_load(z, v)
                self.slope_infl = (self.cd) * (self.surface) / self.delta_t_infl

            if (t - self.t_infl) <= self.delta_t_infl:  # if the chute is inflating
                self.drag_area = self.slope_infl * (t - self.t_infl)
            else:
                self.drag_area = self.cd * self.surface

    def create_design(self):
        """
            This function computes the design specifications of the drogue parachute (such as the length of
            the suspension lines, number of gores, etc.)

        """

        b = self.b
        self.suspension_lines = b * np.sqrt(4 / np.pi * self.surface)
        a = self.a
        n = self.n
        D0 = np.sqrt(4 / np.pi * self.surface)
        S0 = float(self.surface)
        D_p = np.sqrt(360.0 * S0 / (210.0 * np.pi))  # The formula on page 6-33 Knacke is wrong
        h_s = 0.916 * D0 / 2
        gamma = 2 * np.arcsin(
            np.sin(np.pi / n) / (np.pi * (a + b)))  # [rad]

        D = np.sqrt((S0 / n) / (2 / (np.pi ** 2) * np.sin(np.pi / n) * np.cos(np.pi / n) + (
                    a * (a + 2 * b) / (np.pi * (a + b)) * np.sin(np.pi / n) * np.cos(gamma / 2))))
        r = D / np.pi
        h_max = r * np.pi / 2 * np.cos(np.pi / n)
        S01 = 2 * n * r ** 2 * np.sin(np.pi / n) * np.cos(np.pi / n)
        e_gb = 2 * r * np.sin(np.pi / n)
        e_g2 = 2 * b * D * np.sin(gamma / 2)
        h_e = a * D * np.cos(gamma / 2)
        S02 = 1 / 2 * n * (e_gb + e_g2) * h_e
        if np.abs(S01 + S02 - S0) > 5 / 100 * S0:
            print("Sth is wrong with the computation of the hemisflo geometry, these two values should correspond:",
                  S01 + S02, self.surface)
        L_v = np.sqrt(0.01 * S0 / n) / (np.sin(np.pi / n) * np.cos(np.pi / n))
        # here check that the vent does not overlap the horizontal ribbons
        U_RS = h_max + h_e - L_v * np.cos(np.pi / n)
        B_HR = self.B_HR
        B_VL = self.B_VL
        B_RR = self.B_RR
        B_VR = self.B_VR
        max_n_HR = np.floor(U_RS / B_HR)
        n_HR_vect = np.arange(3, max_n_HR + 1, 1)  # possible values of n_HR for grid search

        def compute_porosity(desired_lambda, n_HR):
            R_S = (U_RS - B_HR * n_HR) / (n_HR - 1)
            A = np.zeros((n_HR - 1, 6))  # no column for alpha in deg and for cos(alpha)
            A[:, 0] = np.arange(1, n_HR, 1)

            for i in range(0, n_HR):
                A[i, 1] = L_v * np.cos(np.pi / n) + B_HR + R_S / 2 + i * (R_S + B_HR)  # [m] h_n
                A[i, 2] = h_max - A[i, 1]  # [m] h_csn
                A[i, 3] = A[i, 2] / (r * np.cos(np.pi / n))  # [rad] alpha
                A[i, 4] = 2 * r * np.sin(np.pi / n) * np.cos(A[i, 3])
                A[i, 5] = A[i, 4] - B_RR - (i + 1) * B_VR

            A_0H = R_S * np.sum(A[:, -1])
            vent_closed_area = 2 * (B_VL / 2 * L_v) - (B_VL) ** 2 / (8 * np.tan(np.pi/ n))
            vent_open_area = L_v ** 2 * np.sin(np.pi / n) * np.cos(np.pi / n) - vent_closed_area
            A_0 = A_0H + vent_open_area
            lambda_g = A_0 / (S0 / n) * 100

            return abs(lambda_g - desired_lambda)

        err_vect = np.zeros_like(n_HR_vect)
        j = 0
        for i in n_HR_vect:
            err_vect[j] = compute_porosity(self.lambda_t, int(i))
            j = j + 1
        n_HR = n_HR_vect[err_vect.argmin()]

        # Now that we have find n_HR, we can compute the final geometry
        R_S = (U_RS - B_HR * n_HR) / (n_HR - 1)
        A = np.zeros((n_HR - 1, 6))  # no column for alpha in deg and for cos(alpha)
        A[:, 0] = np.arange(1, n_HR, 1)

        for i in range(0, n_HR):
            A[i, 1] = L_v * np.cos(np.pi / n) + B_HR + R_S / 2 + i * (R_S + B_HR)  # [m] h_n
            A[i, 2] = h_max - A[i, 1]  # [m] h_csn
            A[i, 3] = A[i, 2] / (r * np.cos(np.pi / n))  # [rad] alpha
            A[i, 4] = 2 * r * np.sin(np.pi / n) * np.cos(A[i, 3])
            A[i, 5] = A[i, 4] - B_RR - (i + 1) * B_VR

        A_0H = R_S * np.sum(A[:, -1])
        vent_closed_area = 2 * (B_VL / 2 * L_v) - (B_VL) ** 2 / (8 * np.tan(np.pi / n))
        vent_open_area = L_v ** 2 * np.sin(np.pi / n) * np.cos(np.pi / n) - vent_closed_area
        A_0 = A_0H + vent_open_area
        lambda_g = A_0 / (S0 / n) * 100
        lambda_final = A_0 / (S0 / n) * 100
