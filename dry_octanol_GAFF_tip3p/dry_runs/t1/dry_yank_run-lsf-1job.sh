#!/bin/bash
#BSUB -J “dry_oct_t1_1”
#BSUB -n 1
#BSUB -R rusage[mem=16]
#BSUB -R span[hosts=1]
#BSUB -q gpuqueue
#BSUB -gpu "num=1:j_exclusive=yes:mode=shared"
#BSUB -W  10:00
#BSUB -We 11:30
##BSUB -m “ls-gpu lt-gpu lp-gpu lg-gpu”
#BSUB -m "ld-gpu ls-gpu lt-gpu lp-gpu lg-gpu"
#BSUB -o %J.stdout
##BSUB -cwd “/scratch/%U/%J”
#BSUB -eo %J.stderr
#BSUB -L /bin/bash

# Setting job_id is for running only the first job from the array.
job_id=1
n_jobs=38

cd $LS_SUBCWD

echo “Job directory: ${LS_SUBCWD}”

# Print PATH variable
echo "PATH:"
echo $PATH
echo "End of PATH."

# Activate environment
# conda init bash
# conda activate
source activate SAMPL6_logP
conda list --export > requirements.txt

# Launch my program.
module load cuda/9.2

echo “Running array job ${job_id}/${n_jobs}...”
python dry_run_yank.py ${job_id} ${n_jobs}
echo "Done!"
