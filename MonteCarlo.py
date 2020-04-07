import numpy as np 
import math
import scipy
import pandas as pd
import matplotlib.pyplot as plt

from ParticleClass import Nuclei, RadioNuclei


c = scipy.constants.speed_of_light

def randomNumber(min, max):
    """
    This function gets a random number from a uniform distribution between
    the inputted minimum and maximum inclusive
    """
    range = max - min
    ran = np.random.uniform(0,1)
    return min + ran*range

def ObjectMonteCarlo(sample, t ):
    """
    A developped function designed to be repeatedly looped for a Monte Carlo method
    Recieves a RadioNuclei object and a time to be analysed over
    Uses the decay constant of the Nuclei object and the random number generator to determine whether it decays
    Returns a boolean, true if the nuclei object decays
    """
    
    x = randomNumber(0,1)
    P = sample.decayConst * t
    if x<=P:
        return True
    else:
        return False

def decayloop(Nucleus, t):
    """
    Using an unstable nucleus runs the ObjectMonteCarlo function to determine if it decays
    Takes in a nucleus and a timestep to pass to the Monte Carlo function
    Returns the new nucleus and the decay energy released or the original nucleus and 0s if no decay occured
    """
    if not Nucleus.stable:
        if ObjectMonteCarlo(Nucleus,t):
            Nucleus , HeatEnergy, EnergyLoss = Nucleus.decay()
            return Nucleus , HeatEnergy, 1,EnergyLoss
    return Nucleus , 0 , 0,0

def timestep(t,Particles):
    """
    Runs the functions for each timestep t in the simulation
    takes in an array of particles and a float as the timestep
    returns the updated array of particles and the decay energy released in this timestep
    """
    i=0
    DHeatEnergy = 0
    DecayNum = 0
    DTotalEnergy = 0
    newArray=Particles
    for cell in newArray:
        newArray[i], DHE ,DN,E = decayloop(cell,t)
        DHeatEnergy +=DHE
        DecayNum +=DN
        DTotalEnergy+=E
        i+=1
    
    return newArray, DHeatEnergy,DecayNum,DTotalEnergy


def MonteCarloLoop(Tend,Particles,tstep,SimNum=0):
    """
    Function to run a Monte Carlo simulation over a given period for an array of nuclei
    Takes in the end time timit, the timestep, and an array of nuclei to run the checks per timestep
    Assumes at T=0 all the particles are as inputted and Delta E = 0
    SimNum is the number of the simulation being run, this is not used but the multiprocessing pool requires to send an iterable list of numbers
    Returns an array of unstable particle numbers, cummulative energy released, total system energy, and cummulative number of decays at each timestep
    """
    InitialEnergy = 0
    for each in Particles:
        InitialEnergy += each.mass * c**2
    UnstableNum = np.array([[0,Particles.size]])
    Decays = np.zeros((1,2))
    DecayEnergy =  np.zeros((1,2))
    SystemEnergy =  np.array([[0,InitialEnergy]])
    TotalHeatEnergy = 0
    TotalDecays = 0
    TotalLostEnergy = 0
    T=tstep

    while T<=Tend:        
        MassEnergy = 0
        instability = 0
        Particles, HeatEnergy , DecayNum,LostE = timestep(tstep,Particles)
        TotalLostEnergy += LostE
        TotalHeatEnergy +=HeatEnergy
        for each in Particles:
            MassEnergy += each.mass * c**2

        TotalDecays +=DecayNum
        for cell in Particles:
            if not cell.stable:
                instability+=1

        DecayEnergy = np.append(DecayEnergy,[[T,TotalHeatEnergy]],axis=0)
        UnstableNum = np.append(UnstableNum,[[T,instability]],axis=0)
        Decays = np.append(Decays, [[T,TotalDecays]],axis=0)
        SystemEnergy = np.append(SystemEnergy,[[T,TotalLostEnergy+MassEnergy]],axis=0)
        T+=tstep
    return DecayEnergy , UnstableNum, Decays, SystemEnergy