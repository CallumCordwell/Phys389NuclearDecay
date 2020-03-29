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
        runningTot += Probability(t)

    return float(runningTot)


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
        return 1
    else:
        return 0

def Variance(sampleNum):
    """
    Legacy code to find the variance of a function f_of_x
    Unusable in this simulation given the true/false nature of the experiment so a different way to calculate vairance is needed 
    """
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

def decayloop(Nucleus, t):
    """
    Using an unstable nucleus runs the ObjectMonteCarlo function to determine if it decays
    Takes in a nucleus and a timestep to pass to the Monte Carlo function
    Returns the new nucleus and the decay energy released
    """
    if not Nucleus.stable:
        if ObjectMonteCarlo(Nucleus,t):
            Nucleus , DEnergy = Nucleus.decay()
            return Nucleus , DEnergy
    return Nucleus , 0

def timestep(t,Particles):
    """
    Runs the functions for each timestep t in the simulation
    takes in an array of particles and a float as the timestep
    returns the updated array of particles and the decay energy released in this timestep
    """
    i=0
    DEnergy = 0
    newArray=Particles
    for cell in Particles:
        newArray[i], DE = decayloop(cell,t)
        DEnergy +=DE
        i+=1
    instability = 0
    for cell in newArray:
        if not cell.stable:
            instability+=1
    return newArray, DEnergy


def StandardDeviationAnalysis():
    """
    Function to analyse the standard deviation of the random number generator used
    Produces a pandas dataframe and a matplotlib graph of the range of random numbers produced.
    """
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
    Function to run a Monte Carlo simulation over a given period for an array of nuclei#
    Takes in end time timit, the timestep, and an array of nuclei to run the checks per timestep
    Assumes at T=0 all the particles are as inputted and Delta E = 0
    """
    Energy = np.zeros((1,2))
    UnstableNum = np.array([[0,Particles.size]])

    TotalEnergy = 0
    T=tstep

    while T<=Tend:
        instability = 0
        Particles, DEnergy = timestep(tstep,Particles)
        TotalEnergy +=DEnergy
        for cell in Particles:
            if not cell.stable:
                instability+=1

        Energy = np.append(Energy,[[T,TotalEnergy]],axis=0)
        UnstableNum = np.append(UnstableNum,[[T,instability]],axis=0)
        T+=tstep
    return Energy , UnstableNum

def MultiProcLoop(Tend,Particles,tstep,SimList):
    """
    Similar to the MonteCarloLoop function will run a full monte carlo simmulation over a given time period
    Created to be run alongside the multiprocessing function in MultiProc.py
    Takes in Tend,Particles and tstep to run the monte carlo simulation every tstep until Tend on the nuclei in particles array
    SimList is a list of 0 to the number of Monte Carlo sims to be run, not used but the multiprocessing pool requires to send an iterable of numbers
    Returns the array of unstable particle number and cummulative energy released at each timestep 
    """
    
    Energy = np.zeros((1,2))
    UnstableNum = np.array([[0,Particles.size]])
    T=tstep
    TempParticles = np.array(Particles)
    
    TotalEnergy = 0
    while T<=Tend:
        TempParticles, DEnergy = timestep(tstep,TempParticles)
        
        instability = 0
        for cell in TempParticles:
            if not cell.stable:
                instability+=1
        TotalEnergy +=DEnergy
        Energy = np.append(Energy,[[T,TotalEnergy]],axis=0)
        UnstableNum = np.append(UnstableNum,[[T,instability]],axis=0)
        T+=tstep
    return UnstableNum, Energy
