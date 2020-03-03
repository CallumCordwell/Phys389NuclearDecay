import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time

from MonteCarlo import ObjectMonteCarlo
from ParticleClass import Nuclei, RadioNuclei
start_time = time.time()
def creation():
    global t
    global Particles
    global Names
    global Tend
    t = 1000
    i = 0
    Tend = 10000
    Particles = np.array([])
    Names = np.array([])
    while i<10:
        Particles =np.append(Particles,[RadioNuclei('14C')])
        Names = np.append(Names, Particles[i].name)
        i+=1

def timeloop(Nucleus, t, path=0):
    if Nucleus.stable:
        return Nucleus , 0
    else:
        Nucleus , DEnergy = Nucleus.decay(path)
        return Nucleus , DEnergy

TotalE = 0
N=0
NT=1000
DataArray = np.array([['0','1','2','3','4','5','6','7','8','9']])
while N<NT:
    creation()
    T=t
    while T<Tend:
        i=0
        for cell in Particles:
            Particles[i], DEnergy = timeloop(cell,T)
            Names[i] = Particles[i].name
            TotalE +=DEnergy
            i+=1
        T+=t
        DataArray = np.append(DataArray,[Names] ,axis=0)
    N+=1
print(TotalE)

D = pd.DataFrame(DataArray)
D.to_csv('NucDecay.csv')
"""
plt.plot(Array)
plt.title('Decay of a single Carbon 14 nuclei using Monte Carlo method')
plt.xlabel('Attempt number')
plt.ylabel('Time to decay, years')
plt.show()

"""

print("--- %s seconds ---" % (time.time() - start_time))
