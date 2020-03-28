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
m_beta = constants.electron_mass *amu
m_alpha = Isotope("4HE").mass*amu
m_neutron = constants.neutron_mass

class Nuclei(object):
    """
    Nuclei object to model each nucleus of the mixture to be modelled
    Contains variable and functions that all nuclei will use
    name is a string with the isotope nape e.g. 14C is Carbon 14
    mass is a float with the isotope mass in amu
    stable is a boolean which is true if the nucleus is stable
    """
    def __init__(self, name):
        i = Isotope(name)
        self.name = name
        self.mass = i.mass
        self.stable = i.stable
        self.nucleons = i.A
    
    def __eq__(self, other):
        if not isinstance(other, RadioNuclei):
            return False
        
        return (self.name == other.name) and (self.mass == other.mass) and (self.stable == other.stable)
    
    def MassDefect(self,mother):
        """
        Finds the mass difference and the energy released from the nuclear decay
        Takes the mother and daughter nuclei as inputs
        Outputs the energy as a float in Joules
        """
        Dmass = (mother.mass - self.mass)*amu
        
        if mother.nucleons == self.nucleons:
            Dmass -= m_beta
        else:
            if mother.nucleons == self.nucleons+4:
                Dmass -= m_alpha
            else:
                Dmass -= m_neutron        

        energy = Dmass * c**2

        return energy


class RadioNuclei(Nuclei):
    """
    Object to model the radioactive nuclei of the mixture
    Inherits from Nuclei class 
    decayConst is a float with the decay constant of the isotope
    daughters is a numpy array of the possible decay products with the first column containing names and the second containing braching ratios
    """
    def __init__(self,name):
        i = Isotope(name)
        super(RadioNuclei,self).__init__(name)
        self.decayConst = i.decay_const("y",unc=False)
        self.halfLife = i.half_life(i.optimum_units(),unc=False)
        self.daughters = np.array(i.decay_products())
    
    
    def decay(self):
        """
        Changes a radionuclei into a daughter state 
        Uses decayPath function to determine which daughter to create
        Also uses MassDefect function to find the energy released in the decay
        returns the Nucleus or Radionucleus object depending on decay result and the decay energy released in joules
        """
        child = self.decayPath()
        decayprod = Nuclei(self.daughters.item((child,0)))
        Erelease = decayprod.MassDefect(self)
        if not decayprod.stable:
            decayprod = RadioNuclei(decayprod.name)
        return decayprod , Erelease
    
    def decayPath(self):
        """
        Determines the decay branch of a decaying nucleus using a random number generator
        returns an integer as the index in the daughters array that the particle will decay through
        """
        paths=np.array(self.daughters[:,1],dtype=float)
        if paths.size == 1:
            i=0
            return i
        else:
            PathsProb = np.sum(paths)
            P = np.random.uniform(0,PathsProb)

            x = 0
            for i, cell in enumerate(paths): 
                x+=cell
                if P<= x:
                    break
            return i
                