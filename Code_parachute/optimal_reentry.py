import numpy as np
from mainpara import Mainpara
from drogue import Drogue
from rocket import Rocket
from dynamics import DynamicsReentry


def optimal_reentry(z_deploy_drogue, z_deploy_main, final_vz, max_force_drogue, max_force_main):

    print(z_deploy_drogue, z_deploy_main)
    new_mainpara = Mainpara(0.5, z_deploy_main, 3.0, 20)  # conical ribbon parachute
    new_rocket = Rocket(0.55, 80.0, 0.02)  # cd0 rocket, mass of rocket, cross-section
    new_drogue = Drogue(0.35, z_deploy_drogue, 0.3,
                        25)  # cd0 drogue, altitude of deployment, surface of chute, total porosity
    dynamics_obj = DynamicsReentry(500, 0, 100e3, 300, 0, new_mainpara, new_drogue,
                                   new_rocket)  # final_time, x0, z0, vx0, vz0, objects)
    dynamics_obj.solve_dynamics()
    print("I have run the simulation")
    alpha = 0.8
    beta = 0.1
    gamma = 0.1

    val = alpha * np.abs(-dynamics_obj.vz_vect[-1] - final_vz)/final_vz + beta * np.abs(
        dynamics_obj.drogue.opening_force - max_force_drogue)/max_force_drogue + gamma * np.abs(
        dynamics_obj.mainpara.opening_force - max_force_main)/max_force_main
    return val
