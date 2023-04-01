from plotanimate import PlotAnimate
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
from optimal_reentry import *
from constants import *
import customtkinter as ctk
ctk.set_appearance_mode("light")
window = ctk.CTk()
window.title("SUPERSONIC PARACHUTE DESIGN TOOL")
window.geometry('600x400')


def run_simulation():
    drag_area_main = float(mass_payload.get()) * GRAVITY / (0.5 * RHO_0 * float(final_v.get()) ** 2)
    new_mainpara = ConicalRibbon(float(z_deploy_main.get()), drag_area_main / 0.5, 20)  # conical ribbon parachute
    new_rocket = Rocket(float(cd0_rocket.get()), float(mass_payload.get()),
                        float(cross_rocket.get()))  # cd0 rocket, mass of rocket, cross-section
    new_drogue = Hemisflo(float(z_deploy_drogue.get()), 0.2,
                          25)  # cd0 drogue, altitude of deployment, surface of chute, total porosity
    t_max = 500.0  # [s] maximum time for solution. The simulation will be stopped once the ground is reached
    x0 = 0.0
    dynamics_obj = DynamicsReentry(t_max, x0, float(z0.get()) * 1e3, float(vx0.get()), float(vz0.get()), new_mainpara,
                                   new_drogue,
                                   new_rocket)  # final_time, x0, z0, vx0, vz0, objects)
    window.destroy()
    dynamics_obj.solve_dynamics()

    plot_animate_obj = PlotAnimate(dynamics_obj)
    plot_animate_obj.plot_coord()
    plot_animate_obj.plot_dynamics()

    speed_animation = 30
    if speed_animation < 1:
        print("Please enter a speed for the animation >= 1 (e.g. 20)\n")
    plot_animate_obj.animate_reentry(speed_animation)


# Define a button to run the simulation


label_rocket = ctk.CTkLabel(window, text="ROCKET PARAMETERS")
label_rocket.grid(column=0, row=0)

label_mass = ctk.CTkLabel(window, text="Mass of payload [kg]")
label_mass.grid(column=0, row=1)
mass_payload = ctk.CTkEntry(window, width=50, height=25, corner_radius=10)
mass_payload.grid(column=1, row=1)

label_cd0_rocket = ctk.CTkLabel(window, text="Rocket c_D0 [-]")
label_cd0_rocket.grid(row=2, column=0)
cd0_rocket = ctk.CTkEntry(window, width=50, height=25, corner_radius=10)
cd0_rocket.grid(row=2, column=1)

label_cross_rocket = ctk.CTkLabel(window, text="Rocket cross-section [m^2]")
label_cross_rocket.grid(row=3, column=0)
cross_rocket = ctk.CTkEntry(window, width=50, height=25, corner_radius=10)
cross_rocket.grid(row=3, column=1)

label_initial = ctk.CTkLabel(window, text="INITIAL CONDITIONS")
label_initial.grid(row=4, column=0)

label_z0 = ctk.CTkLabel(window, text="Initial altitude [km]")
label_z0.grid(row=5, column=0)
z0 = ctk.CTkEntry(window, width=50, height=25, corner_radius=10)
z0.grid(row=5, column=1)

label_vx0 = ctk.CTkLabel(window, text="Initial vx [m/s]")
label_vx0.grid(row=6, column=0)
vx0 = ctk.CTkEntry(window, width=50, height=25, corner_radius=10)
vx0.grid(row=6, column=1)

label_vz0 = ctk.CTkLabel(window, text="Initial vz [m/s]")
label_vz0.grid(row=7, column=0)
vz0 = ctk.CTkEntry(window, width=50, height=25, corner_radius=10)
vz0.grid(row=7, column=1)

label_design = ctk.CTkLabel(window, text="DESIGN PARAMETERS")
label_design.grid(row=0, column=2)

label_z_deploy_drogue = ctk.CTkLabel(window, text="Drogue deployment [m]")
label_z_deploy_drogue.grid(row=1, column=2)
z_deploy_drogue = ctk.CTkEntry(window, width=50, height=25, corner_radius=10)
z_deploy_drogue.grid(row=1, column=3)

label_z_deploy_main = ctk.CTkLabel(window, text="Main deployment [m]")
label_z_deploy_main.grid(row=2, column=2)
z_deploy_main = ctk.CTkEntry(window, width=50, height=25, corner_radius=10)
z_deploy_main.grid(row=2, column=3)

label_final_v = ctk.CTkLabel(window, text="Final descent rate [m/s]")
label_final_v.grid(row=3, column=2)
final_v = ctk.CTkEntry(window, width=50, height=25, corner_radius=10)
final_v.grid(row=3, column=3)

button_run = ctk.CTkButton(window, text="RUN",
                           corner_radius=10,
                           hover_color="#AA0",
                           command=run_simulation)
button_run.grid(column=5, row=5)

# run
window.mainloop()

# """This is the main to run the simulation. See documentation for details.
#     By Francesco Sala"""
#
# final_v = 15.0    # m/s, final descent rate
# mass = 80.0      # kg, mass of the payload
# drag_area_main = mass*GRAVITY/(0.5*RHO_0*final_v**2)
#
# new_mainpara = ConicalRibbon(400, drag_area_main/0.5, 20)          # conical ribbon parachute
# new_rocket = Rocket(0.55, mass, 0.02)               # cd0 rocket, mass of rocket, cross-section
# new_drogue = Hemisflo(6e3, 0.2, 25)            # cd0 drogue, altitude of deployment, surface of chute, total porosity
# dynamics_obj = DynamicsReentry(500, 0, 100e3, 300, 0, new_mainpara, new_drogue, new_rocket)  # final_time, x0, z0, vx0, vz0, objects)
#
#
# dynamics_obj.solve_dynamics()
#
# plot_animate_obj = PlotAnimate(dynamics_obj)
# plot_animate_obj.plot_coord()
# plot_animate_obj.plot_dynamics()
#
#
# speed_animation = 30
# if speed_animation < 1:
#     print("Please enter a speed for the animation >= 1 (e.g. 20)\n")
# plot_animate_obj.animate_reentry(speed_animation)
#
#
#
