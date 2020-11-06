#!/bin/bash
#BSUB -J "gaff_tip3p[1-27]"
#BSUB -n 1
#BSUB -R rusage[mem=8]
#BSUB -R span[hosts=1]
#BSUB -q gpuqueue
#BSUB -gpu "num=1:j_exclusive=yes:mode=shared"
#BSUB -W  10:00
#BSUB -We 8:30
#BSUB -m "ld-gpu ls-gpu lt-gpu lp-gpu lg-gpu"
#BSUB -o %J.stdout
#BSUB -eo %J.stderr
#BSUB -L /bin/bash

# Number of jobs in this array
n_jobs=27

# Change working directory
cd $LS_SUBCWD
echo “Job directory: ${LS_SUBCWD}”

# Print PATH variable
echo "PATH:"
echo $PATH

# Activate environment
source activate SAMPL6_logP
conda list --export > requirements.txt

# Launch my program.
module load cuda/9.2
echo “Running array job $LSB_JOBINDEX/${n_jobs}...”
echo $LSB_JOBINDEX >> job_indices.txt
python wet_run_yank.py $LSB_JOBINDEX ${n_jobs}
echo "Done!"
