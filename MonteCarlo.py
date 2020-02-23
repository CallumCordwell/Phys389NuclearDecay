import numpy as np 
import math
import scipy
#sfrom ParticleClass import Nuclei, RadioNuclei

def randomNumber(min:float, max:float):
    """
    This function gets a random number from a uniform distribution between
    the inputted minimum and maximum inclusive
    """
    range = max - min
    ran = np.random.uniform(0,1)
    return min + ran*range

def crudeMonteCarlo(sampleNum):
    """
    A very basic Monte Carlo simulation
    will run for sampleNum number of times and return and average number of sucesses
    FuncX may be any function assuming that the value returned is a probability between 0 and 1
    """
    
    runningTot = 0.0

    for i in range(sampleNum):
        x = randomNumber(0,1)
        if x <= FuncX():
            runningTot += 1
    
    return float(runningTot/sampleNum)


def FuncX():
    """
    A calculation to find the probability of decay of a given particle
    Returns a probability between 0,1
    
    In future will take in a particle class as use the decay constant of that particle as lamda
    """
    deltaT = 3000.0

    Dconst = 0.00012096809
    P= Dconst * deltaT

    return P

def crudeVariance(sampleNum):
    sampleSum = 0.0

    for i in range(sampleNum):
        x = randomNumber(0,1)
        if x <= FuncX():
            sampleSum += 1
    
    return  float(sampleSum**2/sampleNum) - float(sampleSum/sampleNum)**2

print(crudeMonteCarlo(10000))
print(crudeVariance(10000))
"""
Importance sampling method

f(x) as an exponential decay
g(x) as Aexp(-lambda x)
1= 0-inf integrate g(x) dx ... A=lambda

"""


