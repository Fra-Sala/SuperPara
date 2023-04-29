import numpy as np
from parachute import Parachute
from constants import *


class OutputDynamics:

    def __init__(self, mainpara, drogue, rocket, dynamics_obj, final_v):
        self.mainpara = mainpara
        self.drogue = drogue
        self.rocket = rocket
        self.dynamics_obj = dynamics_obj
        self.filename = "OUTPUT_DYNAMICS"
        self.final_v = final_v
        self.bool_intro = 0


    def write_dynamics(self):
        """

        :rtype: None
        """
        self.mainpara.create_design()
        self.drogue.create_design()
        if self.bool_intro == 0:
            with open(self.filename, 'w') as file:
                file.write(" -------- DYNAMICS ROUTINE --------\n")

                # The initial conditions, which are the same for each iteration

                file.write("\nInitial conditions:\n")
                file.write("\t z0 = {:.3f} [km] (initial altitude)".format(float(self.dynamics_obj.z_vect[0])/1000))
                file.write(
                    "\t vx0 = {:.3f} [m/s] (initial horizontal velocity)".format(float(self.dynamics_obj.vx_vect[0])))
                file.write(
                    "\t vz0 = {:.3f} [m/s] (initial vertical velocity)".format(float(self.dynamics_obj.vz_vect[0])))
                file.write("\t vz_final = {:.3f} [m/s] (desired final descent rate)".format(float(self.final_v)))

                file.write(
                    "\n\n Here are the relevant quantities for each possible altitude of drogue deployment. Use these to select an altitude "
                    "for the deployment of the drogue. For deployment of main, z = 500 m should be a reasonable initial guess.\n\n")
                self.bool_intro = 1

        with open(self.filename, 'a') as file:
            file.write(
                "\t Maximum deceleration: {:.3f} g\n".format(float(np.max(np.abs(self.dynamics_obj.az_vect) / GRAVITY))))
            file.write("\tMach number at drogue deployment: {:.3f}\n ".format(
                float(self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)])))
            file.write("\t Opening load (drogue): {:.3f} [N]\n".format(self.drogue.opening_force))
            if self.drogue.opening_force > 1e4:
                file.write(
                    "\t>>>> WARNING: the opening load for the drogue parachute could be excessive. Consider changing some input value!\n")

            file.write("\t Opening load (main): {:.3f} [N]\n".format(self.mainpara.opening_force))
            if self.mainpara.opening_force > 3e4:
                file.write(
                    "\t>>>> WARNING: the opening load for the main parachute could be excessive. Consider changing some input value!\n")

            file.write("\t Constructed surface of drogue parachute = {:.3f} [m^2]\n".format(float(self.drogue.surface)))
            file.write("\t Constructed surface of main parachute = {:.3f} [m^2]\n".format(float(self.mainpara.surface)))
            if self.mainpara.surface > 10.0:
                file.write(
                    "\t>>>> WARNING: the constructed surface of the main parachute is too big. Consider changing some "
                           "design values!\n")
            file.write("\t Total time for reeentry: {:.2f} [s]\n".format(self.dynamics_obj.t_vect[-1]))

