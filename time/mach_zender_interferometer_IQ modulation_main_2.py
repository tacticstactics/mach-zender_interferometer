
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
stept = 0.5 * 1e-15 #[s]
tcol = np.linspace(0.0, stept * samplerate, samplerate, endpoint=False)


freq_rf1 = 1e12 # [Hz]
amp_sine = 0.5*np.pi



#sinesignal
dc_offset = 0.5*np.pi # DC offset
sine_signalcol = np.zeros(samplerate)
for ii in range(samplerate):       
    t = tcol[ii]
    sinesignal = amp_sine * np.sin(2 * np.pi * freq_rf1 * t) + dc_offset
    sine_signalcol[ii] = sinesignal  

#prbs
amp_prbs = 1*np.pi


# Random_signal generation

a_range = [0, 10]
a = np.random.rand(samplerate) * (a_range[1]-a_range[0]) + a_range[0] # range for amplitude

b_range = [300, 600]
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

a = np.zeros(samplerate)
j = 0
while j < samplerate:
    a[j] = amp_prbs
    a[j+1] = 0
    j = j+2

i=0
prbs1 = np.zeros(samplerate)
while b[i]<np.size(prbs1):
    k = b[i]
    prbs1[k:] = a[i]
    i=i+1

#-----

b2_range = [300, 600]
b2 = np.random.rand(samplerate) *(b2_range[1]-b2_range[0]) + b2_range[0] # range for frequency
b2 = np.round(b2)
b2 = b2.astype(int)

b2[0] = 0

for i in range(1,np.size(b2)):
    b2[i] = b2[i-1]+b2[i]

i=0
random_signal2 = np.zeros(samplerate)
while b[i]<np.size(random_signal2):
    k = b2[i]
    random_signal2[k:] = a[i]
    i=i+1

a = np.zeros(samplerate)
j = 0
while j < samplerate:
    a[j] = amp_prbs
    a[j+1] = 0
    j = j+2

i=0
prbs2 = np.zeros(samplerate)
while b[i]<np.size(prbs2):
    k = b2[i]
    prbs2[k:] = a[i]
    i=i+1


#----

#randomintcol = np.zeros(samplerate)
#for ii in range(samplerate):
#    randomintcol[ii] = np.random.random_integers(2)



#signal1col = sine_signalcol
#signal1col = random_signal
#signal1col = prbs1
signal1col = np.zeros(samplerate)
#signal1col = randomintcol

#signal2col = sine_signalcol
#signal2col = random_signal
signal2col = prbs2
#signal2col = np.zeros(samplerate)


#
oplcommon1=0 #Common Path Length 1
oplcommon2=0 #Common Path Length 2

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

IPB1 = 0.5 * np.pi #In Phase Bias: Optical Phase delay between Arm A and B
IPB2 = 0.5 * np.pi #In Phase Bias: Optical Phase delay between Arm A and B

# Define Input Electric Field

# Input: Port 1 only
E1in = np.array([[1+0.00j],[0-0.00j]])
#Ein1 = np.array([[0.707+0.707j],[0]])

# Input Both 1 and 2 port
#Ein1 = np.array([[1+0j],[1-0j]]) 
#Ein1 = np.array([[0.707+0.707j],[-0.707-0.707j]])
#Ein1 = np.array([[1 + 0j],[-1 - 0j]])

# Input Port 2 only
#Ein1 = np.array([[0],[1]]) 
#Ein1 = np.array([[0],[0.707+0.707j]])

E7out_p1_col = np.zeros(samplerate)
E7out_p2_col = np.zeros(samplerate)

P1_powercol = np.zeros(samplerate)
P2_powercol = np.zeros(samplerate)

E9out_p1_col = np.zeros(samplerate)
E9out_p2_col = np.zeros(samplerate)


P9_1powercol = np.zeros(samplerate)
P9_2powercol = np.zeros(samplerate)

#Tx

