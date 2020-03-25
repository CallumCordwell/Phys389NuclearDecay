Runner is the main file that launches the simulation
MonteCarlo is the file that runs the majority of the satistical Monte Carlo simmulation functions
ParticleClass contains the onject classes for nuclei and radionuclei
MultiProc contains the functions for running the simulation using multi-threading. 
  NB: when using MultiProc an edit is needed in the npat module to ensure that multiple threads can run at once. The dbmgr.py file here must replace the file of the same name used in the npat folder.
test_testing is the testing file for all the other files
