#!/bin/bash
#BSUB -J GAFF_t1[1-8] 
#BSUB -n 1
#BSUB -R rusage[mem=4]
#BSUB -R span[hosts=1]
#BSUB -q gpuqueue
#BSUB -gpu "num=1:j_exclusive=yes:mode=shared"
#BSUB -W  0:30
#BSUB -We 1:00
#BSUB -m "ld-gpu ls-gpu lt-gpu lp-gpu lg-gpu"
#BSUB -o %J.stdout
#BSUB -eo %J.stderr
#BSUB -L /bin/bash

# Set job directory
cd $LS_SUBCWD
echo “Job directory: ${LS_SUBCWD}”


# Activate environment
source activate SAMPL6_logP
conda list --export > requirements.txt

# Setting job_id is for running only the first job from the array.                   
# job_id=1 # for single job                                                                            
n_jobs=8


# Launch my program.
module load cuda/9.2
#module load cuda/9.1.85
#nvcc -V

# Run the simulation. 

# Single job
#echo "Running single job ${job_id}/${n_jobs}..."
#python run2.py ${job_id} ${n_jobs}

#Array Job
echo "Running array job $LSB_JOBINDEX/${n_jobs}..."
echo $LSB_JOBINDEX >> job_indices.txt 
python run2.py $LSB_JOBINDEX ${n_jobs}
echo "Done!" 

