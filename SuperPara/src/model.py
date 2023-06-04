from constants import *
from pyatmos import coesa76
import numpy as np


def model(t, y, mainparaObj, drogueObj, rocketObj):
    """
        Implementation of the dynamical model of the problem.
        Simulates the reentry from an altitude of a payload and the opening of a drogue chute and a main parachute.

        :param t: Current time.
        :param y: Current state vector [z, vz, x, vx].
        :param mainparaObj: Object of the class MainPara representing main parachute parameters.
        :param drogueObj: Object of the class Drogue representing drogue parachute parameters.
        :param rocketObj: Object of the class Rocket representing rocket parameters.
        :return: The derivative of the state vector [dz/dt, dvz/dt, dx/dt, dvx/dt].
    """

    z, vz, x, vx = y  # retrieve current values of z, vz, x, vx
    z76 = coesa76(z / 1000)  # change the altitude to km
    rho, temp = z76.rho, z76.T  # retrieve current density and temperature

    v = np.sqrt(vz ** 2 + vx ** 2)  # compute modulus of the velocity
    mach = v / np.sqrt(GAMMA * R_AIR * temp)

    rocketObj.compute_cd_rocket(mach)  # set the cd member of the rocket
    drag_area_chute = 0.0
    if z > mainparaObj.z_deploy:  # check whether we should try to compute cD*S for the drogue or for the main parachute
        drogueObj.compute_dragArea_chute(t, z, v,
                                                           mach)  # set the drag area member of the drogue chute
        drag_area_chute = drogueObj.drag_area
    else:
        mainparaObj.compute_dragArea_chute(t, z, v, mach)
        drag_area_chute = mainparaObj.drag_area
    theta = np.arctan(np.abs(vz) / vx)

    dydt = [vz,
            1 / rocketObj.mass * ((1 / 2 * rho * (v ** 2) * rocketObj.cross_section * (rocketObj.cd) + 1 / 2 * rho * (
                    v ** 2) * drag_area_chute) * np.sin(
                theta) - rocketObj.mass * GRAVITY),
            vx,
            -1 / rocketObj.mass * ((1 / 2 * rho * (v ** 2) * rocketObj.cross_section * (rocketObj.cd) + 1 / 2 * rho * (
                    v ** 2) * drag_area_chute) * np.cos(theta))]

    return dydt
