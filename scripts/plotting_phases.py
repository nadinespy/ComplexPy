#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 12:14:26 2022

@author: nadinespy
"""

import os
import scipy.io as sci
import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np


os.chdir('/media/nadinespy/NewVolume1/my_stuff/work/PhD/my_projects/'
         'EmergenceComplexityMeasuresComparisonSimulations/'
         'EmergenceComplexityMeasuresComparison_Matlab/results/'
         'analyses/12node_kuramoto/sim_time_series')

mat = sci.loadmat('12km_phase_40_20_10000.mat')
phase = mat['phase']


plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig, ax = plt.subplots()

x = np.linspace(0, 15, 100)
y = np.cos(x)

ax.plot(x, y, lw=2, color='red')

def animate(frame):
   ax.set_xlim(left=0, right=frame)

ani = animation.FuncAnimation(fig, animate, frames=10)

plt.show()



import numpy as np
import matplotlib.pyplot as plt

# Initialize
x_axis_start = 0
x_axis_end = 10

plt.axis([x_axis_start, x_axis_end, 0, 1])
plt.ion()

# Realtime plot
for i in range(100):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.10)
    # print(i)

    if i%10 == 0 and i>1:
        print("Axis should update now!")
        x_axis_start += 10
        x_axis_end += 10
        plt.axis([x_axis_start, x_axis_end, 0, 1])