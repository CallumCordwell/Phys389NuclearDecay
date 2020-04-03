import numpy as np 
import math
import scipy
import pandas as pd
import matplotlib.pyplot as plt

from ParticleClass import Nuclei, RadioNuclei

def randomNumber(min, max):
    """
    This function gets a random number from a uniform distribution between
    the inputted minimum and maximum inclusive
    """
    range = max - min
    ran = np.random.uniform(0,1)
    return min + ran*range

def crudeMonteCarlo(sampleNum, t ):
    """
    A very basic Monte Carlo simulation
    will run for sampleNum number of times and return and average number of sucesses
    FuncX may be any function assuming that the value returned is a probability between 0 and 1
    """
    
    runningTot = 0.0

    for i in range(sampleNum):
        if Probability(t):
            runningTot += 1

    return runningTot


def Probability(deltaT):
    """
    A comparison to find if a given particle decays in timestep deltaT
    Uses the decay constant of carbon 14
    Returns 1 if the particle decays and 0 if it doesn't
    """
    x = randomNumber(0,1)
    Dconst = 0.00012096809
    P= Dconst * deltaT

    if x<=P:
        return True
    else:
        return False



def ObjectMonteCarlo(sample, t ):
    """
    A variant of the curde Monte Carlo function designed to run using a Nuclei object
    Uses the decay constant of the Nuclei and the random number generator to determine whether it decays
    Returns a boolean true if the nuclei decays
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
    Returns the new nucleus and the decay energy released
    """
    if not Nucleus.stable:
        if ObjectMonteCarlo(Nucleus,t):
            Nucleus , DEnergy, DecayNum = Nucleus.decay()
            return Nucleus , DEnergy, DecayNum
    return Nucleus , 0 , 0

def timestep(t,Particles):
    """
    Runs the functions for each timestep t in the simulation
    takes in an array of particles and a float as the timestep
    returns the updated array of particles and the decay energy released in this timestep
    """
    i=0
    DEnergy = 0
    DecayNum = 0
    newArray=Particles
    for cell in newArray:
        newArray[i], DE ,DN = decayloop(cell,t)
        DEnergy +=DE
        DecayNum +=DN
        i+=1
    
    return newArray, DEnergy,DecayNum


def MonteCarloLoop(Tend,Particles,tstep,SimNum=0):
    """
    Function to run a Monte Carlo simulation over a given period for an array of nuclei
    Takes in end time timit, the timestep, and an array of nuclei to run the checks per timestep
    Assumes at T=0 all the particles are as inputted and Delta E = 0
    SimNum is the number of the simulation being run, this is not used but the multiprocessing pool requires to send an iterable list of numbers
    Returns the array of unstable particle number, cummulative energy released at each timestep, and  cummulative number of decays at each timestep
    """
    Energy = np.zeros((1,2))
    UnstableNum = np.array([[0,Particles.size]])
    Decays = np.zeros((1,2))

    TotalEnergy = 0
    TotalDecays = 0
    T=tstep

    while T<=Tend:
        if T==tstep:
            for each in Particles:
                if each.stable:
                    print(np.where(Particles == each))
                    print(each.name)
        
        instability = 0
        Particles, DEnergy , DecayNum = timestep(tstep,Particles)
        TotalEnergy +=DEnergy
        TotalDecays +=DecayNum
        for cell in Particles:
            if not cell.stable:
                instability+=1

        Energy = np.append(Energy,[[T,TotalEnergy]],axis=0)
        UnstableNum = np.append(UnstableNum,[[T,instability]],axis=0)
        Decays = np.append(Decays, [[T,TotalDecays]],axis=0)
        T+=tstep
    return Energy , UnstableNum, Decays