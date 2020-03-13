import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import MonteCarlo as MC
from ParticleClass import Nuclei, RadioNuclei

start_time = time.time()


MCNum = 100
tstep=1000
Tend=15000
Energy = np.zeros((int(Tend/tstep),2), dtype=float)
stability = np.zeros((int(Tend/tstep),2))


for i in range(MCNum):
    Particles = np.array([])
    for i in range(10):
        Particles =np.append(Particles,[RadioNuclei('14C')])
    
    DEnergy, LoopStability = MC.MonteCarloLoop(Tend,Particles,tstep)

    stability = np.add(stability,LoopStability)
    Energy = np.add(Energy, DEnergy)

stability /= MCNum
Energy /= MCNum

EndEnergy = np.sum(Energy[:,1])

print(EndEnergy)



print("--- %s seconds ---" % (time.time() - start_time))
