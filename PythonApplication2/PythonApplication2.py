
import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

import mach_zender_interferometer_def

print('')
print('mach-zender_interferometer_timedomain.py')
print('')

m = 512


samplerate = 4096
# サンプリング周波数


#len_wave = len(wave)
#print('Length of wave = ')
#print(len_wave)
#print('')


no = 1 # Refractive Index of medium

oplcommon1=100 #Common Path Length 1
oplcommon2=100 #Common Path Length 2

opl1 =100 
opl2= 100
# Optical Path Length Difference (opl1-opl2) determines free spectral range as optical filter.

wl = 0.633; #wavelength in um


PT1 = 0.5 # PT: Power Transmission of first beam splitter
PT2 = 0.5 # PT: Power Transmission of second beam splitter

# Define Input Electric Field

# Input Port 1 only
Ein1 = np.array([[1+0.0000j],[0-0.0000j]])
#Ein1 = np.array([[0.707+0.707j],[0]])

# Input Both 1 and 2 port
#Ein1 = np.array([[1+0j],[1-0j]]) 
#Ein1 = np.array([[0.707+0.707j],[-0.707-0.707j]])
#Ein1 = np.array([[1 + 0j],[-1 - 0j]])

# Input Port 2 only
#Ein1 = np.array([[0],[1]]) 
#Ein1 = np.array([[0],[0.707+0.707j]])

tcol = np.zeros((samplerate,1));
signalcol = np.zeros((samplerate,1));

P1_powercol = np.zeros((samplerate,1));
P1_phasecol = np.zeros((samplerate,1));

P2_powercol = np.zeros((samplerate,1));
P2_phasecol = np.zeros((samplerate,1));

stept = 1/samplerate

amp_c = 1                                                       # キャリア振幅
freq_c = 10                                                     # キャリア周波数
freq_am = 2                                                     # 変調周波数
md = 0.9                                                         # 振幅変調指数(0<=m<=1)

for ii in range(samplerate):
    
    t = stept * ii
    tcol[(ii)] = t

    signal = np.sin(2 * np.pi * freq_am * t)                             # 変調波(<=1)
    signalcol[(ii)] = signal

    wave = amp_c * (1 + md * signal) * np.cos(2 * np.pi * freq_c * t) 
    
    Eout1 = mach_zender_interferometer_def.propagate1(wl, no, oplcommon1, oplcommon2, Ein1)
    Ein2 = Eout1
    
    Eout2 = mach_zender_interferometer_def.beamsplitter(PT1, Ein2)
    Ein3 = Eout2
    
    Eout3 = mach_zender_interferometer_def.propagate1(wl, no, opl1, opl2+wave, Ein3) # Each path experience differnt path length
    Ein4 = Eout3
    
    Eout4 = mach_zender_interferometer_def.beamsplitter(PT2, Ein4) # Each path enter second beam splitter
    Ein5 = Eout4
    
    Eout5 = mach_zender_interferometer_def.propagate1(wl, no, oplcommon1, oplcommon2, Ein5)
    Ein6 = Eout5
    
    Eout_port1 = Ein6[0,0] 
    power_11 = (np.abs(Eout_port1))**2 # Optical power is calculated as square of absolute electric field strength
    P1_powercol[(ii)] = power_11
    
    P1_phase = cmath.phase(power_11)
    P1_phasecol[(ii)] = P1_phase
    
    Eout_port_2 = Ein6[1,0]
    power_22 = (np.abs(Eout_port_2))**2
    
    P2_powercol[(ii)] = power_22
    
    P2_phase = cmath.phase(power_22)
    P2_phasecol[(ii)] = P2_phase
 
 

fig = plt.figure(figsize = (10,4), facecolor='lightblue')

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

ax1.plot(tcol,P1_powercol,tcol,P2_powercol)
ax1.set_xlabel("time")
ax1.set_ylabel("Power")
ax1.set_ylim(0,2)
ax1.grid()

ax2.plot(tcol,P1_phasecol,tcol,P2_phasecol)
ax2.set_xlabel("time")
ax2.set_ylabel("Phase")
ax2.set_ylim(-2,2)
ax2.grid()

plt.show()


