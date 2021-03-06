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
m_alpha = (4.001506179127)*amu
m_neutron = constants.neutron_mass

class Nuclei(object):
    """
    Nuclei object to model each nucleus of the mixture to be simulated
    Contains variables and functions that all nuclei will use
    name is a string with the nuclide name e.g. 14C is Carbon 14
    mass is a float with the nuclide mass in kg
    stable is a boolean which is true if the nuclide is stable
    nucleons and protons are integers conatining the number of nucleons and protons in the given nuclide
    """
    def __init__(self, name):
        i = Isotope(name)
        self.name = name
        self.mass = i.mass*amu
        self.stable = i.stable
        self.nucleons = i.A
        self.protons = i.Z
    
    def __eq__(self, other):
        if not isinstance(other, RadioNuclei):
            return False
        
        return (self.name == other.name) and (self.mass == other.mass) and (self.stable == other.stable)
    
    def MassDefect(self,mother):
        """
        Finds the mass difference and the energy released from the nuclear decay
        'if' queries to find which decay type the nucleus has undergone
        Takes the mother and daughter nuclei as inputs
        Outputs the energy including and excluding the emitted particle as a float in Joules
        """
        Dmass = (mother.mass - self.mass)
        EnergyLoss=Dmass * c**2

        if not mother.protons == self.protons:              #True -> new element
            if mother.nucleons == self.nucleons:            #Beta Decay
                Dmass -= m_beta
            else:
                if mother.nucleons == self.nucleons+4:      #Alpha Decay
                    Dmass -= m_alpha    
        else:
            if mother.nucleons ==  self.nucleons+1:         #True:Neutron Emission, False:Gamma Decay
                Dmass -=  m_neutron                         

        HeatEnergy = Dmass * c**2

        return HeatEnergy,EnergyLoss


class RadioNuclei(Nuclei):
    """
    Object to model the radioactive nuclei of the mixture
    Inherits from Nuclei class 
    decayConst is a float with the decay constant of the nuclide, units are defined here with seconds chosen to more more broadly applicable
    halfLife is a float with the half life of the nuclide, units are defined here with seconds chosen to more more broadly applicable
    daughters is a numpy array of the possible decay products with the first column containing names and the second containing braching ratios
    """
    def __init__(self,name):
        i = Isotope(name)
        super(RadioNuclei,self).__init__(name)
        self.decayConst = i.decay_const('s',unc=False)
        self.halfLife = i.half_life('s',unc=False)
        self.daughters = np.array(i.decay_products())
    
    
    def decay(self):
        """
        Changes a radionuclei object into a daughter state 
        Uses decayPath function to determine which daughter to create
        Also uses MassDefect function to find the energy released in the decay
        returns the Nucleus or Radionucleus object depending on decay result and the decay energy including and excluding the emitted particle in joules
        """
        child = self.decayPath()
        decayprod = Nuclei(self.daughters.item((child,0)))
        HeatEnergy,EnergyLoss = decayprod.MassDefect(self)
        if not decayprod.stable:
            decayprod = RadioNuclei(decayprod.name)
        return decayprod , HeatEnergy,EnergyLoss
    
    def decayPath(self):
        """
        Determines the decay branch of a decaying nucleus using a random number generator
        returns an integer as the index of the daughters array that the particle will decay through
        """
        paths=np.array(self.daughters[:,1],dtype=float)
        if paths.size == 1:
            return 0
        else:
            PathsProb = np.sum(paths)
            P = np.random.uniform(0,PathsProb)

            x = 0
            for i, cell in enumerate(paths): 
                x+=cell
                if P<= x:
                    break
            return i
                