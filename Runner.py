import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import MonteCarlo as MC
from ParticleClass import Nuclei, RadioNuclei
"""
Runs the monte carlo sim without multiprocessing using MonteCarloLoop
"""
def dataPlot(array):
    """
    Plots a matplotlib graph for the given array
    Takes in an array to output a pandas dataframe and a matplotlib graph
    """
    D = pd.DataFrame(array)
    #print(Stability)
    #DataArray = np.append(DataArray, EndEnergy[:,None] ,axis=1)
    D.to_csv('NucDecay.csv')

    plt.plot(array[:,0] , array[:,1])
    plt.title('Average decay energy released for 10 atoms of C14 decay')
    plt.xlabel('Time, y')
    plt.ylabel('Average decay energy release')
    plt.show()


def CreateParticles(ToBeMade):
    """
    Creates particles dictated by the array supplied
    Supplied array needs to be of form [[x_1,name_1],[x_2,name_2]...] where x_i is the number of nuclei of a type to be made and name_i is the isotope to be made
    """
    Particles = np.array([])
    for row in ToBeMade:
        for i in range(0,int(row[0])):
            Particles =np.append(Particles,[RadioNuclei(row[1])])

    return Particles

def SmallestHalfLife(Particles):
    half_lives = np.array([])
    for each in Particles:
        half_lives = np.append(half_lives,each.halfLife)
    minHL = np.amin(half_lives)
    return minHL/10

start_time = time.time()


MCNum = 10
tstep=500
Tend=30000
Energy = np.zeros((int(Tend/tstep +1),2), dtype=float)
stability = np.zeros((int(Tend/tstep +1),2))
ToBeMade = np.array([['10',"14C"]])
Particles = CreateParticles(ToBeMade)
minHalfLife = SmallestHalfLife(Particles)


for i in range(MCNum):
    TempParticles = np.array(Particles)
    DEnergy, LoopStability = MC.MonteCarloLoop(Tend,TempParticles,tstep)

    stability = np.add(stability,LoopStability)
    Energy = np.add(Energy, DEnergy)

stability /= MCNum
Energy /= MCNum

EndEnergy = np.sum(Energy[:,1])

#print(Energy)
print(stability)
dataPlot(stability)

print("--- %s seconds ---" % (time.time() - start_time))
