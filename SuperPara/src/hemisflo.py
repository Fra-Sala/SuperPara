from parachute import Parachute
from pyatmos import coesa76
import numpy as np


class Hemisflo(Parachute):
    """Class Hemisflo. It contains all the parameters that characterize the preliminary design of the hemisflo drogue parachute"""

    def __init__(self, z_deploy, x1_factor=0.95, cx_factor=1.25):

        """
           Constructor for the Hemisflo class.

           :param z_deploy: Deployment altitude [m].
           :param x1_factor: X1 factor for the parachute (default value: 0.95).
           :param cx_factor: CX factor for the parachute (default value: 1.25).
        """
        # default values for the factors are taken from Knacke's book
        cd0_parachute = 0.35
        type_str = "hemisflo"
        Parachute.__init__(self, cd0_parachute, z_deploy, x1_factor, cx_factor, type_str)

        # Here the attributes that define the geometry of the hemisflo parachute
        #
        # Known values:
        self.a = 0.1
        self.n = 8
        self.b = 2
        self.B_HR = 2 * 0.0254  # [m] 2 inches is the typical width of the horiz ribbon
        self.B_VL = 0.75 * 0.0254  # [m]
        self.B_RR = 1.25 * 0.0254  # [m]
        self.B_VR = 0.25 * 0.0254  # [m]
        self.n_VR = 1  # number of vertical ribbons

        # Initially unknown values:
        #
        # self.D0 = None
        # self.suspension_lines = None
        # self.D_p = None
        self.gamma = None
        self.D = None
        self.r = None
        self.h_max = None
        self.S01 = None
        self.e_gb = None
        self.e_g2 = None
        self.h_e = None
        self.S02 = None
        self.L_v = None
        self.U_RS = None
        self.max_n_HR = None
        self.n_HR_vect = None
        self.R_S = None
        self.A_0 = None
        self.A_0H = None
        self.vent_closed_area = None
        self.vent_open_area = None

    def compute_cd(self, mach):

        """
            This function returns a plausible value of the drag coefficient for a hemisflo parachute
            operating at M >> 0.3 (compressibility effects not negligible). The implemented law
            is taken from the plot in "Parachute recovery systems design manual", Section 5.

            :param mach: current Mach number.

        """

        if mach < 1.9:
            self.cd = 0.35
        else:
            self.cd = -1 / 9 * mach + 0.561  # data from Pepper 1986

    def compute_delta_t_infl(self, v):
        """
            This method overrides mother-method. It computes the delta time for the
            inflation of a ribbon parachute. The used empirical formula depends
            on the type of parachute. See Knacke's book page 5-42 for details.
            :param v: current velocity [m/s].

        """
        self.delta_t_infl = 0.65 * self.lambda_t * 2 * np.sqrt(self.surface / (np.pi)) / np.abs(v)

    def compute_dragArea_chute(self, t, z, v, mach):
        """
           Calculate the drag area of the parachute at a given time.

           :param t: Current instant of time [s].
           :param z: Current altitude [m].
           :param v: Current velocity [m/s].
           :param mach: Current Mach number.
        """
        self.compute_cd(mach)

        if z <= self.z_deploy:  # if we have reached the altitude of deployment

            if self.flag_infl == 0:
                # If the inflation has not occurred yet, then it is taking place at this precise instant t
                self.flag_infl = 1
                self.t_infl = t
                #print("The inflation of the hemisflo takes place at v = %.2f, mach = %,2f", v, mach)
                self.compute_delta_t_infl(v)
                self.compute_opening_load(z, v)
                self.slope_infl = (self.cd) * (self.surface) / self.delta_t_infl

            if (t - self.t_infl) <= self.delta_t_infl:  # if the chute is inflating
                self.drag_area = self.slope_infl * (t - self.t_infl)
            else:
                self.drag_area = self.cd * self.surface

    def create_design(self):
        """
            Compute the design specifications of the drogue parachute.
            This function calculates various geometric parameters and updates the attributes of the parachute object.

        """

        # Extract known values
        b = self.b
        a = self.a
        n = self.n
        n_VR = self.n_VR
        B_HR = self.B_HR
        B_VL = self.B_VL
        B_RR = self.B_RR
        B_VR = self.B_VR
        S0 = float(self.surface)

        # Proceed with computation of the design

        suspension_lines = b * np.sqrt(4 / np.pi * self.surface)
        D0 = np.sqrt(4 / np.pi * S0)
        D_p = np.sqrt(360.0 * S0 / (210.0 * np.pi))  # The formula on page 6-33 Knacke is wrong

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
                  S01 + S02, S0)
        L_v = np.sqrt((0.01 * S0 / n) / (np.sin(np.pi / n) * np.cos(np.pi / n)))
        # here check that the vent does not overlap the horizontal ribbons
        required_distance = B_RR * n
        available_distance = 2 * L_v * np.sin(np.pi / n) * n
        if required_distance > available_distance:
            L_v = required_distance / (2 * n * np.sin(np.pi / n))
        U_RS = h_max + h_e - L_v * np.cos(np.pi / n)

        max_n_HR = np.floor(U_RS / B_HR)
        n_HR_vect = np.arange(3, max_n_HR + 1, 1)  # possible values of n_HR for grid search

        def compute_porosity(desired_lambda, n_HR):
            R_S = (U_RS - B_HR * n_HR) / (n_HR - 1)
            A = np.zeros((n_HR - 1, 6))  # no column for alpha in deg and for cos(alpha)
            A[:, 0] = np.arange(1, n_HR, 1)

            for i in range(0, n_HR - 1):
                A[i, 1] = L_v * np.cos(np.pi / n) + B_HR + R_S / 2 + i * (R_S + B_HR)  # [m] h_n
                A[i, 2] = h_max - A[i, 1]  # [m] h_csn
                A[i, 3] = A[i, 2] / (r * np.cos(np.pi / n))  # [rad] alpha
                A[i, 4] = 2 * r * np.sin(np.pi / n) * np.cos(A[i, 3])
                A[i, 5] = A[i, 4] - B_RR - B_VR * n_VR

            A_0H = R_S * np.sum(A[:, -1])
            vent_closed_area = 2 * (B_VL / 2 * L_v) - (B_VL) ** 2 / (8 * np.tan(np.pi / n))
            vent_open_area = L_v ** 2 * np.sin(np.pi / n) * np.cos(np.pi / n) - vent_closed_area
            A_0 = A_0H + vent_open_area
            lambda_g = A_0 / (S0 / n) * 100

            return abs(lambda_g - desired_lambda)

        err_vect = np.zeros_like(n_HR_vect)
        j = 0
        for i in n_HR_vect:
            err_vect[j] = compute_porosity((self.lambda_t-self.lambda_material), int(i))
            j = j + 1
        n_HR = int(n_HR_vect[err_vect.argmin()])

        # Now that we have find n_HR, we can compute the final geometry
        R_S = (U_RS - B_HR * n_HR) / (n_HR - 1)
        A = np.zeros((n_HR - 1, 6))  # no column for alpha in deg and for cos(alpha)
        A[:, 0] = np.arange(1, n_HR, 1)

        for i in range(0, n_HR - 1):
            A[i, 1] = L_v * np.cos(np.pi / n) + B_HR + R_S / 2 + i * (R_S + B_HR)  # [m] h_n
            A[i, 2] = h_max - A[i, 1]  # [m] h_csn
            A[i, 3] = A[i, 2] / (r * np.cos(np.pi / n))  # [rad] alpha
            A[i, 4] = 2 * r * np.sin(np.pi / n) * np.cos(A[i, 3])
            A[i, 5] = A[i, 4] - B_RR - B_VR * n_VR

        A_0H = R_S * np.sum(A[:, -1])
        vent_closed_area = 2 * (B_VL / 2 * L_v) - (B_VL) ** 2 / (8 * np.tan(np.pi / n))
        vent_open_area = L_v ** 2 * np.sin(np.pi / n) * np.cos(np.pi / n) - vent_closed_area
        if np.abs(vent_open_area) < 5e-3:
            vent_open_area = 0.0
        A_0 = A_0H + vent_open_area

        lambda_final = A_0 / (S0 / n) * 100

        # Update the geometry of the parachute

        self.lambda_t = lambda_final + self.lambda_material

        self.D0 = D0
        self.suspension_lines = suspension_lines
        self.D_p = D_p

        self.gamma = gamma
        self.D = D
        self.r = r
        self.h_max = h_max
        self.S01 = S01
        self.e_gb = e_gb
        self.e_g2 = e_g2
        self.h_e = h_e
        self.S02 = S02
        self.L_v = L_v
        self.U_RS = U_RS
        self.max_n_HR = max_n_HR
        self.n_HR_vect = n_HR_vect
        self.R_S = R_S
        self.A_0 = A_0
        self.A_0H = A_0H
        self.vent_closed_area = vent_closed_area
        self.vent_open_area = vent_open_area

    def write_out(self, file):

        """
            Write the design specifications of the drogue parachute to a file.

            :param file: File object to write the specifications to.
        """

        file.write("\tA_0 = {:.3f} [m^2] (open area of a gore including vent area)\n\n".format(float(self.A_0)))
        file.write(
            "\tA_0H = {:.3f} [m^2] (open area between horizontal ribbons of one gore)\n\n".format(float(self.A_0H)))
        file.write("\tD = {:.3f} [m] (circumferential distance of the hemispherical part)\n\n".format(float(self.D)))
        file.write("\tD_p = {:.3f} [m] (diameter of the hemisphere after inflation)\n\n".format(float(self.D_p)))
        file.write("\te_gb = {:.3f} [m] (gore width at skirt of hemispherical portion)\n\n".format(float(self.e_gb)))
        file.write("\te_g2 = {:.3f} [m] (gore width at skirt of the extension)\n\n".format(float(self.e_g2)))
        file.write(
            "\t\u03B3 = {:.3f} [rad] (angle between two adjacent suspension lines)\n\n".format(float(self.gamma)))
        file.write("\th_e = {:.3f} [m] (height of the skirt extension measured along gore centerline)\n\n".format(
            float(self.h_e)))
        file.write(
            "\th_max = {:.3f} [m] (maximum height of a gore of the hemispherical part)\n\n".format(float(self.h_max)))

        file.write("\tL_e = {:.3f} [m] (Length of suspension lines)\n\n".format(float(self.suspension_lines)))
        file.write("\tL_v = {:.3f} [m] (vent line length divided by two)\n\n".format(float(self.L_v)))
        file.write("\tR_S = {:.3f} [m] (height of space between horizontal ribbons)\n\n".format(float(self.R_S)))
        file.write(
            "\tS_01 = {:.3f} [m^2] (area of the hemispherical portion of the canopy)\n\n".format(float(self.S01)))
        file.write("\tS_02 = {:.3f} [m^2] (area of the skirt extension)\n\n".format(float(self.S02)))
        file.write("\tU_RS = {:.3f} [m] (usable ribbon space)\n\n".format(float(self.U_RS)))
