import numpy as np 
import math
import scipy
import pandas as pd
import matplotlib.pyplot as plt

from ParticleClass import Nuclei, RadioNuclei

e=np.e

def randomNumber(min:float, max:float):
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
        x = randomNumber(0,1)
        runningTot += FuncX(x, t)

    return float(runningTot)


def FuncX(x,deltaT):
    """
    A calculation to find the probability of decay of a given particle
    Returns a probability between 0,1
    
    In future will take in a particle class as use the decay constant of that particle as lamda
    """

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
    will run for sampleNum number of times and return and average number of sucesses
    FuncX may be any function assuming that the value returned is a probability between 0 and 1
    """
    
    x = randomNumber(0,1)
    P = sample.decayConst * t
    if x<=P:
        return True
    else:
        return False
