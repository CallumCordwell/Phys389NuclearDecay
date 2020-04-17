# Phys389NuclearDecay
Lancaster University Phys389 project to simulate Nuclear Decays, available on GitHub at https://github.com/CallumCordwell/Phys389NuclearDecay:
  	Core.py is the main file that launches the simulation using multiprocessing.
  	MonteCarlo.py is the file that runs the majority of the satistical Monte Carlo simulation functions.
  	ParticleClass.py contains the object classes for nuclei and radionuclei.
  	Functions.py contains a series of data handling and excess functions to keep the Core file clear.
  	test_testing.py is the testing file for all the other files containing pytest functions.

To run the simulation the following python modules will be needed:
	multiprocessing
	scipy
	numpy
	math
	pandas
	matplotlib
	time
	functools
	NPAT (may need to be downloaded from GitHub: https://github.com/jtmorrell/npat)

To run a simulation simply run the Core.py file using any python shell.

To edit the simulation:
	- Open the Core.py file in an editor
	- Find the function called 'startUp'
	- The variables created here define the simulation, edit these as fit for the simulation or test desired:
		- 'ToBeMade' 2D array defines the nuclei to be simulated, where the first column is the number of nuclei of a nuclide e.g. "10" and the second column is the nuclide name such as "197BIg" for ground state of bismuth 197. N.B. only ground and first metastable states (defined by using 'm' instead of 'g' after the element name) are able to be analysed due to limitation of the NPAT tool
		- 'MCNum' defines the number of iterations to repeat the simulation over, this should be 500 or over for reasonable accuracy
    	- 'tstep' defines the size of the time step in the simulation, should be 0.1 of the half life of the nuclides used or less for reasonable accuracy
    	- 'Tend' defines the simulation period
	- Save the file and run as above.
