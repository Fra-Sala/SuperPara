from rocket import Rocket
from parachute import Drogue
from dynamics import DynamicsReentry
from plotanimate import PlotAnimate
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

"""This is the main to run the simulation. See documentation for details.
    By Francesco Sala"""


new_rocket = Rocket(0.55, 20.0, 0.02)               # cd0 rocket, mass of rocket, cross-section
new_drogue = Drogue(0.35, 20e3, 0.2, 25)            # cd0 drogue, altitude of deployment, surface of chute, total porosity
dynamics_obj = DynamicsReentry(230, 0, 100e3, 200, 0, new_drogue, new_rocket)  # final_time, x0, z0, vx0, vz0, objects)

dynamics_obj.solve_dynamics()

plot_animate_obj = PlotAnimate(dynamics_obj)
plot_animate_obj.plot_coord()
plot_animate_obj.plot_trajectory()
plot_animate_obj.animate_reentry()

