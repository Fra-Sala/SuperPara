from plotanimate import PlotAnimate
import matplotlib as mpl
from interface import Interface
mpl.rcParams.update(mpl.rcParamsDefault)
import customtkinter as ctk
from make_design import MakeDesign
from hemisflo import Hemisflo
from conicalribbon import ConicalRibbon
from rocket import Rocket
from dynamics import DynamicsReentry


def run_all():

    window = ctk.CTk()
    gui = Interface(window)
    window.mainloop()

    new_drogue = gui.new_drogue
    new_mainpara = gui.new_mainpara
    new_rocket = gui.new_rocket
    dynamics_obj = gui.dynamics_obj
    dynamics_obj.solve_dynamics()
    plot_animate_obj = PlotAnimate(dynamics_obj)

    # Plot a couple of graphs

    plot_animate_obj.plot_coord()
    plot_animate_obj.plot_dynamics()

    if gui.show_animation_var.get() == 1:
        speed_animation = 30
        if speed_animation < 1:
            print("Please enter a speed for the animation >= 1 (e.g. 20)\n")
        plot_animate_obj.animate_reentry(speed_animation)

    mkds = MakeDesign(new_mainpara, new_drogue, new_rocket, dynamics_obj)
    mkds.write_text()


def run_mock():
    """
    :param

    """
    new_drogue = Hemisflo(5000)
    new_drogue.required_S0(0.4, 80.0, 400, option=2)
    new_drogue.compute_porosity(type_chute=3)
    new_mainpara = ConicalRibbon(400)
    new_mainpara.required_S0(20, 80.0, z=0.0, option=1)
    new_mainpara.compute_porosity(type_chute=2)

    new_rocket = Rocket(0.55, 80.0, 0.03)
    dynamics_obj = DynamicsReentry(500, 0.0, 100e3, 300.0, 0.0, new_mainpara, new_drogue, new_rocket)
    dynamics_obj.solve_dynamics()
    plot_animate_obj = PlotAnimate(dynamics_obj)

    #no need to plot

    # plot_animate_obj.plot_coord()
    # plot_animate_obj.plot_dynamics()

    mkds = MakeDesign(new_mainpara, new_drogue, new_rocket, dynamics_obj)
    mkds.write_text()


if __name__ == "__main__":

    test = 0
    if test == 0:
        run_all()
    else:
        run_mock()





