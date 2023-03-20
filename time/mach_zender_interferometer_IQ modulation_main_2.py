
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c 

import mach_zender_interferometer_time_def

print('')
print('mach-zender_interferometer_IQ modulation_main.py')
print('')

wl1 = 1550e-9
freq1 = c / wl1

samplerate = 16384 # NUmber of Points
stept = 1/samplerate

tcol = np.linspace(0.0, stept * samplerate, samplerate, endpoint=False)

freq_am1 = 5 # [Hz]
amp_c1 = 0.5*np.pi
dc_offset1 = 0.5*np.pi # DC offset


freq_am2 = 10 # [Hz]
amp_c2 = 0.5*np.pi
dc_offset2 = 0.5 * np.pi # DC offset

#

phase_IQ = 0.5*np.pi # RF Phase delay between I and Q signal

IPB = 1*np.pi #In Phase Bias: Optical Phase delay between Arm a and B


no = 1 # Refractive Index of medium

#
oplcommon1=100 #Common Path Length 1
oplcommon2=100 #Common Path Length 2

#opl1 =100 
#opl2= 100
# Optical Path Length Difference (opl1-opl2) determines free spectral range as optical filter.



PT1 = 0.5 # PT: Power Transmission of first beam splitter

PT2_1 = 0.5 # PT: Power Transmission of second beam splitter of arm A
PT2_2 = 0.5 # PT: Power Transmission of second beam splitter of arm B

PT3_1 = 0.5 # PT: Power Transmission of third beam splitter of arm A
PT3_2 = 0.5 # PT: Power Transmission of third beam splitter of arm B

PT4 = 0.5 # PT: Power Transmission of 4th beam splitter
PT5 = 0.5 # PT: Power Transmission of 5th beam splitter

PT6_1 = 0.5 # PT: Power Transmission of 5th beam splitter
PT6_2 = 0.5 # PT: Power Transmission of 5th beam splitter

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

t_rx_col = np.zeros(samplerate)

signal1col = np.zeros(samplerate)
signal2col = np.zeros(samplerate)

E7_col = np.zeros(samplerate)

P1_powercol = np.zeros(samplerate)
P2_powercol = np.zeros(samplerate)

P9_1powercol = np.zeros(samplerate)
P9_2powercol = np.zeros(samplerate)

#Tx

for ii in range(samplerate):
        
    t = tcol[ii]
    
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
    
    opl1 = 2*np.pi * freq1 * t


    signal1 = amp_c1 * np.sin(2 * np.pi * freq_am1 * t) + dc_offset1
    signal1col[ii] = signal1  


    E4_1out = mach_zender_interferometer_time_def.propagate1(opl1, opl1+signal1, E4_1in) # Each path experience different path length
    E5_1in = E4_1out
    
    E5_1out = mach_zender_interferometer_time_def.beamsplitter(PT3_1, E5_1in) # Each path enter second beam splitter
    E6_1in = E5_1out

    E6_1out = mach_zender_interferometer_time_def.propagate1(0, 0, E6_1in) # no delay


    #Arm 2

    E3_2in = np.array([[E2out[1,0]],[0+0j]])
    
    #print("E3_2in")
    #print(E3_2in)
    #print("")

    E3_2out = mach_zender_interferometer_time_def.beamsplitter(PT2_2, E3_2in)

    E4_2in = E3_2out

 
    signal2 = amp_c2 * np.sin(2 * np.pi * freq_am2 * t + phase_IQ) + dc_offset2
    signal2col[ii] = signal2    
    

    E4_2out = mach_zender_interferometer_time_def.propagate1(opl1, opl1+signal2, E4_2in) # Each path experience different path length
    E5_2in = E4_2out

    E5_2out = mach_zender_interferometer_time_def.beamsplitter(PT3_2, E5_2in) # Each path enter second beam splitter
    E6_2in = E5_2out

    E6_2out = mach_zender_interferometer_time_def.propagate1(IPB, IPB, E6_2in) # Actually only one path couple to fourth beam splitter
    
    # Combine I + Q using fourth beam splitter

    E7_in = np.array([[E6_1out[0,0]], [E6_2out[0,0]]])

    #print("E7_in")
    #print(E7_in)
    #print("")


    E7_out = mach_zender_interferometer_time_def.beamsplitter(PT4, E7_in) # Each path enter second beam splitter
    
    E7out_port1 = E7_out[0,0] #trans
    E7_col[ii] = E7out_port1

    power_11 = (np.abs(E7out_port1))**2 # Optical power is calculated as square of absolute electric field strength
    P1_powercol[ii] = power_11    
  

    E7out_port_2 = E7_out[1,0] #reflect
    power_22 = (np.abs(E7out_port_2))**2
    
    P2_powercol[ii] = power_22   
    

 
