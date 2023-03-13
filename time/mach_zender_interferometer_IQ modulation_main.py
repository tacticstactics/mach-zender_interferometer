
import numpy as np
import matplotlib.pyplot as plt

import mach_zender_interferometer_time_def

print('')
print('mach-zender_interferometer_IQ modulation_main.py')
print('')


wl = 0.633; #wavelength in um

samplerate = 2048 # Sampling Frequency. [Hz]
stept = 1/samplerate

amp_c1 = 2.5
freq_am1 = 5 # [Hz]
md = 1 # modulation depth. 1 = 100 %
dc_offset1 = 2.1 # DC offset


amp_c2 = 2.5
freq_am2 = 5 # [Hz]
md = 1 # modulation depth. 1 = 100 %
dc_offset2 = 2.1 # DC offset



no = 1 # Refractive Index of medium

#
oplcommon1=100 #Common Path Length 1
oplcommon2=100 #Common Path Length 2

opl1 =100 
opl2= 100
# Optical Path Length Difference (opl1-opl2) determines free spectral range as optical filter.


PT1 = 0.5 # PT: Power Transmission of first beam splitter
PT2_1 = 0.5 # PT: Power Transmission of second beam splitter
PT2_2 = 0.5 # PT: Power Transmission of second beam splitter

PT3_1 = 0.5 # PT: Power Transmission of second beam splitter
PT3_2 = 0.5 # PT: Power Transmission of second beam splitter

PT4 = 0.5 # PT: Power Transmission of first beam splitter

# Define Input Electric Field

# Input: Port 1 only
E1in = np.array([[1+0.0000j],[0-0.0000j]])
print(E1in)
#Ein1 = np.array([[0.707+0.707j],[0]])

# Input Both 1 and 2 port
#Ein1 = np.array([[1+0j],[1-0j]]) 
#Ein1 = np.array([[0.707+0.707j],[-0.707-0.707j]])
#Ein1 = np.array([[1 + 0j],[-1 - 0j]])

# Input Port 2 only
#Ein1 = np.array([[0],[1]]) 
#Ein1 = np.array([[0],[0.707+0.707j]])

tcol = np.zeros(samplerate)
signal1col = np.zeros(samplerate)
signal2col = np.zeros(samplerate)

P1_powercol = np.zeros(samplerate)
P1_phasecol = np.zeros(samplerate)

P2_powercol = np.zeros(samplerate)
P2_phasecol = np.zeros(samplerate)


for ii in range(samplerate):
    
    t = stept * ii
    tcol[ii] = t

    
    E1out = mach_zender_interferometer_time_def.propagate1(wl, no, oplcommon1, oplcommon2, E1in)
    E2in = E1out
    
    E2out = mach_zender_interferometer_time_def.beamsplitter(PT1, E2in)
    E3_1in = E2out


    #Arm 1

    E3_1out = mach_zender_interferometer_time_def.beamsplitter(PT2_1, E3_1in)
    
    #print(E3_1out)
    #print("")

    E4_1in = E3_1out

    signal1 = amp_c1 * np.sin(2 * np.pi * freq_am1 * t) + dc_offset1
    signal1col[ii] = signal1  


    E4_1out = mach_zender_interferometer_time_def.propagate1(wl, no, opl1, opl2+signal1, E4_1in) # Each path experience different path length
    E5_1in = E4_1out
    
    E5_1out = mach_zender_interferometer_time_def.beamsplitter(PT2_2, E5_1in) # Each path enter second beam splitter
    E6_1in = E5_1out
    
    #Arm 2
    
    E3_2in = E2out
    
    signal2 = amp_c2 * np.sin(2 * np.pi * freq_am2 * t) + dc_offset2
    signal2col[ii] = signal2

    
    
    #


    E6_1out = mach_zender_interferometer_time_def.propagate1(wl, no, oplcommon1, oplcommon2, E6_1in)
    E7in = E6_1out
    
    Eout_port1 = E7in[0,0] 
    power_11 = (np.abs(Eout_port1))**2 # Optical power is calculated as square of absolute electric field strength
    P1_powercol[ii] = power_11
    
    P1_phase = np.angle(power_11)
    P1_phasecol[ii] = P1_phase
    
    Eout_port_2 = E7in[1,0]
    power_22 = (np.abs(Eout_port_2))**2
    
    P2_powercol[ii] = power_22
    
    P2_phase = np.angle(power_22)
    P2_phasecol[ii] = P2_phase
 
 

fig = plt.figure(figsize = (10,6), facecolor='lightblue')

ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

ax1.plot(tcol,signal1col)
#ax1.set_ylim(-3,3)

ax2.plot(tcol,P1_powercol,tcol,P2_powercol)

ax2.set_ylabel("Power")
ax2.set_ylim(0,1.1)
ax2.grid()

ax3.plot(tcol,P1_phasecol,tcol,P2_phasecol)
ax3.set_xlabel("time [s]")
ax3.set_ylabel("Angle")
ax3.set_ylim(-2,2)
ax3.grid()

plt.show()


