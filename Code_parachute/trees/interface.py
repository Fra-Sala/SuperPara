import customtkinter as ctk
import tkinter as tk
from plotanimate import PlotAnimate
import matplotlib as mpl
from make_design import *
from output_dynamics import *

mpl.rcParams.update(mpl.rcParamsDefault)
from optimal_reentry import *
from constants import *

ctk.set_appearance_mode("light")


class Interface:

    """
        A class to manage the GUI. Its methods take care of assembling the dynamics objects and solving the dynamics.
    """

    def __init__(self, master):

        """
            Constructor for the class. Initializes the instance variables and sets up the GUI elements.

            :param master: The master widget (the main window of the GUI).
        """

        #Initialize instance variables
        self.mass = 0.0
        self.cd_rocket = 0.0
        self.rocket_cross_section = 0.0
        self.initial_altitude = 0.0
        self.initial_vx = 0.0
        self.initial_vz = 0.0
        self.z_drogue_deploy = 0.0
        self.z_deploy_main = 0.0
        self.final_v = 0.0
        self.window = master
        self.window.geometry('800x500')
        self.window.resizable(False, False)
        self.window.title("SUPERPARA DESIGN TOOL")
        self.window.option_add('*Font', 'Arial 30')

        self.label_rocket = ctk.CTkLabel(self.window, text="ROCKET PARAMETERS", font=("Times New Roman", 18, "bold"))
        self.label_rocket.grid(column=0, row=0)

        self.label_mass = ctk.CTkLabel(self.window, text="Mass of payload [kg]")
        self.label_mass.grid(column=0, row=1)
        self.mass_payload = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)
        self.mass_payload.grid(column=1, row=1)

        self.label_cd0_rocket = ctk.CTkLabel(self.window, text="Rocket c_D0 [-]")
        self.label_cd0_rocket.grid(row=2, column=0)
        self.cd0_rocket = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)
        self.cd0_rocket.grid(row=2, column=1)

        self.label_cross_rocket = ctk.CTkLabel(self.window, text="Rocket cross-section [m^2]")
        self.label_cross_rocket.grid(row=3, column=0)
        self.cross_rocket = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)
        self.cross_rocket.grid(row=3, column=1)

        self.label_initial = ctk.CTkLabel(self.window, text="INITIAL CONDITIONS", font=("Times New Roman", 18, "bold"))
        self.label_initial.grid(row=4, column=0)

        self.label_z0 = ctk.CTkLabel(self.window, text="Initial altitude [km]")
        self.label_z0.grid(row=5, column=0)
        self.z0 = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)
        self.z0.grid(row=5, column=1)

        self.label_vx0 = ctk.CTkLabel(self.window, text="Initial vx [m/s]")
        self.label_vx0.grid(row=6, column=0)
        self.vx0 = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)
        self.vx0.grid(row=6, column=1)

        self.label_vz0 = ctk.CTkLabel(self.window, text="Initial vz [m/s]")
        self.label_vz0.grid(row=7, column=0)
        self.vz0 = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)
        self.vz0.grid(row=7, column=1)

        self.label_initial = ctk.CTkLabel(self.window, text="DESIGN PARAMETERS", font=("Times New Roman", 18, "bold"))
        self.label_initial.grid(row=0, column=2)

        # We now allow the user the decide whether to run the code once for a given altitude of deployment of the drogue,
        # or to iterate and study how the dynamics changes for different values of the altitude of deployment of the drogue

        self.label_option_iterate = ctk.CTkLabel(self.window, text="Select an option:")
        self.label_option_iterate.grid(row=1, column=2)
        self.option_iterate_var = tk.IntVar()

        # A button if we want to iterate
        self.iterate_z_rb = ctk.CTkRadioButton(self.window,
                                               text="Iterate dynamics for different altitudes\n of deployment of the drogue",
                                               variable=self.option_iterate_var, value=1, command=self.show_iterate)
        self.iterate_z_rb.grid(row=2, column=2)

        # A button if we want to output the design
        self.single_z_rb = ctk.CTkRadioButton(self.window,
                                              text="Define altitude for drogue deployment\n and compute design",
                                              variable=self.option_iterate_var, value=2, command=self.show_iterate)
        self.single_z_rb.grid(row=3, column=2)

        # Prepare the entries for the iterations of the dynamics
        self.label_first_z_iterate = ctk.CTkLabel(self.window, text="Begin iterations at z1 [m] (z1>z2):")
        self.first_z_iterate = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)

        self.label_second_z_iterate = ctk.CTkLabel(self.window, text="End iterations at z2 [m] (z1>z2):")
        self.second_z_iterate = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)

        self.label_n_iterations = ctk.CTkLabel(self.window, text="Number of iterations in [z2,z1] (z1>z2):")
        self.n_iterations = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)

        # Prepare the entry for the case of single design
        self.label_z_deploy_drogue = ctk.CTkLabel(self.window, text="Drogue deployment [m]")
        self.z_deploy_drogue = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)

        # Other design parameters
        self.label_z_deploy_main = ctk.CTkLabel(self.window, text="Main deployment [m]")
        self.label_z_deploy_main.grid(row=7, column=2)
        self.z_deploy_main = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)
        self.z_deploy_main.grid(row=7, column=3)

        self.label_final_v = ctk.CTkLabel(self.window, text="Final descent rate [m/s]")
        self.label_final_v.grid(row=8, column=2)
        self.final_v = ctk.CTkEntry(self.window, width=50, height=25, corner_radius=10)
        self.final_v.grid(row=8, column=3)

        self.label_initial = ctk.CTkLabel(self.window, text="TYPE OF PARACHUTES", font=("Times New Roman", 18, "bold"))
        self.label_initial.grid(row=9, column=2)

        # Here we define the checkbox to choose the desidered type of parachute
        self.label_drogue = ctk.CTkLabel(self.window, text="Select type of drogue parachute:")
        self.label_drogue.grid(row=10, column=2)
        self.hemisflo_type_var = tk.BooleanVar(value=False)
        self.hemisflo_type_cb = ctk.CTkCheckBox(self.window, text="Hemisflo (supersonic)",
                                                variable=self.hemisflo_type_var)
        self.hemisflo_type_cb.grid(row=11, column=2)

        self.label_drogue = ctk.CTkLabel(self.window, text="Select type of main parachute:")
        self.label_drogue.grid(row=12, column=2)
        self.conical_ribbon_type_var = tk.BooleanVar(value=False)
        self.conical_ribbon_type_cb = ctk.CTkCheckBox(self.window, text="Conical Ribbon",
                                                      variable=self.conical_ribbon_type_var)
        self.conical_ribbon_type_cb.grid(row=13, column=2)

        # A button to run the simulation
        self.button_run = ctk.CTkButton(self.window, text="RUN",
                                        corner_radius=10,
                                        hover_color="#AA0",
                                        command=self.run_button)
        self.button_run.grid(row=12, column=5)

        # Here we let the user decide whether to have insights into the dynamics
        self.show_animation_var = tk.BooleanVar(value=False)
        self.show_animation_cb = ctk.CTkCheckBox(self.window, text="Show Animation", variable=self.show_animation_var)
        self.show_animation_cb.grid(row=13, column=5)

        # The following label is used to print possible errors when parsing the using input
        self.label = ctk.CTkLabel(master, text="")
        self.label.grid(row=9, column=2)

        # Here the attributes to store the necessary objects
        self.new_drogue = None
        self.new_mainpara = None
        self.new_rocket = None
        self.dynamics_obj = None

    def show_iterate(self):
        """
            This method is called when the user selects the iterate option. It shows or hides the input fields based on the selected
            option.

        """


        if self.option_iterate_var.get() == 1:
            self.label_first_z_iterate.grid(row=4, column=2)
            self.first_z_iterate.grid(row=4, column=3)
            self.label_second_z_iterate.grid(row=5, column=2)
            self.second_z_iterate.grid(row=5, column=3)
            self.label_n_iterations.grid(row=6, column=2)
            self.n_iterations.grid(row=6, column=3)

            # Delete entries for the case of single design
            self.label_z_deploy_drogue.grid_forget()
            self.z_deploy_drogue.grid_forget()

        elif self.option_iterate_var.get() == 2:
            self.label_z_deploy_drogue.grid(row=4, column=2)
            self.z_deploy_drogue.grid(row=4, column=3)

            self.label_first_z_iterate.grid_forget()
            self.first_z_iterate.grid_forget()
            self.label_second_z_iterate.grid_forget()
            self.second_z_iterate.grid_forget()
            self.label_n_iterations.grid_forget()
            self.n_iterations.grid_forget()

    def run_button(self):

        """
            This function is triggered when the "Run" button is clicked by the user. It performs the necessary validations on the input values
            and executes the simulation based on the selected options (i.e. it either iterates the dynamics or solves it only once).

        """

        text_mass_payload = self.mass_payload.get()
        text_cd0_rocket = self.cd0_rocket.get()
        text_cross_rocket = self.cross_rocket.get()
        text_z0 = self.z0.get()
        text_vx0 = self.vx0.get()
        text_vz0 = self.vz0.get()
        text_z_deploy_drogue = self.z_deploy_drogue.get()
        text_z_deploy_main = self.z_deploy_main.get()
        text_final_v = self.final_v.get()
        text_z1 = self.first_z_iterate.get()
        text_z2 = self.second_z_iterate.get()
        text_n_iterations = self.n_iterations.get()

        # Initialize error message variable
        error_message = "ERROR:\n"

        try:
            # Convert the entered text to float values
            mass_payload = float(text_mass_payload)
        except ValueError:
            error_message += "mass_payload must be a valid float.\n"

        try:
            # Convert the entered text to float values
            cd0_rocket = float(text_cd0_rocket)
        except ValueError:
            error_message += "cd0 rocket must be a valid float.\n"

        try:
            # Convert the entered text to float values
            cross_rocket = float(text_cross_rocket)
        except ValueError:
            error_message += "The rocket cross section must be a valid float.\n"

        try:
            # Convert the entered text to float values
            z0 = float(text_z0)
        except ValueError:
            error_message += "z0 must be a valid float.\n"

        try:
            # Convert the entered text to float values
            vx0 = float(text_vx0)
        except ValueError:
            error_message += "vx0 must be a valid float.\n"

        try:
            # Convert the entered text to float values
            vz0 = float(text_vz0)
        except ValueError:
            error_message += "vz0 must be a valid float.\n"

        if self.option_iterate_var.get() == 1:
            try:
                # Convert the entered text to float values
                z1 = float(text_z1)
            except ValueError:
                error_message += "z1 for iterations must be a valid float.\n"

            try:
                # Convert the entered text to float values
                z2 = float(text_z2)
            except ValueError:
                error_message += "z2 for iterations must be a valid float.\n"

            try:
                # Convert the entered text to float values
                n_iter = int(text_n_iterations)
            except ValueError:
                error_message += "The number of iterations must be a valid integer.\n"



        elif self.option_iterate_var.get() == 2:
            try:
                # Convert the entered text to float values
                z_deploy_drogue = float(text_z_deploy_drogue)
            except ValueError:
                error_message += "z_deploy_drogue must be a valid float.\n"

        try:
            # Convert the entered text to float values
            z_deploy_main = float(text_z_deploy_main)
        except ValueError:
            error_message += "z_deploy_main must be a valid float.\n"

        try:
            # Convert the entered text to float values
            final_v = float(text_final_v)
        except ValueError:
            error_message += "final_v must be a valid float.\n"

            # If there is an error message, display it in the label widget
        if error_message:
            self.label.configure(text=error_message)
        else:
            # If there is no error message, display the values in the label widget
            result = f"mass_payload = {mass_payload}\n" \
                     f"cd0_rocket = {cd0_rocket}\n" \
                     f"cross_rocket = {cross_rocket}\n" \
                     f"z0 = {z0}\n" \
                     f"vx0 = {vx0}\n" \
                     f"vz0 = {vz0}\n" \
                     f"z_deploy_drogue = {z_deploy_drogue}\n" \
                     f"z_deploy_main = {z_deploy_main}\n" \
                     f"final_v = {final_v}\n"
            self.label.configure(text=result)

        outdy = OutputDynamics();   # Create an object to output the dynamics

        self.window.withdraw()
        if self.option_iterate_var.get() == 1:
            z_vect_iter = np.linspace(z1, z2, n_iter); # the highest altitude is the first to be tested
            for i, z in enumerate(z_vect_iter):
                # Check if this is the first iteration
                if i != 0:
                    outdy.bool_intro = 1
                outdy.pos_intro = i
                self.make_simulation(z, i, outdy)

        elif self.option_iterate_var.get() == 2:
            self.make_simulation(z_deploy_drogue, 0,  outdy)
            plot_animate_obj = PlotAnimate(self.dynamics_obj)
            plot_animate_obj.plot_coord()
            plot_animate_obj.plot_dynamics()

            if self.show_animation_var.get() == 1:
                speed_animation = 30
                plot_animate_obj.animate_reentry(speed_animation)

            mkds = MakeDesign(self.new_mainpara, self.new_drogue, self.new_rocket, self.dynamics_obj)
            mkds.write_text()

        self.window.destroy()


    def make_simulation(self, z_deploy_drogue, pos, outdy):
        """
            This function performs a simulation of a rocket reentry using the provided parameters.

            :param z_deploy_drogue: the altitude at which the drogue parachute is deployed.
            :param pos: the position in the (eventual) array of altitudes, when iterating.
            :param outdy: the output dynamics object.
        """

        mass_payload = float(self.mass_payload.get())
        cd0_rocket = float( self.cd0_rocket.get())
        cross_rocket = float(self.cross_rocket.get())
        z0 = float(self.z0.get())
        vx0 = float(self.vx0.get())
        vz0 = float(self.vz0.get())
        z_deploy_main = float(self.z_deploy_main.get())
        final_v = float(self.final_v.get())

        # First of all, create objects for both the drogue and main parachute
        if self.hemisflo_type_var.get() == 1:
            self.new_drogue = Hemisflo(z_deploy_drogue)
        else:
            print("Sorry, no other types of drogue parachutes are implemented at the moment\n")

        mach_after_drogue = 0.4
        self.new_drogue.required_S0(mach_after_drogue, mass_payload, z_deploy_main, option=2)
        self.new_drogue.compute_porosity(type_chute=3)

        if self.conical_ribbon_type_var.get() == 1:
            self.new_mainpara = ConicalRibbon(z_deploy_main)  # conical ribbon parachute
        else:
            print("Sorry, no other types of main parachutes are implemented at the moment\n")

        self.new_mainpara.required_S0(final_v, mass_payload, z=0.0, option=1)

        self.new_mainpara.compute_porosity(type_chute=2)

        self.new_rocket = Rocket(cd0_rocket, mass_payload + 0.01 * mass_payload,
                                 cross_rocket)  # cd0 rocket, mass of rocket, cross-section

        t_max = 1000.0          # [s] upper bound for duration of reentry. (For comparison, 180 s is a likely value)
        x0 = 0.0                # [m] the origin of the frame of reference is on the vertical of the apogee
        self.dynamics_obj = DynamicsReentry(t_max, x0, z0 * 1e3, vx0, vz0, self.new_mainpara,
                                            self.new_drogue,
                                            self.new_rocket)  # final_time, x0, z0, vx0, vz0, objects)
        # Solve the dynamics
        self.dynamics_obj.solve_dynamics()

        # Set the attributes of the output dynamics object
        outdy.mainpara = self.new_mainpara
        outdy.drogue = self.new_drogue
        outdy.rocket = self.new_rocket
        outdy.dynamics_obj = self.dynamics_obj
        outdy.final_v = final_v
        outdy.pos_iter = pos

        # Print the variables concerning the dynamics to file
        outdy.write_dynamics()

