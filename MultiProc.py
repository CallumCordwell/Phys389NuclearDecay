from multiprocessing import Process, Queue
import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import MonteCarlo as MC
from ParticleClass import Nuclei, RadioNuclei

start_time = time.time()


Particles = np.array([])
i=0
while i<10:
    Particles =np.append(Particles,[RadioNuclei('14C')])
    i+=1


t=1000
def worker(num,x,q):
    """thread worker function"""
    q.put( ['Worker:', num , x])

if __name__ == '__main__':
    q = Queue()
    for i in range(5):
        p = Process(target=MC.Mutlitimestep, args=(t,Particles,q,))
        p.start()
        print( q.get())
        p.join()
