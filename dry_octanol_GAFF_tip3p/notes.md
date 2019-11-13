# SAMPL6 LOGP REFERENCE CALCULATIONS WITH DRY OCTANOL PHASE

## 2019/05/23

### Creating conda environment.

To replicate the conda environments Danielle used in wet octanol logP calculations, I copied `requirements.txt` file from https://github.com/bergazin/SAMPL6pt2_ref_calc/blob/master/requirements.txt.  
$ conda create --name SAMPL6_logP --file requirements.txt  

This didn't work. So I will manually create a similar environment that will use yank=0.24.0=py36_0  
$ conda create -n SAMPL6_logP python=3.6  
$ conda activate SAMPL6_logP  

I tried installing yank=0.24 from conda but that wasn't available:  
$ conda install -c omnia yank=0.24.0=py36_0  

Instead I tried the way Danielle installed everything:  
$ conda install -c omnia openmm openforcefield parmed yank openmoltools  
$ conda update yank  


## 2019/06/24

### Correcting conda activate error

`conda activate SAMPL6_logP` command was giving an conda initialization error.  
Instead using `source activate SAMPL6_logP` fixed the problem.  


### Correctiong error about Scipy.misc.logsumexp()

I had scipy=1.3.0 installed when I got an error about importing logsumexp() function.  
I saw that Danielle was using scipy=1.2.1, so I tried changing my scipy version, which worked.  
$ conda install scipy=1.2.1  


## 2019/05/23

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

## 2019/05/31

Most of the jobs completed. Run ` check_incomplete_runs.py` to see which systems were not completed.  

`./dry_runs/t1`
Incomplete systems:
['SM04_octanol_0.0_1.0_GAFF_tip3p_equil', 'Celiprolol_octanol_0.0_1.0_GAFF_tip3p_equil', 'rPropranolol_octanol_0.0_1.0_GAFF_tip3p_equil', 'SM07_octanol_0.0_1.0_GAFF_tip3p_equil']
Completed: 34/38

`./dry_runs/t2`
Incomplete systems:
['Celiprolol_octanol_0.0_1.0_GAFF_tip3p_equil', '4Pentoxyphenol_octanol_0.0_1.0_GAFF_tip3p_equil']
Completed: 36/38

`./dry_runs/t3`
Incomplete systems:
['SM13_octanol_0.0_1.0_GAFF_tip3p_equil', 'Celiprolol_octanol_0.0_1.0_GAFF_tip3p_equil']
Completed: 36/38

I resubmitted the array jobs to give these a second try for finishing.


## 2019/08/19

### Analyzing dry octanol GAFF TIP3P Yank simulations.

Analysis scripts from Danielle:  
`/dry_runs/analysis/tools.py`  
`/dry_runs/analysis/test.py`  

Modified analysis scripts to skip problematic analysis an report NaN as free energy:  
`test_SAMPL6_molecules.py`  
`test_extra_molecules.py`


1) 4 hour interactive job request:  
$ bsub -n 1 -W 4:00 -Is /bin/bash  

2) Run:
$ conda activate SAMPL6_logP
$ python test_SAMPL6_molecules.py
$ python test_extra_molecules.py

4) Check if there are any NaN free energy reports in JSON output files:  
`SAMPL6_mols_trial_t1_GAFF_tip3p_dryoct.json`  
`SAMPL6_mols_trial_t2_GAFF_tip3p_dryoct.json`  
`SAMPL6_mols_trial_t3_GAFF_tip3p_dryoct.json`  

Problematic cases in t1:  
- SM02_octanol_0.0_1.0_GAFF_tip3p_equil  
- SM14_octanol_0.0_1.0_GAFF_tip3p_equil  
- Quinoline_octanol_0.0_1.0_GAFF_tip3p_equil  

Problematic cases in t2:  
- SM04_octanol_0.0_1.0_GAFF_tip3p_equil  
- Ketoprofen_octanol_0.0_1.0_GAFF_tip3p_equil   
- Pericyazine_octanol_0.0_1.0_GAFF_tip3p_equil  

