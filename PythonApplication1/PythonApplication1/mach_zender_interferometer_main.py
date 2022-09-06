
import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

import mach_zender_interferometer_def

print('')
print('mach-zender_interferometer_main.py')
print('')

m = 512

no = 1
#ne = 1.1

oplcommon1=100
oplcommon2=100

opl1 = 10
opl2= 1000

wl0 = 0.633; #um
stepwl = 0.00003; # um

PT1 = 0.5 # PT: Power Transmission
PT2 = 0.49 # PT: Power Transmission

# Input Port 1 only
#Ein1 = np.array([[1+0.0000j],[0-0.0000j]])
#Ein1 = np.array([[0.707+0.707j],[0]])

# Input Both 1 and 2 port
Ein1 = np.array([[1+0j],[1-0j]]) #Both 1 and 2 port
#Ein1 = np.array([[0.707+0.707j],[-0.707-0.707j]]) #Both 1 and 2 port

# Input Port 2 only
#Ein1 = np.array([[0],[1]]) 
#Ein1 = np.array([[0],[0.707+0.707j]])

wlcol = np.zeros((m,1));

P1_powercol = np.zeros((m,1));
P1_phasecol = np.zeros((m,1));

P2_powercol = np.zeros((m,1));
PP2col = np.zeros((m,1));
P2_phasecol = np.zeros((m,1));



for ii in range(m):
 wl = wl0 + ii * stepwl
 wlcol[(ii)] =wl

 Eout1 = mach_zender_interferometer_def.propagate1(wl, no, oplcommon1, oplcommon2, Ein1)
 Ein2 = Eout1
 
 Eout2 = mach_zender_interferometer_def.beamsplitter(PT1, Ein2)
 Ein3 = Eout2
 
 Eout3 = mach_zender_interferometer_def.propagate1(wl, no, opl1, opl2, Ein3) 
 Ein4 = Eout3
 
 Eout4 = mach_zender_interferometer_def.beamsplitter(PT2, Ein4) 
 Ein5 = Eout4
 
 Eout5 = mach_zender_interferometer_def.propagate1(wl, no, oplcommon1, oplcommon2, Ein5)
 Ein6 = Eout5
 
 Eout_port1 = Ein6[0,0]
  
 power_11 = (np.abs(Eout_port1))**2
 P1_powercol[(ii)] = power_11
 
 P1_phase = cmath.phase(power_11)
 P1_phasecol[(ii)] = P1_phase
 
 Eout_port_2 = Ein6[1,0]
 power_22 = (np.abs(Eout_port_2))**2
 PP2col[(ii)] = power_22
 P2_powercol[(ii)] = power_22

 P2_phase = cmath.phase(power_22)
 P2_phasecol[(ii)] = P2_phase
 
 

fig = plt.figure(figsize = (10,6), facecolor='lightblue')

ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2, sharey=ax1)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4, sharey=ax3)

ax1.plot(wlcol,P1_powercol,wlcol,P2_powercol)

ax1.set_ylabel("Power")
ax1.set_ylim(0,2)
ax1.grid()

ax3.plot(wlcol,P1_phasecol,wlcol,P2_phasecol)
ax4.plot()



ax3.set_xlabel("Wavelength")
ax4.set_xlabel("Wavelength")
ax3.set_ylabel("Phase")


plt.show()


