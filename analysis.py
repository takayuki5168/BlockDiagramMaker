#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from control import matlab
from matplotlib import pyplot as plt
import numpy as np

import block

class Analysis:

    #def __init__(self):

    def analysis(self, widget, block, which):
        nume = [int(n) for n in block.nume_coef]
        deno = [int(d) for d in block.deno_coef]
        nume.reverse()
        deno.reverse()
        system = matlab.tf(nume, deno)

        if which == 'bode':
            matlab.bode(system)
            plt.show()
        elif which == 'rlocus':
            matlab.rlocus(system)
            plt.show()
        elif which == 'nyquist':
            matlab.nyquist(sys)
            plt.show()
        elif which == 'impulse':
            t = np.linspace(0, 3, 1000)
            yout, T = matlab.impulse(system, t)
            plt.plot(T, yout)
            plt.axhline(0, color="b", linestyle="--")
            plt.xlim(0, 3)
            plt.show()
        elif which == 'step':
            t = np.linspace(0, 3, 1000)
            yout, T = matlab.step(system, t)
            plt.plot(T, yout)
            plt.axhline(1, color="b", linestyle="--")
            plt.xlim(0, 3)
            plt.show()
