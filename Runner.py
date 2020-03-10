import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time

from MonteCarlo import ObjectMonteCarlo
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
    while i<20:
        Particles =np.append(Particles,[RadioNuclei('14C')])
        Names = np.append(Names, Particles[i].name)
        i+=1

def timeloop(Nucleus, t, path=0):
    if Nucleus.stable:
        return Nucleus , 0
    else:
        if ObjectMonteCarlo(Nucleus,t):
            Nucleus , DEnergy = Nucleus.decay(path)
            return Nucleus , DEnergy
    return Nucleus , 0

t = 1000
Tend = 30000
EndEnergy = np.array([])
Stability = np.zeros([(int(Tend/t)),2]) #+1 as the time step starts at 0, remove if starting at T=t

N=0
NT=100
DataArray = np.empty([20])
DataArray = [DataArray]
while N<NT:
    reset()
    T=0
    while T<Tend:
        i=0
        if not T==0:
            for cell in Particles:
                Particles[i], DE = timeloop(cell,t)
                Names[i] = Particles[i].name
                DEnergy +=DE
                i+=1
        
        DataArray = np.append(DataArray,[Names] ,axis=0)
        Energy=np.append(Energy,DEnergy)
        DEnergy=0
        #Each time step data averaged over the whole Monte Carlo Sim
        i=0
        Stability[int(T/t)][1] = T
        for cell in Particles:
            if Particles[i].stable:
                pass 
            else:
                Stability[int(T/t)][0] += 1 
            i+=1
        T+=t

    #End of each Monte Carlo loop data
    EndEnergy = np.append(EndEnergy, np.sum(Energy))
    N+=1

DataArray = np.delete(DataArray,0,0)
Stability[:,0] /=NT

print(np.mean(EndEnergy))
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
