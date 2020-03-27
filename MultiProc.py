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
import Functions as functions

def MyProcess(Tend,Particles,tstep,SimList):
    """
    Function for multiprocessing, this defines the process to be run as func and creates a pool of functions waiting to be run as a processor becomes available
    Will run a process for each iterable in SimList
    Takes in Tend,Particles, and tstep to pass to the MonteCarlo function
    returns a list of outputs from the pool (list of lists of numpy array)
    """
    func = partial(MC.MultiProcLoop, Tend,Particles,tstep)
    with Pool() as pool:
        p = pool.map(func,SimList)
    return p

def startUp():
    """
    Defines the variables for use in the multiprocessing processes
    returns all the variables needed to run the Monte Carlo sims such as time steps and number of sims to be run 
    """
    ToBeMade = np.array([["10","14C"],["10","231PA"],["5","212BI"],["20","81KR"],["20","85KR"]])
    Particles = functions.CreateParticles(ToBeMade)

    MCNum = 10000
    tstep=20
    Tend=150000

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

    functions.dataPlot(stability/MCNum, "StabiltyRan")
    functions.dataPlot(energy/MCNum,"EnergyRan")