#Rx 

for ii in range(samplerate):
    
    t2 = stept * ii
    t_rx_col[ii] = t2

    E8_in = E7_col[ii]

    E8_out = mach_zender_interferometer_time_def.beamsplitter(PT5, E8_in) # Each path enter second beam splitter   
    
    losc_I_phase = 2*np.pi * freq1 * t2
    losc_Q_phase = losc_I_phase + 0.5*np.pi

    Elosc_I = mach_zender_interferometer_time_def.propagate1(losc_I_phase, losc_I_phase, np.array([[1+0.0000j],[0-0.0000j]]))
    # Actually only one path couple to fourth beam splitter
    # 
    Elosc_Q = mach_zender_interferometer_time_def.propagate1(losc_Q_phase, losc_Q_phase, np.array([[1+0.0000j],[0-0.0000j]]))

    E9_1in = np.array([[E8_out[0,0]],[Elosc_Q[0,0]]])
    E9_2in = np.array([[E8_out[1,0]],[Elosc_I[0,0]]])

    E9_1out = mach_zender_interferometer_time_def.beamsplitter(PT6_1, E9_1in) # Each path enter second beam splitter   
    
    E9_2out = mach_zender_interferometer_time_def.beamsplitter(PT6_2, E9_2in) # Each path enter second beam splitter

    E9_1out_port1 = E9_1out[0,0] #trans


    E9_2out_port1 = E9_2out[0,0] #trans

    P9_1power = (np.abs(E9_1out_port1))**2 # Optical power is calculated as square of absolute electric field strength
    P9_1powercol[ii] = P9_1power

    P9_2power = (np.abs(E9_2out_port1))**2 # Optical power is calculated as square of absolute electric field strength
    P9_2powercol[ii] = P9_2power
   


fig1 = plt.figure(figsize = (10,6), facecolor='lightblue')

ax1 = fig1.add_subplot(4, 1, 1)
ax2 = fig1.add_subplot(4, 1, 2)
ax3 = fig1.add_subplot(4, 1, 3)
ax4 = fig1.add_subplot(4, 1, 4)

ax1.plot(tcol,signal1col, ".-", color="c")
ax1.set_ylim(-1*np.pi,np.pi)
ax1.grid()


ax2.plot(tcol,signal2col, ".-",color="y")
ax2.set_ylim(-1*np.pi,np.pi)
#ax2.set_ylabel("Power")
ax2.grid()

ax3.plot(tcol,P1_powercol, ".-",color="m")
ax3.set_ylim(-0.1,1.1)
ax3.grid()

ax4.plot(tcol,P2_powercol, ".-",color="m")
ax4.set_ylim(-0.1,1.1)
ax4.grid()


fig2 = plt.figure(figsize = (10,6), facecolor='lightblue')

ax21 = fig2.add_subplot(4, 1, 1)
ax22 = fig2.add_subplot(4, 1, 2)
ax23 = fig2.add_subplot(4, 1, 3)
ax24 = fig2.add_subplot(4, 1, 4)

ax23.plot(tcol,P9_1powercol, ".-",color="m")
ax23.set_ylim(-0.1,1.1)
ax23.grid()

ax24.plot(tcol,P9_2powercol, ".-",color="m")
ax24.set_ylim(-0.1,1.1)
ax24.grid()


plt.show()




