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


## 2019/09/05

### Checking finished runs
t1 and t2 runs finished. There are 3 molecules unfinished in t3:
["4lodophenol_octanol_0.0_1.0_SMIRNOFF_tip3p_equil", "SM15_octanol_0.0_1.0_SMIRNOFF_tip3p_equil", "Amylobarbitone_octanol_0.0_1.0_SMIRNOFF_tip3p_equil"]

I resubmitted these, however resuming did not make a difference.
To rerun from the beginning I have to remove the names of these three systems to rerun from `/dry_yank_results/dry_yank_mols_done.json` and keep the names of systems that I do not want to rerun.
However I realized these simulations were already missing from the `dry_yank_mols_done.json` file as they did not finish by throwing NaNs. What happened seems to be problematic checkpoint files.
I will instead delete the yank output directories for these and attempt rerun from beginning.

$ cd dry_runs/t3/dry_yank_output
$ rm -rf Amylobarbitone_octanol_0.0_1.0_SMIRNOFF_tip3p_equil
$ rm -rf SM15_octanol_0.0_1.0_SMIRNOFF_tip3p_equil
$ rm -rf 4lodophenol_octanol_0.0_1.0_SMIRNOFF_tip3p_equil


### Analyzing YANK results

1) 4 hour interactive job request:
$ bsub -n 1 -W 4:00 -Is /bin/bash

2) Run:
$ cd /dry_runs/analysis/
$ conda activate SAMPL6_logP
$ python test_SAMPL6_molecules.py
$ python test_extra_molecules.py

All runs are completed properly.



## 2019/11/07

### CORRECTION OF LAMBDA STERICS PROTOCOL

We realized the previous lambda schedule used for water phase was wrong. 
The protocol used to decouple the Lennard-Jones interactions for the water phase was not appropriate. 
Our protocol did not scale steric interactions ( $\lambda$ = [1.00, 1.00, 1.00, 1.00, 1.00]). 
This choice would have been appropriate for a vacuum phase, but not for water phase.  
In the DFE protocol as implemented the thermodynamic cycle do not close because the calculations do not account for turning on Lennard-Jones interactions of the molecule in water phase. 
The correct alchemical protocol would be the same protocol used for the octanol phase.

#### Tasks for this correction:

(1) Update protocol of solvent 2 in yank.yaml.

protocols:
    hydration-protocol:
        solvent1:
            alchemical_path:
                lambda_electrostatics: [1.00, 0.75, 0.50, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
                lambda_sterics: [1.00, 1.00, 1.00, 1.00, 1.00, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05, 0.00]
        solvent2:
            alchemical_path:
                lambda_electrostatics: [1.00, 0.75, 0.50, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
                lambda_sterics: [1.00, 1.00, 1.00, 1.00, 1.00, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05, 0.00]

(2) Delete solvent2.nc file from yank_outputs directory
(3) Delete dry_yank_results/yank_mols_done.json

This will run all the systems again. Since octanol phase is completed, it should skip that phase.


