from multiprocessing import Pool
from scipy import constants
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import MonteCarlo as MC
from ParticleClass import Nuclei, RadioNuclei
from functools import partial

def MyProcess(Tend,Particles,tstep,SimList):
    func = partial(MC.MultiProcLoop, Tend,Particles,tstep)
    with Pool() as pool:
        p = pool.map(func,SimList)
    return p

def MultiProcRunning(Tend,Particles,tstep,MCNum):
    pass

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

def startUp():
    Particles = np.array([])
    i=0
    while i<10:
        Particles =np.append(Particles,[RadioNuclei('14C')])
        i+=1

    MCNum = 50
    tstep=100
    Tend=6000

    return MCNum,tstep,Tend,Particles




if __name__ ==  "__main__":
    start_time = time.time()

    MCNum,tstep,Tend,Particles = startUp()
    energy = np.zeros((int((Tend/tstep) + 1),2), dtype=float)
    stability = np.zeros((int((Tend/tstep) + 1),2))
    print("Starting Threading")
    SimList = [x for x in range(0,MCNum)]
    
    pool = np.array(MyProcess(Tend,Particles,tstep,SimList))
    
    stablepool = pool[:,0]
    energypool = pool[:,1]
    for each in stablepool:
        stability = np.add(stability,each)
    for each in energypool:
        energy = np.add(energy,each)

    print(stability/MCNum)
    print(energy/MCNum)
    
    print("Exiting Main Thread. Time: %s seconds" % (time.time() - start_time))

    DataPlot(stability/MCNum)

