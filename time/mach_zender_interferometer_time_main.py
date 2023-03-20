
import numpy as np
import matplotlib.pyplot as plt

import mach_zender_interferometer_time_def
from scipy.constants import c 

print('')
print('mach-zender_interferometer_time_main.py')
print('')

samplerate = 16384 # NUmber of Points
stept = 0.5*1e-15

print("stept [s]")
print(f'{stept:.5E}')
print('')

tcol = np.linspace(0.0, stept * samplerate, samplerate, endpoint=False)

wl1 = 1550e-9 #wavelength [m]

freq1 = c / wl1
print("freq1 [Hz]")
print(f'{freq1:.5E}')
print("")

no = 1 # Refractive Index of medium

oplcommon1=100 #Common Path Length 1
oplcommon2=100 #Common Path Length 2

opl1 =100 
opl2= 100
# Optical Path Length Difference (opl1-opl2) determines free spectral range as optical filter. In the case of modulator, DOPL does not affect.

PT1 = 0.5 # PT: Power Transmission of first beam splitter
PT2 = 0.5 # PT: Power Transmission of second beam splitter




sine_signalcol = np.zeros(samplerate)
random_signalcol = np.zeros(samplerate)
prbs1 = np.zeros(samplerate)

#Sine signal parameters

amp_c = 2.5
freq_am = 5 # [Hz]
md = 1 # modulation depth. 1 = 100 %
dc_offset = 2.1 # DC offset

#sinesignal
for ii in range(samplerate):
    
    t = stept * ii
    tcol[ii] = t

    sinesignal = amp_c * np.sin(2 * np.pi * freq_am * t) + dc_offset
    sine_signalcol[ii] = sinesignal  



# Random signal generation

a_range = [1, 10]
a = np.random.rand(samplerate) * (a_range[1]-a_range[0]) + a_range[0] # range for amplitude

b_range = [30, 60]
b = np.random.rand(samplerate) *(b_range[1]-b_range[0]) + b_range[0] # range for frequency
b = np.round(b)
b = b.astype(int)

b[0] = 0

for i in range(1,np.size(b)):
    b[i] = b[i-1]+b[i]

i=0
random_signal = np.zeros(samplerate)
while b[i]<np.size(random_signal):
    k = b[i]
    random_signal[k:] = a[i]
    i=i+1


# prbs----

a = np.zeros(samplerate)
j = 0
while j < samplerate:
    a[j] = 4.2
    a[j+1] = 0
    j = j+2

i=0
prbs1 = np.zeros(samplerate)
while b[i]<np.size(prbs1):
    k = b[i]
    prbs1[k:] = a[i]
    i=i+1
#----


#signalcol = sine_signalcol
signalcol = random_signal
#signalcol = prbs1


#Define Input condition

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


P1_powercol = np.zeros(samplerate)
P1_phasecol = np.zeros(samplerate)

P2_powercol = np.zeros(samplerate)
P2_phasecol = np.zeros(samplerate)


for ii in range(samplerate):
    
    t = tcol[ii]
    signal = signalcol[ii]
    
    Eout1 = mach_zender_interferometer_time_def.propagate1(oplcommon1, oplcommon2, Ein1)
    Ein2 = Eout1
    
    Eout2 = mach_zender_interferometer_time_def.beamsplitter(PT1, Ein2)
    Ein3 = Eout2
    
    Eout3 = mach_zender_interferometer_time_def.propagate1(opl1, opl2+signal, Ein3) # Each path experience different path length
    Ein4 = Eout3
    
    Eout4 = mach_zender_interferometer_time_def.beamsplitter(PT2, Ein4) # Each path enter second beam splitter
    Ein5 = Eout4
    
    Eout5 = mach_zender_interferometer_time_def.propagate1(oplcommon1, oplcommon2, Ein5)
    Ein6 = Eout5
    
    Eout_port1 = Ein6[0,0] 
    power_11 = (np.abs(Eout_port1))**2 # Optical power is calculated as square of absolute electric field strength
    P1_powercol[ii] = power_11
    
    P1_phase = np.angle(power_11)
    P1_phasecol[ii] = P1_phase
    
    Eout_port_2 = Ein6[1,0]
    power_22 = (np.abs(Eout_port_2))**2
    
    P2_powercol[ii] = power_22
    
    P2_phase = np.angle(power_22)
    P2_phasecol[ii] = P2_phase
 
 

fig = plt.figure(figsize = (10,6), facecolor='lightblue')

ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

ax1.plot(tcol,signalcol, ".-")
#ax1.set_ylim(-3,3)

ax2.plot(tcol,P1_powercol,".-", tcol,P2_powercol, ".-")

ax2.set_ylabel("Power")
ax2.set_ylim(0,1.1)
ax2.grid()

ax3.plot(tcol,P1_phasecol,tcol,P2_phasecol, ".-")
ax3.set_xlabel("time [s]")
ax3.set_ylabel("Angle")
ax3.set_ylim(-2,2)
ax3.grid()

plt.show()
