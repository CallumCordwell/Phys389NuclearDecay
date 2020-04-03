import pytest
import MonteCarlo as MC
import ParticleClass as PC
#import Runner

def test_random():
    i=5
    j=-2
    assert MC.randomNumber(j,i) <=i
    assert MC.randomNumber(j,i) >=j

def test_MonteCarlo():
    loopnum = 100
    time = 1000.6
    assert MC.crudeMonteCarlo(loopnum,time) >0
    assert MC.crudeMonteCarlo(loopnum,time) <loopnum
    
    P= PC.RadioNuclei('14C')
    assert MC.ObjectMonteCarlo(P,0) == False
    assert MC.ObjectMonteCarlo(P,100000) == True

def test_probability():
    P= PC.RadioNuclei('14C')

    assert MC.Probability(100000) == True
    assert MC.Probability(1000)==False

def test_DecayEnergy():
    mother = PC.RadioNuclei('238U')
    daughter = PC.Nuclei('234TH')
    assert daughter.MassDefect(mother) < 8.47819*10**(-13)
    assert daughter.MassDefect(mother) > 8.47817*10**(-13)
    mother = PC.RadioNuclei('14C')
    daughter = PC.Nuclei('14N')
    assert daughter.MassDefect(mother) < 2.50703e-14
    assert daughter.MassDefect(mother) > 2.50701e-14



def test_decay():
    mother = PC.RadioNuclei('238U')
    daughter = PC.RadioNuclei('234THg') 
    test, E = mother.decay()
    assert test == daughter

def test_path():
    mother = PC.RadioNuclei('176PT')
    assert mother.decayPath() >= 0 

