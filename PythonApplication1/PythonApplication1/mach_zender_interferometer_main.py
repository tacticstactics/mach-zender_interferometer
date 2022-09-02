
import numpy as np
import matplotlib.pyplot as plt

import mach_zender_interferometer_def

print('')
print('mach-zender_interferometer_main.py')
print('')


wavel = 1.55e-6
no = 1
#ne = 1.1
#theta1 = 22.5
oplcommon1=1
oplcommon2=1

opl1 = 400
opl2= 399.99

Ein1 = np.array([[1],[0]])

#Ein1 = np.array([[0.707],[0.707]])


print('')
print('E1')
print(Ein1)
print('')


Eout1 = mach_zender_interferometer_def.propagate1(wavel, no, oplcommon1, oplcommon2, Ein1)

Ein2 = Eout1

print('')
print('E2')
print(Ein2)
print('')

PT = 0.5

#PT = 0.25
#PT = 0.999

Eout2 = mach_zender_interferometer_def.dielectric_beamsplitter(PT, Ein2)

print('')
print('E2')
print(Eout2)
print('')


Ein3 = Eout2
Eout3 = mach_zender_interferometer_def.propagate1(wavel, no, opl1, opl2, Ein3)

print('')
print('Eout3')
print(Eout3)
print('')



Ein4 = Eout3
Eout4 = mach_zender_interferometer_def.dielectric_beamsplitter(PT, Ein4)


Ein5 = Eout4
Eout5 = mach_zender_interferometer_def.propagate1(wavel, no, oplcommon1, oplcommon2, Ein5)

print('')
print('Eout5')
print(Eout5)
print('')


#fig = plt.figure(figsize = (10,6), facecolor='lightblue')



