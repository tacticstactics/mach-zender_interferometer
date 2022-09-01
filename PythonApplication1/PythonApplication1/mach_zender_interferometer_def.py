#mach_zender_interferometer_def.py

import math
import numpy as np


def propagate1(wavel=1.55e-6,no=1,opl=1,Ein=np.array([[1],[0]])):

    T11 = np.array([[np.exp(1j*wavel*no*opl),0],[0,np.exp(1j*wavel*no*opl)]]);

    Eout = np.dot(T11,Ein)

    return Eout



def beamsplitter(PT=0.5,Ein=np.array([[1],[0]])):

     PR = 1-PT

     Theta1 = np.arctan(PR/PT) #Radian


     BS1 = np.array([[math.sin(Theta1),math.cos(Theta1)],[math.cos(Theta1),-1*math.sin(Theta1)]])
       
     Eout=np.dot(BS1,Ein)

     return Eout