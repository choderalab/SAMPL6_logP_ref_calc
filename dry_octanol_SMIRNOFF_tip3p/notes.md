# SAMPL6 LOGP REFERENCE CALCULATIONS WITH DRY OCTANOL PHASE (SMIRNOFF, TIP3P)

## 2019/08/15

### Conda environment

Proper conda environment: SAMPL6_logP  
$ source activate SAMPL6_logP  


### Equilibrated input files

3 replicates of equilibrated systems were prepared by Danielle Bergazin.  
PDB coordinate files and XML system files can be found in `equilibrated_input_files/` directory.


### Submit array jobs to run 3 replicates of octanol(dry)-water logP calculations with YANK

Directory:
- ./dry_runs/t1
- ./dry_runs/t2
- ./dry_runs/t3

Each phase will be simulated for 5 ns. The protocol is adopted from hydration free energy calculations on FreeSolv database for SMIRNOFF paper:
https://github.com/MobleyLab/SMIRNOFF_paper_code/tree/master/FreeSolv/scripts

default_time step: 3*femtoseconds
temperature: 298.15*kelvin
pressure: 1.0*atmosphere
checkpoint_interval: 50
default_nsteps_per_iteration: 335 #286
default_number_of_iterations: 5000
anisotropic_dispersion_cutoff: 12.0*angstroms
hydrogen_mass: 1.0*amu





