import numpy as np 
import math
import scipy
import pandas as pd
import matplotlib.pyplot as plt
#from ParticleClass import Nuclei, RadioNuclei
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


t = 1000
T=t
N=10000
Array = np.array([[N,0]])
plt.plot(Array,Array)
while N > 1:
    N -= int(crudeMonteCarlo(N,t))
    Array = np.append(Array,[[N,T]], axis=0)
    T+=t


D = pd.DataFrame(Array, columns=('Time,y', 'Number of C14 nuclei'))
print(D)
D.to_csv('NucDecay.csv')
plt.plot(Array[:,0],Array[:,1])
plt.title('Decay of Carbon 14 nuclei using Monte Carlo method')
plt.xlabel('Time, years')
plt.ylabel('Number of C14 nuclei')
plt.show()

fig = plt.plot(Array[:,1],Array[:,0])
plt.show(fig)

