from constants import *
from pyatmos import coesa76
import numpy as np
from rocket import Rocket
from parachute import Parachute



def model(t,y, drogueObj, rocketObj):

    z, vz, x, vx = y  # retrieve current values of z, vz, x, vx
    z76 = coesa76(z / 1000)  # change the altitude to km
    rho, temp = z76.rho, z76.T  # retrieve current density and temperature

    v = np.sqrt(vz ** 2 + vx ** 2)  # compute modulus of the velocity
    mach = v / np.sqrt(GAMMA * R_AIR * temp)

    rocketObj.compute_cd_rocket(mach)         # set the cd member of the rocket
    drogueObj.compute_dragArea_chute(t, z, v, mach)  # set the drag area member of the drogue chute
    theta = np.arctan(np.abs(vz) / vx)


    dydt = [vz,
            1 / rocketObj.mass * ((1 / 2 * rho * (v ** 2) * rocketObj.cross_section * (rocketObj.cd) + 1 / 2 * rho * (
                    v ** 2) * drogueObj.drag_area) * np.sin(
                theta) - rocketObj.mass * GRAVITY)
        ,
            vx,
            -1 / rocketObj.mass * ((1 / 2 * rho * (v ** 2) * rocketObj.cross_section * (rocketObj.cd) + 1 / 2 * rho * (
                    v ** 2) * drogueObj.drag_area) * np.cos(theta))]




    return dydt
