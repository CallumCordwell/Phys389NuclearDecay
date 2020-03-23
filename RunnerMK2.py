import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import MonteCarlo as MC
from ParticleClass import Nuclei, RadioNuclei
import MultiProc 

def DataPlot(array):
    """
    Plots a matplotlib graph for the given array
    Takes in an array to output a pandas dataframe and a matplotlib graph
    """
    D = pd.DataFrame(array)
    D.to_csv('NucDecay.csv')

    plt.plot(array[:,0] , array[:,1])
    plt.title('Average decay energy released for 10 atoms of C14 decay')
    plt.xlabel('Time, y')
    plt.ylabel('Average decay energy release')
    plt.show()


Particles = np.array([])
i=0
while i<10:
    Particles =np.append(Particles,[RadioNuclei('14C')])
    i+=1

MCNum = 1000
tstep=1000
Tend=15000
energy = np.zeros((int((Tend/tstep) + 1),2), dtype=float)
stability = np.zeros((int((Tend/tstep) + 1),2))

start_time = time.time()
print("Starting Threading")

energy, stability = MultiProc.CreateandRunThreads(MCNum,Tend,tstep,Particles)



print("Exiting Main Thread. Time: %s seconds" % (time.time() - start_time))
print(energy)
print(stability)