Problematic cases in t3:  
- SM04_octanol_0.0_1.0_GAFF_tip3p_equil
- Ketoprofen_octanol_0.0_1.0_GAFF_tip3p_equil  
- Pericyazine_octanol_0.0_1.0_GAFF_tip3p_equil

I realized these problematic cases has threw NaN in the first iteration of Yank in water phase.
I need to rerun these. To rerun I have to remove the names of systems to rerun from `/dry_yank_results/dry_yank_mols_done.json` and keep the names of systems that I do not want to rerun.

## 2019/09/05

### Analyzing dry octanol GAFF TIP3P Yank simulations

I checked if previously failed cases that threw NaN in the first iteration of Yank simulation were able to run this time.

Problematic cases in t1:  
- SM02_octanol_0.0_1.0_GAFF_tip3p_equil  
- SM14_octanol_0.0_1.0_GAFF_tip3p_equil  
- Quinoline_octanol_0.0_1.0_GAFF_tip3p_equil  
- Sulfamethazine_octanol_0.0_1.0_GAFF_tip3p_equil  
 
Problematic cases in t2:  
- SM04_octanol_0.0_1.0_GAFF_tip3p_equil  
- Ketoprofen_octanol_0.0_1.0_GAFF_tip3p_equil  
- Pericyazine_octanol_0.0_1.0_GAFF_tip3p_equil  

Problematic cases in t3:  
- SM04_octanol_0.0_1.0_GAFF_tip3p_equil   
- Ketoprofen_octanol_0.0_1.0_GAFF_tip3p_equil  
- Pericyazine_octanol_0.0_1.0_GAFF_tip3p_equil  

To check if the XML files were correct and same between the 3 replicates I run diff command:   

$ diff t1/t1_dry_oct_XMLs/SM08_water_0.0_1.0_GAFF_tip3p.xml t2/t2_dry_oct_XMLs/SM08_water_0.0_1.0_GAFF_tip3p.xml  
$ diff t1/t1_dry_oct_XMLs/SM08_octanol_0.0_1.0_GAFF_tip3p.xml t2/t2_dry_oct_XMLs/SM08_octanol_0.0_1.0_GAFF_tip3p.xml  
$ diff t1/t1_dry_oct_XMLs/SM08_water_0.0_1.0_GAFF_tip3p.xml t3/t3_dry_oct_XMLs/SM08_water_0.0_1.0_GAFF_tip3p.xml  
$ diff t1/t1_dry_oct_XMLs/SM08_octanol_0.0_1.0_GAFF_tip3p.xml t3/t3_dry_oct_XMLs/SM08_octanol_0.0_1.0_GAFF_tip3p.xml  
$ diff t2/t2_dry_oct_XMLs/SM08_water_0.0_1.0_GAFF_tip3p.xml t3/t3_dry_oct_XMLs/SM08_water_0.0_1.0_GAFF_tip3p.xml  
$ diff t2/t2_dry_oct_XMLs/SM08_octanol_0.0_1.0_GAFF_tip3p.xml t3/t3_dry_oct_XMLs/SM08_octanol_0.0_1.0_GAFF_tip3p.xml  

There was no output proving the files are the same as they are supposed to. 


### Another attempt to run simulations that threw NaNs after deleting their solvent.nc and checkpoint files

