from npat import Isotope
import numpy as np
from scipy import constants
"""
cheat sheet for npat Isotope interactions
i= Isotope('14C')
print(i.TeX)
print(i.mass , 'u')
print(i.half_life(i.optimum_units(),unc=False), i.optimum_units())
print(i.decay_const(i.optimum_units(),unc=False) , '1/' + i.optimum_units())
print(i.decay_products())
"""

c = constants.speed_of_light
amu = constants.atomic_mass

class Nuclei(object):
    def __init__(self, name):
        i = Isotope(name)
        self.name = name
        self.mass = i.mass
        self.stable = i.stable
    
    def MassDefect(self,child):
        """
        Finds the mass difference and the energy released from the nuclear decay
        Takes the mother and daughter nuclei as inputs
        Outputs the energy as a float
        """
        Dmass = (self.mass - child.mass)*amu
        energy = Dmass * c**2

        return energy

class RadioNuclei(Nuclei):
    def __init__(self,name):
        i = Isotope(name)
        super(RadioNuclei,self).__init__(name)
        self.decayConst = i.decay_const(i.optimum_units(),unc=False), i.optimum_units()
        self.daughters = np.array(i.decay_products())
    
    
    def decay(self,child):
        """
        Decays a radionuclei into the defined daughter state
        child is an integer that refers to an index in the daughter array
        Also uses MassDefect function to return the energy released in the decay
        """
        decayprod = Nuclei(self.daughters.item((child,0)))
        Erelease = self.MassDefect(decayprod)
        self = decayprod
        if not self.stable:
            self = RadioNuclei(self.name)
        return self,Erelease


C = RadioNuclei('212BI')

print(C.name)
print(C.daughters)

while not C.stable:
    C , DEnergy = C.decay(0)
    print(C.name)
    print(C.stable)
    print(DEnergy)