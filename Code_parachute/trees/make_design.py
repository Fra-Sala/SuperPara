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
        with open(self.filename, 'w') as file:
            file.write(" -------- SUPERSONIC DESIGN PRELIMINARY PARACHUTE -------\n")

            file.write("\n\n 1. DROGUE DESIGN\n")
            file.write("You selected a " + self.drogue.type_chute + " parachute\n")
            if self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)] > 1:
                file.write("The selected drogue parachute will be deployed in supersonic conditions, at Mach = " + str(self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)]) + "\n")
            else:
                file.write("The selected drogue parachute will be deployed in subsonic conditions, at Mach = " + str(
                    self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)]) + "\n")
            file.write("Here are the design parameters for the drogue:\n\n")
            file.write("\tS_0 = {:.2f} [m^2]\n".format(float(self.drogue.surface)))
            file.write("\tcd0 (at v = 0 m/s) = {:.2f} [-]\n".format(float(self.drogue.cd0)))
            file.write("\tdelta t = {:.5f} [s]\n".format(float(self.drogue.delta_t_infl)))
            file.write("\tAltitude of deployment = {:.2f}[m]\n".format(float(self.drogue.z_deploy)))
            file.write("\tTotal porosity = {:.2f} %\n".format(float(self.drogue.lambda_t)))
            file.write("\tInflation load = {:.2f} [N]\n".format(float(self.drogue.opening_force)))
            file.write("\tcx factor = {:.3f} \n".format(self.drogue.cx_factor))
            file.write("\tX1 factor = {:.3f} \n".format(self.drogue.x1_factor))
            file.write("Length of suspension lines\n")
            file.write("Number of gores \n")
            file.write("Diameter of hole on top\n")
            file.write("Canopy cone angle\n")

            file.write("-------------------------------------------------\n")