import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import MonteCarlo as MC
from ParticleClass import Nuclei, RadioNuclei

def DataPlot(array):
<<<<<<< HEAD
    """
    Plots a matplotlib graph for the given array
    Takes in an array to output a pandas dataframe and a matplotlib graph
    """
=======
>>>>>>> parent of 255e39c... Update RunnerMK2.py
    D = pd.DataFrame(array)
    #print(Stability)
    #DataArray = np.append(DataArray, EndEnergy[:,None] ,axis=1)
    D.to_csv('NucDecay.csv')

    plt.plot(array[:,0] , array[:,1])
    plt.title('Average decay energy released for 10 atoms of C14 decay')
    plt.xlabel('Time, y')
    plt.ylabel('Average decay energy release')
    plt.show()




start_time = time.time()


MCNum = 100
tstep=1000
Tend=5000
Energy = np.zeros((int(Tend/tstep +1),2), dtype=float)
stability = np.zeros((int(Tend/tstep +1),2))


for i in range(MCNum):
    Particles = np.array([])
    for i in range(10):
        Particles =np.append(Particles,[RadioNuclei('14C')])
    
    DEnergy, LoopStability = MC.MonteCarloLoop(Tend,Particles,tstep)

    stability = np.add(stability,LoopStability)
    Energy = np.add(Energy, DEnergy)

stability /= MCNum
Energy /= MCNum

EndEnergy = np.sum(Energy[:,1])

print(Energy)
print(stability)


print("--- %s seconds ---" % (time.time() - start_time))
