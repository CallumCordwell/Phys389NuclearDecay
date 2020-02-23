from npat import Isotope
import numpy as np
"""
cheat sheet for npat Isotope interactions
i= Isotope('14C')
print(i.TeX)
print(i.mass , 'u')
print(i.half_life(i.optimum_units(),unc=False), i.optimum_units())
print(i.decay_const(i.optimum_units(),unc=False) , '1/' + i.optimum_units())
print(i.decay_products())
"""

class Nuclei(object):
    def __init__(self, name):
        i = Isotope(name)
        self.name = name
        self.mass = i.mass
        self.stable = i.stable


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
        """
        self = Nuclei(self.daughters.item((child,0)))

        if not self.stable:
            self = RadioNuclei(self.name)
        return self


C = RadioNuclei('212BI')

print(C.name)
print(C.daughters)

while not C.stable:
    C= C.decay(0)
    print(C.name)
    print(C.stable)