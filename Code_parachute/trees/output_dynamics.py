import numpy as np
from parachute import Parachute
from constants import *
from pyatmos import coesa76

class OutputDynamics:
    """
        Class for writing output data and results of the dynamics simulation.
    """

    def __init__(self):
        """
            Initializes an OutputDynamics object.
        """
        self.mainpara = None
        self.drogue = None
        self.rocket = None
        self.dynamics_obj = None
        self.filename = "OUTPUT_DYNAMICS"
        self.final_v = None
        self.bool_intro = 0
        self.pos_intro = 0

    def write_dynamics(self):
        """
            Writes the output data and results of the dynamics simulation to a file.

        """
        self.mainpara.create_design()
        self.drogue.create_design()
        if self.bool_intro == 0:
            with open(self.filename, 'w') as file:
                file.write(" ------------------- DYNAMICS ROUTINE -------------------\n")

                # The initial conditions, which are the same for each iteration

                file.write("\n ---- Initial conditions: ----\n\n")
                file.write("\t z0 = {:.3f} [km] (initial altitude)\n\n".format(float(self.dynamics_obj.z_vect[0]) / 1000))
                file.write(
                    "\t vx0 = {:.3f} [m/s] (initial horizontal velocity)\n\n".format(float(self.dynamics_obj.vx_vect[0])))
                file.write(
                    "\t vz0 = {:.3f} [m/s] (initial vertical velocity)\n\n".format(float(self.dynamics_obj.vz_vect[0])))
                file.write("\t vz_final = {:.3f} [m/s] (desired final descent rate)\n\n".format(float(self.final_v)))

                file.write(
                    "\n\nHere are listed relevant quantities for each possible altitude of drogue deployment. Use these to select an altitude "
                    "for the deployment of the drogue. (For deployment of the main parachute, z = 500 m should be a reasonable initial guess).\n\n")


        with open(self.filename, 'a') as file:
            file.write(
                "\n\n---------------------------ITERATION #{:d},  Z DEPLOYMENT DROGUE = {:.2f} [m] -------------------------------\n\n".format(
                    self.pos_intro + 1, self.drogue.z_deploy))
            file.write(
                "\tMaximum deceleration: {:.2f} g\n\n".format(
                    float(np.max(np.abs(self.dynamics_obj.az_vect) / GRAVITY))))
            if np.max(np.abs(self.dynamics_obj.az_vect) / GRAVITY) > 50:
                file.write(
                    "\t\t>>>> WARNING: the maximum deceleration is excessive. Consider changing some input value!\n\n")
            max_mach = self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)]
            file.write("\tMach number at drogue deployment: {:.3f}\n\n".format(
                float(max_mach)))
            # We now compute the maximum stagnation temperature
            T_deploy = coesa76(self.drogue.z_deploy/1000).T
            T_max = T_deploy*(1+max_mach**2*(GAMMA-1)/2)
            # file.write("\tMaximum stagnation temperature: {:.3f} [K]\n\n".format(
            #     float(T_max)))


            file.write("\tOpening load (drogue): {:.3f} [N]\n\n".format(self.drogue.opening_force))
            if self.drogue.opening_force > 2e4:
                file.write(
                    "\t\t>>>> WARNING: the opening load for the drogue parachute could be excessive. Consider changing some input value!\n\n")

            file.write("\tOpening load (main): {:.3f} [N]\n\n".format(self.mainpara.opening_force))
            if self.mainpara.opening_force > 5e4:
                file.write(
                    "\t\t>>>> WARNING: the opening load for the main parachute could be excessive. Consider changing some input value!\n\n")

            file.write(
                "\tConstructed surface of drogue parachute = {:.3f} [m^2]\n\n".format(float(self.drogue.surface)))
            file.write(
                "\tConstructed surface of main parachute = {:.3f} [m^2]\n\n".format(float(self.mainpara.surface)))
            if self.mainpara.surface > 10.0:
                file.write(
                    "\t>>>> WARNING: the constructed surface of the main parachute is too big. Consider changing some "
                    "design values!\n\n")
            file.write("\tTotal time for reentry: {:.2f} [s]\n\n".format(self.dynamics_obj.t_vect[-1]))
