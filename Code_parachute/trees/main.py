from plotanimate import PlotAnimate
import matplotlib as mpl
from interface import Interface
mpl.rcParams.update(mpl.rcParamsDefault)
from optimal_reentry import *
from constants import *
import customtkinter as ctk

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



if __name__ == "__main__":
    run_all()



