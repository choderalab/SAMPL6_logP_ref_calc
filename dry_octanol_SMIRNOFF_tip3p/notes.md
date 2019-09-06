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
