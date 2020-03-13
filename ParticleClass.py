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
    
    def __eq__(self, other):
        if not isinstance(other, RadioNuclei):
            return False
        
        return (self.name == other.name) and (self.mass == other.mass) and (self.stable == other.stable)
    
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
        self.decayConst = i.decay_const(i.optimum_units(),unc=False)
        self.daughters = np.array(i.decay_products())
    
    
    def decay(self,child):
        """
        Decays a radionuclei into the defined daughter state
        child is an integer that refers to an index in the daughter array
        Also uses MassDefect function to return the energy released in the decay
        """
        i = self.decayPath()
        decayprod = Nuclei(self.daughters.item((child,i)))
        Erelease = self.MassDefect(decayprod)
        New = decayprod
        if not New.stable:
            New = RadioNuclei(New.name)
        return New , Erelease
    
    def decayPath(self):
        paths=np.array(self.daughters[:,1],dtype=float)
        PathsProb = np.sum(paths)

        P = np.random.uniform(0,PathsProb)

        x = 0
        for i, cell in enumerate(paths): 
            x+=cell
            if P<= x:
                break
        return i
            

