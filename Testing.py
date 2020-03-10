import pytest
import MonteCarlo as MC
import ParticleClass as PC
#import Runner

def test_random():
    i=5
    j=-2
    assert MC.randomNumber(j,i) <=i
    assert MC.randomNumber(j,i) >=j

def test_crudeMC():
    loopnum = 100
    time = 1000.6
    assert MC.crudeMonteCarlo(loopnum,time) >0
    assert MC.crudeMonteCarlo(loopnum,time) <loopnum

def test_probability():
    P= 1

    assert MC.Probability(1,100000) ==1
    assert MC.Probability(0.2,1000)==0

def test_DecayEnergy():
    mother = PC.Nuclei('238U')
    daughter = PC.RadioNuclei('235U')
    assert mother.MassDefect(daughter) < 4.4879*10**(-10)

def test_decay():
    mother = PC.RadioNuclei('238U')
    daughter = PC.RadioNuclei('234THg')
    assert mother.decay(0) == daughter

mother = PC.RadioNuclei('238U')
daughter = PC.RadioNuclei('234THg')
print(mother)
print(daughter)
print(mother.decay(0))

test_decay()
