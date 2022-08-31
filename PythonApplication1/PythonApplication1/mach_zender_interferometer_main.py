
import numpy as np
import matplotlib.pyplot as plt


import mach_zender_interferometer_def

param=0.1
m=256

print('')
print('mach-zender_interferometer_main.py')
print('')


rscol = mach_zender_interferometer_def.proc1(param,m)


fig = plt.figure(figsize = (10,6), facecolor='lightblue')

