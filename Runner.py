import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import MonteCarlo as MC
from ParticleClass import Nuclei, RadioNuclei

start_time = time.time()

def reset():
    global Particles
    global Names
    global DEnergy
    global Energy
    DEnergy = 0
    i = 0
    Particles = np.array([])
    Names = np.array([])
    Energy = np.array([])
    while i<10:
        Particles =np.append(Particles,[RadioNuclei('14C')])
        i+=1

t = 1000
Tend = 10000
EndEnergy = np.array([])
Stability = np.zeros([(int(Tend/t)+1),2]) #+1 as the time step starts at 0, remove if starting at T=t

N=0
NT=200
DataArray = np.empty([10])
DataArray = [DataArray]
while N<NT:
    reset()
    T=0
    
    while T<=Tend:
        instability=0
        if not T==0:
            Particles, DEnergy = MC.timestep(t,Particles)
        else:
            DEnergy = 0
        array = np.array([])
        for cell in Particles:
            array = np.append(array, cell.name)
            if not cell.stable:
                instability+=1
        DataArray = np.append(DataArray,[array],axis=0)
        Energy = np.append(Energy,DEnergy)
        Stability[int(T/t)][1] = T
        Stability[int(T/t)][0] += instability
        T+=t

    #End of each Monte Carlo loop data
    EndEnergy = np.append(EndEnergy, np.sum(Energy))
    N+=1


print(Stability)

DataArray = np.delete(DataArray,0,0)
Stability[:,0] /=NT

D = pd.DataFrame(Stability)
#print(Stability)
#DataArray = np.append(DataArray, EndEnergy[:,None] ,axis=1)
D.to_csv('NucDecay.csv')

plt.plot(Stability[:,1] , Stability[:,0])
plt.title('Average number of stable particles over time for C14 decay')
plt.xlabel('Time, y')
plt.ylabel('Average number of stable particles')
plt.show()



print("--- %s seconds ---" % (time.time() - start_time))
