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
    Will run a process for each iterable in SimList using as many threads as available on the computer, if a specific number of threads is desired add a number to the line with Pool() as pool: to become with Pool(N) as pool():
    Takes in time period, time step, and an array of nuclei to pass to the MonteCarlo function
    returns a list of outputs from the pool (list of numpy arrays)
    """
    
    func = partial(MC.MonteCarloLoop, Tend,Particles,tstep)
    with Pool() as pool:
        p = pool.map(func,SimList,chunksize=1)
    return p

def startUp():
    """
    Defines the variables for use in the multiprocessing processes
    returns all the variables needed to run the Monte Carlo sims: the time steps, number of sims to be run, time period, and the array of nuclei
    """
    ToBeMade = np.array([["60","197BIm"],["10","231PA"],['10','81KR'],["10","85KR"],['10','171ER'],['10','241AM']])
    Particles = functions.CreateParticles(ToBeMade)

    MCNum = 500
    tstep=1
    Tend=1800
    
    string=''
    for i in range(ToBeMade.shape[0]):
        string=string + ToBeMade[i,0] +' ' +ToBeMade[i,1]+ ', '
    print('Simulation initilised using: ' + string)

    return MCNum,tstep,Tend,Particles

"""
Core programme:
Majority used to define variables to measure the result then call the multiprocessing pool
A timer is added to measure the time taken to run the simulations
Data is outputted using the Functions.dataPlot() function
"""

if __name__ ==  "__main__":
    start_time = time.time()

    MCNum,tstep,Tend,Particles = startUp()
    decayEnergy = np.zeros((int((Tend/tstep) + 1),2))
    stability = np.zeros((int((Tend/tstep) + 1),2))
    decays = np.zeros((int((Tend/tstep) + 1),2))
    systemEnergy = np.zeros((int((Tend/tstep) + 1),2))

    print("Starting Threading")
    SimList = [x for x in range(0,MCNum)]
    pool= np.array(MyProcess(Tend,Particles,tstep,SimList))
    
    print("Exiting Main Thread. Time: %s seconds" % (time.time() - start_time))

    pool /= MCNum

    energypool = pool[:,0]
    stablepool = pool[:,1]
    decayspool = pool[:,2]
    systemenergypool = pool[:,3]
    
    for each in energypool:
        decayEnergy = np.add(decayEnergy,each)
    for each in stablepool:
        stability = np.add(stability,each)
    for each in decayspool:
        decays = np.add(decays, each)
    for each in systemenergypool:
        systemEnergy = np.add(systemEnergy,each)


    functions.dataPlot(decayEnergy,systemEnergy,decays,stability)
    


