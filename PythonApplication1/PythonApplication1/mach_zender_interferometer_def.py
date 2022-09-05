#mach_zender_interferometer_def.py

import math
import numpy as np



def propagate1(wavel=1.55e-6,no=1, opl1=1, opl2=1, Ein=np.array([[1],[0]])):

    propagatematrix1 = np.array([[np.exp(1j*wavel*no*opl1),0],[0,np.exp(1j*wavel*no*opl2)]]);

    Eout = np.dot(propagatematrix1,Ein)

    #Pout = np.array([[],[]])
    
    return Eout



def dielectric_beamsplitter(PT,Ein):

    #Dielectric
     #phiT = 0
     #phiR = 0
     #phiO = 0


     #Symmetric
     phiT = 0
     phiR = -0.5*np.pi
     phiO = 0.5 * np.pi


     T = np.sqrt(PT)

     PR = 1-PT

     R = np.sqrt(PR)

     Theta1 = np.arctan(R/T) #Radian
     
     #print('')
     #print('Theta1 = ')
     #print(Theta1)
     #print('')
     
     # https://en.wikipedia.org/wiki/Beam_splitter

     
     dielectricBS1 = np.dot(np.exp(1J*phiO),np.array([[math.sin(Theta1)*np.exp(1J*phiR),math.cos(Theta1)*np.exp(-1J*phiT)],[math.cos(Theta1)*np.exp(1j*phiT),-1*math.sin(Theta1)*np.exp(-1J*phiR)]]))
     
     #print('')
     #print('dielectricBS1 = ')
     #print(dielectricBS1)


     Eout = np.dot(dielectricBS1,Ein)

     return Eout
