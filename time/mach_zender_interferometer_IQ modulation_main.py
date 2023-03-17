
import numpy as np
import matplotlib.pyplot as plt

import mach_zender_interferometer_time_def

print('')
print('mach-zender_interferometer_IQ modulation_main.py')
print('')


samplerate = 2048 # Sampling Frequency. [Hz]
stept = 1/samplerate

freq_am1 = 5 # [Hz]
amp_c1 = 0.5*np.pi
dc_offset1 = 0.5*np.pi # DC offset


freq_am2 = 5 # [Hz]
amp_c2 = 0.5*np.pi
dc_offset2 = 0.5 * np.pi # DC offset

phase_IQ = 1*np.pi # Electric Phase delay between I and Q

IPB = 1*np.pi #In Phase Bias. Optical Phase dela between arm a and B


no = 1 # Refractive Index of medium

#
oplcommon1=100 #Common Path Length 1
oplcommon2=100 #Common Path Length 2

opl1 =100 
opl2= 100
# Optical Path Length Difference (opl1-opl2) determines free spectral range as optical filter.



PT1 = 0.5 # PT: Power Transmission of first beam splitter

PT2_1 = 0.5 # PT: Power Transmission of second beam splitter of arm A
PT2_2 = 0.5 # PT: Power Transmission of second beam splitter of arm B

PT3_1 = 0.5 # PT: Power Transmission of third beam splitter of arm A
PT3_2 = 0.5 # PT: Power Transmission of third beam splitter of arm B

PT4 = 0.5 # PT: Power Transmission of 4th beam splitter

# Define Input Electric Field

# Input: Port 1 only
E1in = np.array([[1+0.0000j],[0-0.0000j]])
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
    
    E1out = mach_zender_interferometer_time_def.propagate1(oplcommon1, oplcommon2, E1in)
    E2in = E1out
    
    E2out = mach_zender_interferometer_time_def.beamsplitter(PT1, E2in)
    E3_1in = np.array([[E2out[0,0]],[0+0j]])

    #print("E3_1in")
    #print(E3_1in)
    #print("")

    #Arm 1

    E3_1out = mach_zender_interferometer_time_def.beamsplitter(PT2_1, E3_1in)
    
    #print(E3_1out)
    #print("")

    E4_1in = E3_1out

    signal1 = amp_c1 * np.sin(2 * np.pi * freq_am1 * t) + dc_offset1
    signal1col[ii] = signal1  


    E4_1out = mach_zender_interferometer_time_def.propagate1(opl1, opl2+signal1, E4_1in) # Each path experience different path length
    E5_1in = E4_1out
    
    E5_1out = mach_zender_interferometer_time_def.beamsplitter(PT3_1, E5_1in) # Each path enter second beam splitter
    E6_1in = E5_1out

    E6_1out = mach_zender_interferometer_time_def.propagate1(0, 0, E6_1in) # do not experience delay


    #Arm 2

    E3_2in = np.array([[E2out[1,0]],[0+0j]])
    
    #print("E3_2in")
    #print(E3_2in)
    #print("")

    E3_2out = mach_zender_interferometer_time_def.beamsplitter(PT2_2, E3_2in)

    E4_2in = E3_2out

 
    signal2 = amp_c2 * np.sin(2 * np.pi * freq_am2 * t + phase_IQ) + dc_offset2
    signal2col[ii] = signal2    
    

    E4_2out = mach_zender_interferometer_time_def.propagate1(opl1, opl2+signal2, E4_2in) # Each path experience different path length
    E5_2in = E4_2out

    E5_2out = mach_zender_interferometer_time_def.beamsplitter(PT3_2, E5_2in) # Each path enter second beam splitter
    E6_2in = E5_2out

    E6_2out = mach_zender_interferometer_time_def.propagate1(IPB, IPB, E6_2in) # Actually only one path couple to fourth beam splitter
    
    # Combine I + Q using fourth beam splitter

    E7_in = np.array([[E6_1out[0,0]],[E6_2out[0,0]]])

    #print("E7_in")
    #print(E7_in)
    #print("")


    E7_out = mach_zender_interferometer_time_def.beamsplitter(PT4, E7_in) # Each path enter second beam splitter

    
    Eout_port1 = E7_out[0,0] 
    power_11 = (np.abs(Eout_port1))**2 # Optical power is calculated as square of absolute electric field strength
    P1_powercol[ii] = power_11
    
    P1_phase = np.angle(power_11)
    P1_phasecol[ii] = P1_phase
    
    Eout_port_2 = E7_out[1,0]
    power_22 = (np.abs(Eout_port_2))**2
    
    P2_powercol[ii] = power_22
    
    P2_phase = np.angle(power_22)
    P2_phasecol[ii] = P2_phase
 
 

fig = plt.figure(figsize = (10,6), facecolor='lightblue')

ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

ax1.plot(tcol,signal1col, tcol,signal2col)
#ax1.set_ylim(-3,3)
ax1.grid()


ax2.plot(tcol,P1_powercol,tcol,P2_powercol)

ax2.set_ylabel("Power")
ax2.set_ylim(0,1.1)
ax2.grid()



plt.show()