for ii in range(samplerate):
        
    t = tcol[ii]
    
    E1out = mach_zender_interferometer_time_def.propagate1(oplcommon1, oplcommon2, E1in)
    E2in = E1out
    
    E2out = mach_zender_interferometer_time_def.beamsplitter(PT1, E2in)
    E3_1in = np.array([[E2out[0,0]],[0+0j]])

    #Arm 1

    E3_1out = mach_zender_interferometer_time_def.beamsplitter(PT2_1, E3_1in)
    
    #print(E3_1out)
    #print("")

    E4_1in = E3_1out
    
    opl1 = 2*np.pi * freq1 * t

    signal1 = signal1col[ii]  


    E4_1out = mach_zender_interferometer_time_def.propagate1(opl1, opl1+signal1, E4_1in) # Each path experience different path length
    E5_1in = E4_1out
    
    E5_1out = mach_zender_interferometer_time_def.beamsplitter(PT3_1, E5_1in) # Each path enter second beam splitter
    E6_1in = E5_1out

    E6_1out = mach_zender_interferometer_time_def.propagate1(0, 0, E6_1in) # no delay for arm A


    #Arm 2

    #E3_2in = np.array([[0+0j], [E2out[1,0]]])
    E3_2in = np.array([[E2out[1,0]], [0+0j]])   

    E3_2out = mach_zender_interferometer_time_def.beamsplitter(PT2_2, E3_2in)
    E4_2in = E3_2out
 
    #signal2 = amp_c2 * np.sin(2 * np.pi * freq_am2 * t + phase_IQ) + dc_offset2
    signal2 = signal2col[ii]    
    

    E4_2out = mach_zender_interferometer_time_def.propagate1(opl1, opl1+signal2, E4_2in) # Each path experience different path length
    E5_2in = E4_2out

    E5_2out = mach_zender_interferometer_time_def.beamsplitter(PT3_2, E5_2in) # Each path enter second beam splitter
    E6_2in = E5_2out

    E6_2out = mach_zender_interferometer_time_def.propagate1(IPB1, IPB1, E6_2in) # Delay for arm B. Actually only one path couple to fourth beam splitter
    
    # Combine I + Q using fourth beam splitter

    E7_in = np.array([[E6_1out[0,0]], [E6_2out[0,0]]])


    E7_out = mach_zender_interferometer_time_def.beamsplitter(PT4, E7_in) # Each path enter second beam splitter
    
    E7out_port1 = E7_out[0,0] #trans
    E7out_p1_col[ii] = E7out_port1

    # power_11 = (np.abs(E7out_port1))**2 # Optical power is calculated as square of absolute electric field strength
    # P1_powercol[ii] = power_11    
  

    E7out_port2 = E7_out[1,0] #reflect
    E7out_p2_col[ii] = E7out_port2
    # power_22 = (np.abs(E7out_port2))**2    
    # P2_powercol[ii] = power_22
 
    #Rx 

    E8_in = E7out_port1

    E8_out = mach_zender_interferometer_time_def.beamsplitter(PT5, E8_in) # Each path enter second beam splitter   
    
    #Local Oscillator
    losc_I_phase = 2*np.pi * freq1 * t
    losc_Q_phase = losc_I_phase - IPB2

    Elosc_I = mach_zender_interferometer_time_def.propagate1(losc_I_phase, losc_I_phase, np.array([[0.5+0.0000j],[0-0.0000j]]))
    # Actually only one path couple to fourth beam splitter
    # 
    Elosc_Q = mach_zender_interferometer_time_def.propagate1(losc_Q_phase, losc_Q_phase, np.array([[0.5+0.0000j],[0-0.0000j]]))

    E9_1in = np.array([[E8_out[0,0]], [Elosc_I[0,0]]])
    E9_2in = np.array([[E8_out[1,0]], [Elosc_Q[0,0]]])

    E9_1out = mach_zender_interferometer_time_def.beamsplitter(PT6_1, E9_1in) # Each path enter second beam splitter   
    
    E9_2out = mach_zender_interferometer_time_def.beamsplitter(PT6_2, E9_2in) # Each path enter second beam splitter

    E9_1out_port1 = E9_1out[0,0] #trans
    E9out_p1_col[ii] = E9_1out_port1

    E9_2out_port1 = E9_2out[0,0] #trans
    E9out_p2_col[ii] = E9_2out_port1

    #P9_1power = (np.abs(E9_1out_port1))**2 # Optical power is calculated as square of absolute electric field strength
    #P9_1powercol[ii] = P9_1power

    #P9_2power = (np.abs(E9_2out_port1))**2 # Optical power is calculated as square of absolute electric field strength
    #P9_2powercol[ii] = P9_2power
   


fig1 = plt.figure(figsize = (10,6), facecolor='lightblue')

ax1 = fig1.add_subplot(4, 1, 1)
ax2 = fig1.add_subplot(4, 1, 2)
ax3 = fig1.add_subplot(4, 1, 3)
ax4 = fig1.add_subplot(4, 1, 4)

ax1.plot(tcol,signal1col, ".-", color="c")
#ax1.set_ylim(-1*np.pi,np.pi)
ax1.grid()


ax2.plot(tcol,signal2col, ".-",color="y")
#ax2.set_ylim(-1*np.pi,np.pi)
#ax2.set_ylabel("Power")
ax2.grid()

ax3.plot(tcol,np.real(E7out_p1_col), ".-",color="m")
ax3.set_ylim(-1.1,1.1)
ax3.set_ylabel("Electric Field")
ax3.grid()

ax4.plot(tcol,np.real(E7out_p2_col), ".-",color="m")
ax4.set_ylim(-1.1,1.1)
ax4.set_ylabel("Electric Field")
ax4.grid()


fig2 = plt.figure(figsize = (10,6), facecolor='lightblue')

ax21 = fig2.add_subplot(4, 1, 1)
ax22 = fig2.add_subplot(4, 1, 2)
ax23 = fig2.add_subplot(4, 1, 3)
ax24 = fig2.add_subplot(4, 1, 4)

ax23.plot(tcol, np.real(E9out_p1_col), ".-",color="m")
ax23.set_ylim(-1.1,1.1)
ax23.grid()

ax24.plot(tcol, np.real(E9out_p2_col), ".-",color="m")
ax24.set_ylim(-1.1,1.1)
ax24.grid()

plt.show()