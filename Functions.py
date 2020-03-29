import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
from ParticleClass import Nuclei, RadioNuclei


def dataPlot(array,datatitle):
    """
    Plots a matplotlib graph for the given array
    Takes in an array to output a pandas dataframe and a matplotlib graph
    """
    D = pd.DataFrame(array)
    D.to_csv(datatitle + '.csv')

    plt.plot(array[:,0] , array[:,1])
    plt.title('Remaining unstable nuclei remaining with a mixture of starting nuclei')
    plt.xlabel('Time, y')
    plt.ylabel('Number of unstable nuclei')
    plt.show()


def CreateParticles(ToBeMade):
    """
    Creates particles dictated by the array supplied
    Supplied array needs to be of form [[x_1,name_1],[x_2,name_2]...] where x_i is the number of nuclei of a type to be made and name_i is the isotope to be made
    """
    Particles = np.array([])
    for row in ToBeMade:
        for i in range(0,int(row[0])):
            Particles =np.append(Particles,[RadioNuclei(row[1])])

    return Particles

def SmallestHalfLife(Particles):
    half_lives = np.array([])
    for each in Particles:
        half_lives = np.append(half_lives,each.halfLife)
    minHL = np.amin(half_lives)
    return minHL


def theorysigma(decayconst,stability):
    y=np.array(stability[:,0])
    sigma=np.array(stability[:,0])
    yminus=np.array(stability[:,0])
    yplus=np.array(stability[:,0])
    i=0
    for t in stability[:,0]:
        y[i]=10*math.exp(- decayconst * t)
        sigma[i]=math.sqrt(10-y[i])

        i+=1

    yplus = np.add(y,sigma)
    yminus =np.subtract(y,sigma)
    
    return y , yplus, yminus