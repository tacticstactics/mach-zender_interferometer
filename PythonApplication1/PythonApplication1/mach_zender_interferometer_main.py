
import numpy as np
import matplotlib.pyplot as plt

import mach_zender_interferometer_def

print('')
print('mach-zender_interferometer_main.py')
print('')

m = 512
wavel = 1.55e-6
no = 1
#ne = 1.1
#theta1 = 22.5
oplcommon1=100
oplcommon2=100

opl1 = 1000
opl2= 10

# Input Port 1 only
#Ein1 = np.array([[1+0.0000j],[0-0.0000j]])
#Ein1 = np.array([[0.707+0.707j],[0]])

# Input Both 1 and 2 port
#Ein1 = np.array([[0.707+0j],[0.707-0j]]) 
#Ein1 = np.array([[0.707+0.707j],[0.707-0.707j]]) #Both 1 and 2 port

# Input Port 2 only
#Ein1 = np.array([[0],[1]]) # 2 port only
Ein1 = np.array([[0],[0.707+0.707j]])


stepwl = 0.00003; # um
wl0 = 0.65; #um
wlcol = np.zeros((m,1));
PP1col = np.zeros((m,1));
P1_phasecol = np.zeros((m,1));
PP2col = np.zeros((m,1));

PT = 0.5 # PT: Power Transmission


for ii in range(m):
 wl = wl0 + ii * stepwl
 wlcol[(ii)] =wl

 Eout1 = mach_zender_interferometer_def.propagate1(wl, no, oplcommon1, oplcommon2, Ein1)
 Ein2 = Eout1
 
 Eout2 = mach_zender_interferometer_def.dielectric_beamsplitter(PT, Ein2)
 Ein3 = Eout2
 
 Eout3 = mach_zender_interferometer_def.propagate1(wl, no, opl1, opl2, Ein3) 
 Ein4 = Eout3
 
 Eout4 = mach_zender_interferometer_def.dielectric_beamsplitter(PT, Ein4) 
 Ein5 = Eout4
 
 Eout5 = mach_zender_interferometer_def.propagate1(wavel, no, oplcommon1, oplcommon2, Ein5)
 Ein6 = Eout5
 
 Eout_port1 = Ein6[0,0]
 
 
 power_11 = (np.abs(Eout_port1))**2
 PP1col[(ii)] = power_11

 #P1_phase = 

 
 Eout_port_2 = Ein6[1,0]
 power_22 = (np.abs(Eout_port_2))**2
 PP2col[(ii)] = power_22
 

fig = plt.figure(figsize = (10,6), facecolor='lightblue')

ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2, sharey=ax1)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4, sharey=ax3)

ax1.plot(wlcol,PP1col)

ax2.plot(wlcol,PP2col)

ax3.set_xlabel("Wavelength")
ax4.set_xlabel("Wavelength")

plt.show()


