import numpy as np
from parachute import Parachute
from dgb import Dgb
from in_param import InParam
from conicalribbon import ConicalRibbon
from interface import Interface
from pyatmos import coesa76
from scipy.optimize import fsolve
from rocket import Rocket
from scipy.integrate import odeint

from matplotlib import pyplot as plt

GAMMA = 1.4
R_AIR = 287
GRAVITY = 9.81

# altitude = 60  # [km] altitude of initial deployment
# coesa76_altitude = coesa76(altitude)
#
# print( coesa76_altitude.rho)
# print(coesa76_altitude.T)
#
# try:
#     design = int(input("Select a desired design:\n1) Disk-gap-band chute \n2) ConicalRibbon\n"))
# #     consider that historically these are the only two types of parachutes effectivley used for Earth re-entry
# except ValueError:
#     print("You did not make an acceptable choice")
#
# # let us characterize the initial conditions
# in_velocity = 100.0  # [m/s]   then I will add the possibility of simply setting a
# descent_rate = 10.0 # [m/s]
#
# # the altitude
# altitude = 30  # [km] altitude of initial deployment
# coesa76_altitude = coesa76(altitude)
#
# ## let us characterize the payload
# # it is supposed to be a
# mass = 20.0   # [kg] mass of the payload
# diameter_rocket = 0.2  # [m]
# cross_section = (diameter_rocket**2)*np.pi/4
# final_Mach = 0.4   # define the Mach number that the rocket must reach after the deployment of the drogue
#
#
# rocket = Rocket(mass, diameter_rocket)
#
# #interf = Interface(in_velocity, descent_rate, mass, design, coesa76_altitude)   #inVelocity, descentRate, mass, designSelection
#
#
# if design == 1:
#     chute = Dgb(input)
# elif design == 2:
#     chute = ConicalRibbon()
#
#
#
#
# def equation(alt):
#
#     surface = 0.2
#     LHS =  0.5*alt.rho*(final_Mach**2)*1.4*287*alt.T*surface*chute.cD
#
#     return LHS
#
# alt_sol =  fsolve(equation, coesa76_altitude)
#
# print(alt_sol)


# first we "compute" the rho at given altitude

def cd_hemisflo(mach):

# This function returns a plausible value of the drag coefficient for a hemisflo parachute
# operating at M >> 0.3 (compressibility effects not negligible)
      #constant value up to
    if mach < 1.9:
        cd = 0.35
    else:
        cd = -1/9*mach+0.561  # data from Pepper 1986
    return cd


t_infl = 1e10 # mock times-tamp for the deployment of the parachute
flag = 0
slope_infl = 0
delta_t_infl = 0

def compute_dragArea_chute(t,h,v,h_deploy):

    h76 = coesa76(h/1000)
    rho = h76.rho
    temp = h76.T
    mach = v / np.sqrt(GAMMA * R_AIR * temp)

    lambda_t = 25  # total porosity
    cd_chute = cd_hemisflo(mach)
    global slope_infl
    global delta_t_infl
    global t_infl

    drag_area = 0.0
    if h <= h_deploy:   # if we have reached the altitude of deployment
        global flag
        if flag == 0:
            t_infl = t
            delta_t_infl = (8*np.sqrt(4* S_chute / np.pi)/(np.abs(v)**0.9)) #0.65 * lambda_t * np.sqrt(4 * S_chute / np.pi) / np.abs(v)
            print(delta_t_infl)
            flag = 1
            slope_infl = (cd_chute * S_chute) / delta_t_infl

        if t-t_infl <= delta_t_infl:        # if the chute is inflating
            drag_area = slope_infl*(t-t_infl)
        else:
            drag_area = cd_chute*S_chute


    return drag_area

def model(y,t, cd0_rocket, h_deploy, S_chute, S_rocket):
    # y = [h, v], where v = dh/dt
    h,v = y
    m = 20   # kg
    h76 = coesa76(h/1000)   #change the altitude to km

    rho = h76.rho
    temp = h76.T
    mach = v/np.sqrt(GAMMA*R_AIR*temp)

    cd_rocket = (cd0_rocket - 0.2605)*np.exp(0.73 * mach) + 0.2605  # exponential law for the drag of the rocket at a given mach number
    drag_area = compute_dragArea_chute(t,h,v,h_deploy)

    dydt = [v, 1/m*(1/2*rho*(v**2)*S_rocket*(cd_rocket)+ 1/2*rho*(v**2)*drag_area - m*GRAVITY)]


    return dydt


S_chute = 0.2
S_rocket = 0.02
cd0_rocket = 0.55

def dynamics_simulation(h_deploy):


    #h_deploy = 3e3  #let s deploy the chute at h = 4 km
    y0 = [ 100e3, 0]   # inital altitude, intial velocity
    t = np.linspace(0,150,1000)  #seconds

    result = odeint(model,y0,t, args=( cd0_rocket, h_deploy, S_chute, S_rocket))
    h = result[:,0]
    v = result[:,1]

    global slope_infl
    global delta_t_infl
    global t_infl
    global flag
    slope_infl = 0.0
    delta_t_infl = 0.0
    t_infl = 1e5
    flag = 0

    accel = (v[1:]-v[0:-1])/(t[1]-t[0])
# Plot
# plt.subplot(221)
# plt.plot(t, h, "--")
# plt.title("Altitude vs time")
# plt.grid()
# plt.tight_layout()
#
#
# plt.subplot(222)
# plt.plot(t,v, "--")
# plt.title("Velocity magnitude vs time")
# plt.grid()
# plt.tight_layout()
# # let us know approximatly the acceleration experienced by the rocket a_i = v_i+1-v_i/t_h
#
# plt.subplot(223)
# plt.plot(t[0:-1],-accel/9.81, "--")
# plt.title("g's vs time (positive downward)")
# plt.grid()
# plt.show()


    return max(abs(accel))



# h_vec = np.arange(4e3, 9e3, 1000)
# a = np.zeros_like(h_vec)
# for i in range(0, len(h_vec)):
#     a[i] = dynamics_simulation(h_vec[i])

h_vec = np.arange(4e3, 4e9, 1000)
a = np.zeros_like(h_vec)

plt.plot(h_vec, a, linewidth=2)