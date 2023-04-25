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

            file.write("\n\n 1. DROGUE DESIGN\n\n")
            file.write("You selected a " + self.drogue.type_chute + " parachute.\n\n")
            if self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)] > 1:
                file.write(
                    "The selected drogue parachute will be deployed in supersonic conditions, at Mach = {:.2f}\n\n".format(
                        float(self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)])))
            else:
                file.write(
                    "The selected drogue parachute will be deployed in subsonic conditions, at Mach = {:.2f}\n\n".format(
                        float(
                            self.dynamics_obj.mach_vect[np.where(self.dynamics_obj.t_vect == self.drogue.t_infl)])))
            file.write("Here are the design parameters for the drogue:\n\n\n")
            file.write("\tS0 = {:.3f} [m^2] (total surface of constructed canopy)\n\n".format(float(self.drogue.surface)))
            file.write("\tD0 = {:.3f} [m] (diameter of constructed canopy)\n\n".format(float(self.drogue.D0)))

            file.write("\tcd0 = {:8.2f} [-] (drag coeff. related to S0, low Mach) \n\n".format(float(self.drogue.cd0)))
            file.write("\t\u0394t = {:8.5f} [s] (time required for inflation)\n\n".format(float(self.drogue.delta_t_infl)))
            file.write("\tz_deploy = {:8.2f} [m] (altitude of deployment)\n\n".format(float(self.drogue.z_deploy)))
            file.write("\t\u03BB_T = {:8.3f} % (total porosity)\n\n".format(float(self.drogue.lambda_t)))
            file.write("\tF_x = {:8.3f} [N] (inflation load)\n\n".format(float(self.drogue.opening_force)))
            file.write("\tcx factor = {:8.3f} \n\n".format(self.drogue.cx_factor))
            file.write("\tX1 factor = {:8.3f} \n\n".format(self.drogue.x1_factor))
            file.write("\t ---- Specific values for this type of parachute ----\n\n")
            self.drogue.write_out(file)



            file.write("-------------------------------------------------\n\n")
