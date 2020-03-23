import numpy as np 
import math
import scipy
import pandas as pd
import matplotlib.pyplot as plt
import threading

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
        runningTot += Probability(t)

    return float(runningTot)


def Probability(deltaT):
    """
    A calculation to find the probability of decay of a given particle
    Uses the decay constant of carbon 14
    Returns a probability between 0,1
    """
    x = randomNumber(0,1)
    Dconst = 0.00012096809
    P= Dconst * deltaT

    if x<=P:
        return 1
    else:
        return 0

def Variance(sampleNum):
    runningSum = 0.0

    for i in range(sampleNum):
        x = randomNumber(0,1)
        runningSum+= f_of_x(x)**2
    sumofsqs = runningSum*1/sampleNum
    
    runningSum=0.0
    for i in range(sampleNum):
        x = randomNumber(0,1)
        runningSum+= f_of_x(x)
    sqavg = (runningSum*1/sampleNum)**2

    return  sumofsqs-sqavg


def ObjectMonteCarlo(sample, t ):
    """
    A variant of the Monte Carlo simulation designed to run using a Nuclei object
    Uses the decay constant of the Nuclei and the random number generator to determine whether it decays
    """
    
    x = randomNumber(0,1)
    P = sample.decayConst * t
    if x<=P:
        return True
    else:
        return False

def decayloop(Nucleus, t, path=0):
    if not Nucleus.stable:
        if ObjectMonteCarlo(Nucleus,t):
            Nucleus , DEnergy = Nucleus.decay(path)
            return Nucleus , DEnergy
    return Nucleus , 0

def timestep(t,Particles):
    i=0
    DEnergy = 0
    instability = 0
    for cell in Particles:
        Particles[i], DE = decayloop(cell,t)
        DEnergy +=DE
        
        
        if not Particles[i].stable:
            instability+=1
        
        i+=1
    return Particles, DEnergy, instability


def StandardDeviationAnalysis():
    array = np.array([])
    i=0
    j=0
    x=0
    while j<1000:
        while  i<100:
            x+= Probability(3000)
            
            i+=1
        array = np.append(array,x/1000)
        x=0
        j+=1
        i=0

    D = pd.DataFrame(array)
    D.to_csv('randomnumberanalysis.csv')

    plt.plot(array)
    plt.title('Probability estimation for 100 attempts')
    plt.xlabel('Event number')
    plt.ylabel('Average number of passes')
    plt.show()


def MonteCarloLoop(Tend,Particles,tstep):
"""
Function to run a Monte Carlo simulation over a given period for an array of nuclei
Takes in end time top timit, the timestep, and an array of nuclei to run the checks per timestep
Assumes at T=0 all the particles are as inputted and \Delta E = 0
"""
    Energy = np.zeros((1,2))
    UnstableNum = np.array([[0,Particles.size]])
    T=tstep
    TotalEnergy = 0
    while T<=Tend:
        Particles, DEnergy, instability = timestep(tstep,Particles)
        TotalEnergy +=DEnergy
        Energy = np.append(Energy,[[T,TotalEnergy]],axis=0)
        UnstableNum = np.append(UnstableNum,[[T,instability]],axis=0)
        T+=tstep
    return Energy , UnstableNum


