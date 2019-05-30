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




