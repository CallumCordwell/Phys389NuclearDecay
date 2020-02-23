import numpy as np 
import math
import scipy
from ParticleClass import decayConst

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
    
    sampleSum = 0.0

    for i in range(sampleNum):
        x = randomNumber(0,1)
        if x<= FuncX():
            sampleSum += 1
    
    return float(sampleSum/sampleNum)


def FuncX():
    """
    A calculation to find the probability of decay of a given particle
    Returns a probability between 0,1
    
    In future will take in a particle class as use the decay constant of that particle as lamda
    """
    deltaT = 3000.0

    lamda = decayConst('14C')

    P= lamda * deltaT

    return P

print(crudeMonteCarlo(10000))