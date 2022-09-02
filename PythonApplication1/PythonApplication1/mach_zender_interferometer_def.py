#mach_zender_interferometer_def.py

import math
import numpy as np


def propagate1(wavel=1.55e-6,no=1,opl=1,Ein=np.array([[1],[0]])):

    T11 = np.array([[np.exp(1j*wavel*no*opl),0],[0,np.exp(1j*wavel*no*opl)]]);

    Eout = np.dot(T11,Ein)

    return Eout



def dielectric_beamsplitter(PT=0.5,Ein=np.array([[1],[0]])):

     phiT = 0
     PhiR = 0
     phiO = 0


     T = np.sqrt(PT)

     PR = 1-PT

     R = np.sqrt(PR)

     Theta1 = np.arctan(R/T) #Radian
     
     print('')

     print('Theta1 = ')
     print(Theta1)

     print('')
     
     # https://en.wikipedia.org/wiki/Beam_splitter

     deBS1 = np.array([[math.sin(Theta1),math.cos(Theta1)],[math.cos(Theta1),-1*math.sin(Theta1)]])
       
     Eout = np.dot(deBS1,Ein)

     return Eout


 def Loudon_beamsplitter(PT=0.5,Ein=np.array([[1],[0]])):

     phiT = 0
     PhiR = -0.5*np.pi
     phiO = 0.5 * np.pi


     T = np.sqrt(PT)

     PR = 1-PT

     R = np.sqrt(PR)

     Theta1 = np.arctan(R/T) #Radian
     
     print('')

     print('Theta1 = ')
     print(Theta1)

     print('')
     
     # https://en.wikipedia.org/wiki/Beam_splitter

     LoudonBS1 = np.array([[math.sin(Theta1),math.cos(Theta1)],[math.cos(Theta1),-1*math.sin(Theta1)]])
       
     Eout=np.dot(LoudonBS1,Ein)

     return Eout
