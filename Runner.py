import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import MonteCarlo as MC
from ParticleClass import Nuclei, RadioNuclei
import functions
"""
Runs the monte carlo sim without multiprocessing using MonteCarloLoop
"""


start_time = time.time()


MCNum = 100
tstep=1000
Tend=60000
Energy = np.zeros((int(Tend/tstep +1),2), dtype=float)
stability = np.zeros((int(Tend/tstep +1),2))
ToBeMade = np.array([["10","231PA"],["10","14C"],["5","212BI"],["20","235U"]])
Particles = functions.CreateParticles(ToBeMade)

for i in range(MCNum):
    TempParticles = np.array(Particles)
    DEnergy, LoopStability= MC.MonteCarloLoop(Tend,TempParticles,tstep)

    stability = np.add(stability,LoopStability)
    Energy = np.add(Energy, DEnergy)
print("--- %s seconds ---" % (time.time() - start_time))    

stability /= MCNum
Energy /= MCNum

EndEnergy = np.sum(Energy[:,1])

#print(Energy)

functions.dataPlot(Energy,"energy")
functions.dataPlot(stability,"stability")

