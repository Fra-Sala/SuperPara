from matplotlib import pyplot as plt
from matplotlib import animation
from dynamics import DynamicsReentry
from matplotlib import rc
from dynamics import DynamicsReentry
from parachute import Parachute
from hemisflo import Hemisflo
from pyatmos import coesa76
from constants import *
import numpy as np

rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
rc('text', usetex=True)
plt.rc('text', usetex=True)
plt.rcParams.update({
    'text.usetex': True
})


class PlotAnimate:
    """Class to plot the solution and relevant data"""

    def __init__(self, dynamics_obj):
        """Constructor for this object, which allows to plot and animate the solution of the falling object"""
        self.dynamics = dynamics_obj

    def plot_coord(self):
        plt.figure(1)
        plt.subplot(131)
        plt.plot(self.dynamics.t_vect, self.dynamics.x_vect, "b-", lw=2)
        plt.title(r'Horizontal position with time')
        plt.xlabel(r'$t$ [s]')
        plt.ylabel(r'$x$ [m]')
        plt.grid()

        plt.subplot(132)
        plt.plot(self.dynamics.t_vect, self.dynamics.z_vect, "g-", lw=2)
        plt.title(r'Altitude with time')
        plt.xlabel(r'$t$ [s]')
        plt.ylabel(r'$z$ [m]')
        plt.grid()

        plt.subplot(133)
        plt.plot(self.dynamics.x_vect, self.dynamics.z_vect, "r--", lw=2)
        plt.title(r'Falling trajectory')
        plt.xlabel(r'$x$ [m]')
        plt.ylabel(r'$z$ [m]')
        plt.grid()
        plt.show()

    def plot_dynamics(self):
        plt.figure(1)
        plt.subplot(141)
        plt.plot(self.dynamics.t_vect, self.dynamics.vx_vect, "b-", lw=2)
        plt.title(r'Velocity component vx with time')
        plt.xlabel(r'$t$ [s]')
        plt.ylabel(r'$x$ [m]')
        plt.grid()

        plt.subplot(142)
        plt.plot(self.dynamics.t_vect, self.dynamics.vz_vect, "g-", lw=2)
        plt.title(r'Velocity component vz with time')
        plt.xlabel(r'$t$ [s]')
        plt.ylabel(r'$vz$ [m/s]')
        plt.grid()

        plt.subplot(143)
        plt.plot(self.dynamics.t_vect, self.dynamics.g_vect, "r-", lw=2)
        plt.title(r'Number of g''s with time')
        plt.xlabel(r'$t$ [s]')
        plt.ylabel(r'$g$')
        plt.grid()

        plt.subplot(144)
        plt.plot(self.dynamics.t_vect, self.dynamics.mach_vect, "k-", lw=2)
        plt.title(r'Mach number during reentry')
        plt.xlabel(r'$t$ [s]')
        plt.ylabel(r'$M$')
        plt.grid()
        plt.show()

    def animate_reentry(self, speed=20):
        fig2 = plt.figure(2)
        ax = plt.axes(xlim=(0, self.dynamics.z_vect[0]),
                      ylim=(0, self.dynamics.z_vect[0]))

        line, = ax.plot([], [], "k--", lw=1)
        lineHead, = ax.plot([], [], "bo", lw=2)

        title = ax.text(0,1.05, 'Animation of the reentry of rocket and parachute dynamics',
                        fontsize=15, transform=ax.transAxes) #0, self.dynamics.z_vect[0]
        info = ax.text(0.8, 0.8, 'Mach',
                       fontsize=12, transform=ax.transAxes)

        def init():
            line.set_data([], [])
            lineHead.set_data([], [])
            return line, lineHead,

        xdata, zdata = [], []

        # animation function
        def animate(i):
            i = i * speed
            if (self.dynamics.t_vect[i] > self.dynamics.drogue.t_infl):
                lineHead.set_color("red")
            if (self.dynamics.t_vect[i] > self.dynamics.mainpara.t_infl):
                lineHead.set_color("orange")

            line.set_data(self.dynamics.x_vect[:i], self.dynamics.z_vect[:i])
            lineHead.set_data(self.dynamics.x_vect[i], self.dynamics.z_vect[i])
            title.set_text("Reentry of rocket and parachute dynamics, t={:5.1f}".format(self.dynamics.t_vect[i]))
            v = np.sqrt(self.dynamics.vx_vect[i] ** 2 + self.dynamics.vz_vect[i] ** 2)
            rho = coesa76(self.dynamics.z_vect[i] / 1000).rho
            temp = coesa76(self.dynamics.z_vect[i] / 1000).T

            mach = v / np.sqrt(GAMMA * R_AIR * temp)

            # info.set_text("v={:3.3f}, mach={:2.1f}, rho={:1.8f}, temp, opening force".format(v, mach, rho))
            # info.set_text("mach, m={:2.1f}".format(mach))
            info.set_text(
                "Altitude: %.1f m\n Mach = %.2f\n ||v|| = %.2f m/s\n g = %.1f \n Opening force drogue = %.2f N \n  Opening force main chute = %.2f N \n g_max = %.1f\n max Mach = %.2f\n" % (
                    self.dynamics.z_vect[i],mach, v, self.dynamics.g_vect[i], self.dynamics.drogue.opening_force,
                    self.dynamics.mainpara.opening_force, np.max(np.abs(self.dynamics.g_vect)),
                    np.max(np.abs(self.dynamics.mach_vect))))
            return line, lineHead, title, info,

        # calling the animation function

        anim = animation.FuncAnimation(fig2, animate, init_func=init, frames=(len(self.dynamics.t_vect) // speed),
                                       interval=1, repeat=False)
        plt.show()
