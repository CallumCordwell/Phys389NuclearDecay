from multiprocessing import Process, Queue
import numpy as np
from scipy import constants
import math
import pandas as pd
import matplotlib.pyplot as plt
import time
import MonteCarlo as MC
from ParticleClass import Nuclei, RadioNuclei
import threading

start_time = time.time()


Particles = np.array([])
i=0
while i<10:
    Particles =np.append(Particles,[RadioNuclei('14C')])
    i+=1

Tend=5000
tstep=1000
MCNum=100
energy = np.zeros((int((Tend/tstep) + 1),2), dtype=float)
stability = np.zeros((int((Tend/tstep) + 1),2))
"""
if __name__ == '__main__':
    q = Queue()
    for i in range(MCNum):
        p = Process(target=MC.Mutlitimestep, args=(Tend,Particles,t,q))
        p.start()
        TempEnergy , TempStability = q.get()
        energy = np.add(energy, TempEnergy)
        stability = np.add(stability,TempStability)
        p.join()
    print(energy)
    print(stability)
"""          
        
class myThread(threading.Thread):
    def __init__(self, ID,q,Particles):
        threading.Thread.__init__(self)
        self.id = ID
        self.tempenergy = np.array([[]])
        self.tempstability = np.array([[]])
        self.q=q
        self.Particles = Particles
    
    def run(self):
        queueLock.acquire()
        self.tempenergy, self.tempstability = MC.MonteCarloLoop(Tend,self.Particles,tstep)
        
        self.q=self.q.put([self.tempenergy,self.tempstability])
        queueLock.release()
        #process(self.id,self.q)

def process(name,q):
    queueLock.acquire()
    print("proccessing " + name)
    q.put(name)
    queueLock.release()
    time.sleep(1)




threadlist= ["thread1","thread2","thread3"]
queueLock = threading.Lock()
workQueue = Queue()
threads =[]

for each in threadlist:
    thread = myThread(each,workQueue,Particles)
    thread.start()
    threads.append(thread)



for t in threads:
   t.join()
   print(workQueue.get())
print("Exiting Main Thread")


"""
    energy = np.add(energy,thread1.tempenergy)
    stability = np.add(stability,thread2.tempstability)
    energy = np.add(energy,thread2.tempenergy)
    stability = np.add(stability,thread2.tempstability)

"""

print("--- %s seconds ---" % (time.time() - start_time))


