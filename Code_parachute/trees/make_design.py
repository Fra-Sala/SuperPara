import numpy as np
from parachute import Parachute


class MakeDesign:

    def __init__(self, mainpara, drogue, rocket, dynamics_obj):

        self.mainpara = mainpara
        self.drogue = drogue
        self.rocket = rocket
        self.dynamics_obj = dynamics_obj
        self.filename = "OUTPUT_DESIGN"

    def write_text(self):
        """

        :rtype: None
        """
        self.mainpara.create_design()
        self.drogue.create_design()

        with open(self.filename, 'w') as file:
            file.write(" -------- SUPERSONIC DESIGN PRELIMINARY PARACHUTE -------\n")

            file.write("\n\n 1. DROGUE DESIGN\n")
            file.write("You selected a " + self.drogue.type_chute + " parachute.\n")
            if self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)] > 1:
                file.write(
                    "The selected drogue parachute will be deployed in supersonic conditions, at Mach = {:.2f}\n".format(
                        float(self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)])))
            else:
                file.write(
                    "The selected drogue parachute will be deployed in subsonic conditions, at Mach = {:.2f}\n".format(
                        float(
                            self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)])))
            file.write("Here are the design parameters for the drogue:\n\n")
            file.write("\tS0 = {:.3f} [m^2]\n".format(float(self.drogue.surface)))
            file.write("\tD0 = {:.3f} [m]\n".format(float(self.drogue.D0)))
            file.write("\tDp = {:.3f} [m]\n".format(float(self.drogue.D_p)))
            file.write("\tDrag coeff. related to S0, cd0 = {:.2f} [-]\n".format(float(self.drogue.cd0)))
            file.write("\t\u0394t inflation = {:.5f} [s]\n".format(float(self.drogue.delta_t_infl)))
            file.write("\tAltitude of deployment = {:.2f}[m]\n".format(float(self.drogue.z_deploy)))
            file.write("\tTotal porosity = {:.3f} %\n".format(float(self.drogue.lambda_t)))
            file.write("\tInflation load = {:.3f} [N]\n".format(float(self.drogue.opening_force)))
            file.write("\tcx factor = {:.3f} \n".format(self.drogue.cx_factor))
            file.write("\tX1 factor = {:.3f} \n".format(self.drogue.x1_factor))

            file.write("\tLength of suspension lines  = {:.2f} [m]\n".format(float(self.drogue.suspension_lines)))
            file.write("\tNumber of gores \n")
            file.write("\tGore height h_s  = {:.3f} [m]\n".format(float(self.drogue.h_s)))
            file.write("\tD_v (vent diameter) = \n")
            file.write("\tCanopy cone angle\n")
            file.write("\tTotal porosity = {:.3f} \n".format(float(self.drogue.lambda_t)))

            file.write("-------------------------------------------------\n")
