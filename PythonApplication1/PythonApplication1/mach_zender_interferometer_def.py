#mach_zender_interferometer_def.py

import numpy as np

def proc1(param=0.01,m=512):


    rscol = np.zeros((m,1))


    return rscol



def beamsplitter(T=0.5,Ein=np.array([[1],[0]])):

     R=1-T

     BS1 = np.array([[R],[1]],[[R],[1]])
       
     Eout=np.dot(BS1,Ein)

     return Eout