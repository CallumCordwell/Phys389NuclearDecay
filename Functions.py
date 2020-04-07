import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
from ParticleClass import Nuclei, RadioNuclei


def dataPlot(DEnergy,TotalEnergy,Decays,Stability):
    """
    Exports all the measured data to a dataframe and a csv, plots relevant graphs
    Takes in arrays of chosen measured data
    Outputs a single csv file for all the data and a series of chosen graphs (graphs can be added or removed as needed)
    """
    D = pd.DataFrame({'Time':DEnergy[:,0], 'Decay Energy':DEnergy[:,1],'Total Energy':TotalEnergy[:,1],'Decay Num':Decays[:,1],'Unstable Num':Stability[:,1]})
    D.to_csv('Data.csv')

    plt.plot('Time' , 'Decay Num',data=D ,label='Decays')
    plt.plot('Time' , 'Unstable Num',data=D , label='Unstable Particles')
    plt.xlabel('Time, seconds')
    plt.ylabel('Number')
    plt.legend()
    plt.show()

    plt.plot('Time' , 'Decay Energy',data=D , label='Decay Energy Release')
    plt.plot('Time' , 'Total Energy',data=D , label='Total System Energy')
    plt.xlabel('Time, seconds')
    plt.ylabel('Energy, J')
    plt.legend()
    plt.show()

    plt.plot('Time' , 'Decay Energy',data=D )
    plt.xlabel('Time, seconds')
    plt.ylabel('Energy Released, J')
    plt.show()

    plt.plot('Time' , 'Decay Num',data=D )
    plt.xlabel('Time, seconds')
    plt.ylabel('Number of Decays')
    plt.show()

    plt.plot('Time' , 'Unstable Num',data=D )
    plt.xlabel('Time, seconds')
    plt.ylabel('Number of Unstable Particles')
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


def theorysigma(decayconst,array,N0):
    """
    Function to find the standard deviation of a single decaying nuclide
    Takes in the decay constant of this nuclide and a 1D array of time steps so the right number and size of right time steps is used
    Returns arrays of a theoretical average and the theoretical +/- 1 standard deviation (only y values, no time steps)
    """
    y=np.array(array,dtype=float)
    sigma=np.array(array,dtype=float)
    yminus=np.array(array,dtype=float)
    yplus=np.array(array,dtype=float)
    i=0
    for t in array:
        y[i]=N0*math.exp(- decayconst * t)
        sigma[i]=math.sqrt(N0-y[i])
        i+=1

    yplus = np.add(y,sigma)
    yminus =np.subtract(y,sigma)
    return y , yplus, yminus