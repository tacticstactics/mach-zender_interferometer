
import numpy as np
import matplotlib.pyplot as plt


import mach_zender_interferometer_def

print('')
print('mach-zender_interferometer_main.py')
print('')


wavel = 1.55e-6
no = 1
ne = 1.1
theta1 = 22.5
opl = 9999


Ein1 = np.array([[1],[0]])

Eout1 = mach_zender_interferometer_def.propagate1(wavel, no, opl, Ein1)


PT = 0.9

Eout2 = mach_zender_interferometer_def.beamsplitter(PT, Eout1)

print('')

print('E2')
print(Eout2)

print('')

#fig = plt.figure(figsize = (10,6), facecolor='lightblue')



