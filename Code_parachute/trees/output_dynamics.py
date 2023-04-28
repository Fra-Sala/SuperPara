import numpy as np
from parachute import Parachute
from constants import *


class OutputDynamics:

    def __init__(self, mainpara, drogue, rocket, dynamics_obj, n_iterations, z_deploy_vect, final_v):
        self.mainpara = mainpara
        self.drogue = drogue
        self.rocket = rocket
        self.dynamics_obj = dynamics_obj
        self.filename = "OUTPUT_DYNAMICS"
        self.n_iterations = n_iterations
        self.z_deploy_vect = z_deploy_vect
        self.final_v = final_v

    def write_initial_values(self):
        """
           Writes the initial conditions for a simulation into a txt file "OUTPUT_DYNAMICS".

           :param:
           None

           :return:
           None
           """

        with open(self.filename, 'w') as file:
            file.write(" -------- DYNAMICS ROUTINE --------\n")

            # The initial conditions, which are the same for each iteration

            file.write("\nInitial conditions:\n")
            file.write("\t z0 = {:.3f} [km] (initial altitude)".format(float(self.dynamics_obj.z_vect[0])))
            file.write("\t vx0 = {:.3f} [m/s] (initial horizontal velocity)".format(float(self.dynamics_obj.z_vect[0])))
            file.write("\t vz0 = {:.3f} [m/s] (initial vertical velocity)".format(float(self.dynamics_obj.z_vect[0])))
            file.write("\t vz_final = {:.3f} [m/s] (desired final descent rate)".format(float(self.final_v)))

            file.write(
                "\n\n Here are the relevant quantities for each possible altitude of drogue deployment. Use these to select an altitude "
                "for the deployment of the drogue. For deployment of main, z = 500 m should be a reasonable initial guess.\n\n")

    def write_dynamics(self):
        """

        :rtype: None
        """
        self.mainpara.create_design()
        self.drogue.create_design()

        with open(self.filename, 'a') as file:
            file.write(
                "\t Maximum deceleration: {:.3f} g".format(float(np.max(np.abs(self.dynamics_obj.a_vect) / GRAVITY))))
            file.write("\tMach number at drogue deployment: {:.3f} ".format(
                float(self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)])))
            file.write("\t Opening load (drogue): {:.3f} [N]".format(self.drogue.opening_force))
            if self.drogue.opening_force > 1e4:
                file.write(
                    "\t>>>> WARNING: the opening load for the drogue parachute could be excessive. Consider changing some input value!\n")

            file.write("\t Opening load (main): {:.3f} [N]".format(self.mainpara.opening_force))
            if self.mainpara.opening_force > 3e4:
                file.write(
                    "\t>>>> WARNING: the opening load for the main parachute could be excessive. Consider changing some input value!\n")

            file.write("\t Constructed surface of drogue parachute = {:.3f} [m^2]".format(self.drogue.surface))
            file.write("\t Constructed surface of main parachute = {:.3f} [m^2]".format(self.mainpara.surface))
            if self.mainpara.surface > 10.0:
                file.write(
                    "\t>>>> WARNING: the constructed surface of the main parachute is too big. Consider changing some "
                           "design values!\n")
            file.write("\t Total time for reeentry: {:.2f} [s]".format(self.dynamics_obj.t_vect[-1]))