I have to remove the names of systems to rerun from `/dry_yank_results/dry_yank_mols_done.json` and keep the names of systems that I do not want to rerun.
To restart simulations this time I will also remove the output files of these simulations from `/dry_yank_outputs/.
	 
$ cd /data/chodera/misik/SAMPL6_logP_ref_calc/dry_octanol_GAFF_tip3p/dry_runs/t1/dry_yank_output
$ rm -rf Sulfamethazine_octanol_0.0_1.0_GAFF_tip3p_equil
$ rm -rf Quinoline_octanol_0.0_1.0_GAFF_tip3p_equil
$ rm -rf SM14_octanol_0.0_1.0_GAFF_tip3p_equil
$ rm -rf SM02_octanol_0.0_1.0_GAFF_tip3p_equil
$ cd /data/chodera/misik/SAMPL6_logP_ref_calc/dry_octanol_GAFF_tip3p/dry_runs/t2/dry_yank_output
$ rm -rf SM04_octanol_0.0_1.0_GAFF_tip3p_equil
$ rm -rf Ketoprofen_octanol_0.0_1.0_GAFF_tip3p_equil
$ rm -rf Pericyazine_octanol_0.0_1.0_GAFF_tip3p_equil
$ cd /data/chodera/misik/SAMPL6_logP_ref_calc/dry_octanol_GAFF_tip3p/dry_runs/t3/dry_yank_output
$ rm -rf SM04_octanol_0.0_1.0_GAFF_tip3p_equil
$ rm -rf Ketoprofen_octanol_0.0_1.0_GAFF_tip3p_equil
$ rm -rf Pericyazine_octanol_0.0_1.0_GAFF_tip3p_equil

I restarted the runs.

If this does not work I will try to get rid off the problem which is causing NaNs in the first iteration of the water phase by preparing new equilibriated starting coordinates.


## 2019/09/06

### Creating new equilibriated starting configurations

Restarting failed simulations that threw NaNs at 1st iteration did not help. Now I will create new replicates of equilibriated systems and replace the old configurations.
I only ran equilibration for failing cases.

New equilibrated files are in this directory: ./extra_equilibration 

1) Copied new PDBs from equilibration to YANK inputs for dry octanol GAFF TIP3P Yank runs:
$ cp ./extra_equilibration/equilibration/1/equil_pdbs/*.pdb ./dry_runs/t1/t1_dry_oct_pdbs/
$ cp ./extra_equilibration/equilibration/2/equil_pdbs/*.pdb ./dry_runs/t2/t2_dry_oct_pdbs
$ cp ./extra_equilibration/equilibration/3/equil_pdbs/*.pdb ./dry_runs/t3/t3_dry_oct_pdbs

2) Remove old simulation outputs from /dry_runs/t*/dry_yank_output

3) Edit `/dry_yank_results/dry_yank_mols_done.json` to remove the names of simulations I want to run again. Leave the names of simulations that we do not need to run.


## 2019/09/09

### Analysis of new simulations

All SAMPL6 molecule runs finished properly.

$ cd dry_runs/analysis  
$ python test_SAMPL6_molecules.py  
$ python test_extra_molecules.py  
$ grep NaN  SAMPL6_mols_trial_t*_GAFF_tip3p_dryoct.json  

Only problematic simulation in t1:  Sulfamethazine_octanol_0.0_1.0_GAFF_tip3p_equil

To rerun equilibration for this system I removed Sulfamethazine entry form: `/extra_equilibration/equilibration/1/equil_results/equil_done.json`.
Then I resubmitted equilibration job:  
$ cd ./extra_equilibration/equilibration/1
$ bsub < equil-lsf.sh 

Copied finished equilibrated sulfamethazine PDBs to input directory of YANK runs:  
$ cd dry_runs/t1/t1_dry_oct_pdbs  
$ cp /data/chodera/misik/SAMPL6_logP_ref_calc/dry_octanol_GAFF_tip3p/extra_equilibration/equilibration/1/equil_pdbs/Sulfamethazine_water_0.0_1.0_GAFF_tip3p_equil.pdb ./  
$ cp /data/chodera/misik/SAMPL6_logP_ref_calc/dry_octanol_GAFF_tip3p/extra_equilibration/equilibration/1/equil_pdbs/Sulfamethazine_octanol_0.0_1.0_GAFF_tip3p_equil.pdb ./  
$ bsub < dry_yank_run-lsf.sh  


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
$ rm dry_yank_output/*/solvent2.nc
$ rm dry_yank_output/*/solvent2_checkpoint.nc

(3) Delete dry_yank_results/yank_mols_done.json

This will run all the systems again. Since octanol phase is completed, it should skip that phase.



