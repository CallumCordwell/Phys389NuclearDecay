import numpy as np
import math
import MonteCarlo as MC
import threading
import queue

queueLock = threading.Lock()


class myThread(threading.Thread):
    """
    Class of processing threads, inherits functionality from Thread Class in threading module
    Takes in all variables to run functions and defines as self varaibles
    """
    def __init__(self,ID,q,Particles,Tend,tstep):
        threading.Thread.__init__(self)
        self.id = ID
        self.tempenergy = np.array([[]])
        self.tempstability = np.array([[]])
        self.q=q
        self.Particles = Particles
        self.Tend = Tend
        self.tstep = tstep
    
    def run(self):
        """
        Primary use of myThread Class, runs the process which requires multithreadding
        Called from start() function in threading.Thread class runs MonteCarloLoop for each thread
        Fills queue with arrays from MonteCarloLoop
        """
        self.tempenergy, self.tempstability = MC.MonteCarloLoop(self.Tend,self.Particles,self.tstep)
        queueLock.acquire()
        self.q=self.q.put([self.tempenergy,self.tempstability])
        queueLock.release()


def CreateandRunThreads(num,Tend,tstep,Particles):
    """
    Creates an array of threads objects for each Monte Carlo simulation and starts each thread
    Takes in the number of simulations to run, end time for the simulation, and timesteps 
    Outputs averaged data for each timestep summed over all simulations
    """
    q = queue.Queue()
    threads =[]
    energy = np.zeros((int((Tend/tstep) + 1),2), dtype=float)
    stability = np.zeros((int((Tend/tstep) + 1),2))

    for each in range(num):
        thread = myThread(each,q,Particles,Tend,tstep)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        TempEnergy , TempStability = q.get()
        energy = np.add(energy, TempEnergy)
        stability = np.add(stability,TempStability)
    return (energy), (stability)






