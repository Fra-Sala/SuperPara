from matplotlib import pyplot as plt
from matplotlib import animation
from dynamics import DynamicsReentry
from matplotlib import rc
from dynamics import DynamicsReentry
from parachute import Parachute
from drogue import Drogue
from pyatmos import coesa76
from constants import *
import numpy as np


rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)


class PlotAnimate:
    """Class to plot the solution and relevant data"""

    def __init__(self, dynamics_obj):
        """Constructor for this object, which allows to plot and animate the solution of the falling object"""
        self.dynamics = dynamics_obj

    def plot_coord(self):
        plt.figure(1)
        plt.subplot(121)
        plt.plot(self.dynamics.t_vect, self.dynamics.x_vect, "--", lw=2)
        plt.title(r'Horizontal position with time')
        plt.xlabel(r'$t$ [s]')
        plt.ylabel(r'$x$ [m]')
        plt.grid()

        plt.subplot(122)
        plt.plot(self.dynamics.t_vect, self.dynamics.z_vect, "--", lw=2)
        plt.title(r'Altitude with time')
        plt.xlabel(r'$t$ [s]')
        plt.ylabel(r'$z$ [m]')
        plt.grid()
        plt.show()

    def plot_trajectory(self):
        plt.figure()
        plt.plot(self.dynamics.x_vect, self.dynamics.z_vect, "r--", lw=2)
        plt.title(r'Falling trajectory')
        plt.xlabel(r'$x$ [m]')
        plt.ylabel(r'$z$ [m]')
        plt.grid()
        plt.show()

    def animate_reentry(self):
        fig2 = plt.figure(2)
        ax = plt.axes(xlim=(0, self.dynamics.z_vect[0]),
                      ylim=(0, self.dynamics.z_vect[0]))

        line, = ax.plot([], [], "k--", lw=1)
        lineHead, = ax.plot([], [], "bo", lw=2)

        title = ax.text(0, self.dynamics.z_vect[0], 'Reentry of rocket and parachute dynamics',
                        fontsize=15)
        info = ax.text(0.8 * self.dynamics.z_vect[0], 0.8 * self.dynamics.z_vect[0], 'mach',
                       fontsize=12)

        def init():
            line.set_data([], [])
            lineHead.set_data([], [])
            return line, lineHead,

        xdata, zdata = [], []

        # animation function
        def animate(i):
            # i describes the frame number
            # appending values to the previously
            # empty x and y data holders
            if (self.dynamics.t_vect[i * 20] > self.dynamics.drogue.t_infl):
                lineHead.set_color("red")
            # xdata.append()
            # zdata.append(self.dynamics.z_vect[i*20])
            line.set_data(self.dynamics.x_vect[:i * 20], self.dynamics.z_vect[:i * 20])
            lineHead.set_data(self.dynamics.x_vect[i * 20], self.dynamics.z_vect[i * 20])
            title.set_text("Reentry of rocket and parachute dynamics, t={:5.1f}".format(self.dynamics.t_vect[i * 20]))
            v = np.sqrt(self.dynamics.vx_vect[i * 20] ** 2 + self.dynamics.vz_vect[i * 20] ** 2)
            rho = coesa76(self.dynamics.z_vect[i * 20] / 1000).rho
            temp = coesa76(self.dynamics.z_vect[i * 20] / 1000).T

            mach = v / np.sqrt(GAMMA * R_AIR * temp)
            g = -self.dynamics.az_vect[i * 20] / 9.81
            # info.set_text("v={:3.3f}, mach={:2.1f}, rho={:1.8f}, temp, opening force".format(v, mach, rho))
            # info.set_text("mach, m={:2.1f}".format(mach))
            info.set_text("Mach = %.2f\n ||v|| = %.2f m/s\n gs = %.2f \n Opening force = %.3f N" % (
            mach, v, g, self.dynamics.drogue.opening_force))
            return line, lineHead, title, info,

        # calling the animation function

        anim = animation.FuncAnimation(fig2, animate, init_func=init, frames=(len(self.dynamics.t_vect) // 20),
                                       interval=1, repeat=False)
        plt.show()

#
#
# """example """
# fig2 = plt.figure(2)
# ax = plt.axes(xlim=(0, 50e3),
#                 ylim=(0, 100e3))
#
# line, = ax.plot([], [], "k--", lw=1)
# lineHead, = ax.plot([],[],"bo",lw=2)
#
#
# title = ax.text(0,100e3, 'Reentry of rocket and parachute dynamics',
#         fontsize = 15)
#
# def init():
#     line.set_data([], [])
#     lineHead.set_data([],[])
#     return line,lineHead,
#
# # initializing empty values
# # for x and y co-ordinates
# xdata, zdata = [], []
#
# # animation function
# def animate(i):
#     print(i)
#     # i describes the frame number
#     # appending values to the previously
#     # empty x and y data holders
#     if (t[i]> t_infl):
#         lineHead.set_color("red")
#     xdata.append(x[i])
#     zdata.append(z[i])
#     line.set_data(xdata, zdata)
#     lineHead.set_data(x[i],z[i])
#     title.set_text("Reentry of rocket and parachute dynamics, t={:5.1f}".format(t[i]))
#
#     return line,lineHead,title,
#
#
# # calling the animation function
#
#
# anim = animation.FuncAnimation(fig2, animate, init_func=init,  frames=len(t),  interval=1, repeat=False)
# plt.show()
