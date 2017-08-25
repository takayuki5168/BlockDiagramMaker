#import math
#
#print('[', end='')
#for t in range(500):
#    print('[{}, {}],'.format(t, 50 * math.sin(3 * t / 30 + 10)), end='')
#print(']', end='')
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from control import matlab
from matplotlib import pyplot as plt
import numpy as np

nume_coef = ['1']
deno_coef = ['1', '1', '1']
nume = [int(n) for n in nume_coef]
deno = [int(d) for d in deno_coef]
nume.reverse()
deno.reverse()
print(nume)
print(deno)
system = matlab.tf(nume, deno)

matlab.bode(system)
plt.show()
