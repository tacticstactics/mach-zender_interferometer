
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
oplcommon1=100
oplcommon2=100

opl1 = 100000000
opl2= 1

Ein1 = np.array([[1+0.0000j],[0-0.0000j]]) # 1 port only

#Ein1 = np.array([[0.707+0.707j],[0.707-0.707j]]) #Both 1 and 2 port

#Ein1 = np.array([[0],[1]]) # 2 port only


print('')
print('E1')
print(Ein1)
print('')


Eout1 = mach_zender_interferometer_def.propagate1(wavel, no, oplcommon1, oplcommon2, Ein1)

Ein2 = Eout1

print('')
print('Ein2')
print(Ein2)
print('')

PT = 0.5 # PT: Power Transmission

#PT = 0.25
#PT = 0.999

Eout2 = mach_zender_interferometer_def.dielectric_beamsplitter(PT, Ein2)

Ein3 = Eout2
print('')
print('After Beam Splitter')
print('Ein3:')
print(Ein3)
print('')



Eout3 = mach_zender_interferometer_def.propagate1(wavel, no, opl1, opl2, Ein3)

Ein4 = Eout3
print('')
print('Ein4')
print(Ein4)
print('')




Eout4 = mach_zender_interferometer_def.dielectric_beamsplitter(PT, Ein4)


Ein5 = Eout4
print('')
print('Ein5')
print(Ein5)
print('')


Eout5 = mach_zender_interferometer_def.propagate1(wavel, no, oplcommon1, oplcommon2, Ein5)

Ein6 = Eout5
print('')
print('Ein6')
print(Ein6)
print('')



#power_1 = 


#fig = plt.figure(figsize = (10,6), facecolor='lightblue')



