import pytest
import MonteCarlo as MC
import ParticleClass as PC
import Functions as F
import numpy as np
import math
"""
Tests for functions in the MonteCarlo file, all relating to the statistical methods
"""

def test_random():
    i=5
    j=-2
    assert MC.randomNumber(j,i) <=i
    assert MC.randomNumber(j,i) >=j

def test_MonteCarlo():
    P= PC.RadioNuclei('171ER')
    assert MC.ObjectMonteCarlo(P,0) == False
    assert MC.ObjectMonteCarlo(P,100000) == True

"""
Tests for functions in the ParticleClass file, all relating to the nuclei and radionuclei objects
"""

def test_DecayEnergy():
    mother = PC.RadioNuclei('238U')
    daughter = PC.Nuclei('234TH')
    assert daughter.MassDefect(mother)[0] < 8.47819*10**(-13)
    assert daughter.MassDefect(mother)[0] > 8.47817*10**(-13)
    assert daughter.MassDefect(mother)[1] < 5.98040*10**(-10)
    assert daughter.MassDefect(mother)[1] > 5.98038*10**(-10)
    mother = PC.RadioNuclei('14C')
    daughter = PC.Nuclei('14N')
    assert daughter.MassDefect(mother)[0] < 2.50703e-14
    assert daughter.MassDefect(mother)[0] > 2.50701e-14
    assert daughter.MassDefect(mother)[1] < 2.50703e-14
    assert daughter.MassDefect(mother)[1] > 2.50701e-14

def test_decay():
    mother = PC.RadioNuclei('238U')
    daughter = PC.RadioNuclei('234THg') 
    test, E, E2= mother.decay()
    assert test == daughter

def test_path():
    mother = PC.RadioNuclei('176PT')
    assert mother.decayPath() >= 0 

"""
Tests for functions in the Functions file, core functions for the running of the programme
"""
def test_CreateParticles():
    ToBeMade = np.array([["60","197BIm"],["10","231PA"],['10','81KR'],["10","85KR"],['10','171ER'],['10','241AM']])
    Particles = F.CreateParticles(ToBeMade)
    length=0
    for each in ToBeMade[:,0]:
        length+=int(each)
    assert Particles.size == length


def test_theorysigma():
    assert F.theorysigma(math.log(2)/10,[10],10)[0] == 5
    assert F.theorysigma(math.log(2)/10,[10],10)[1] == 5+math.sqrt(5)
    assert F.theorysigma(math.log(2)/10,[10],10)[2] == 5-math.sqrt(5)