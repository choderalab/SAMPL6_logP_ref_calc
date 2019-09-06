#!/bin/bash
#PBS -q home
#PBS -A mobley-bergazin
#PBS -l nodes=1:ppn=4:gpu
#PBS -l walltime=00:30:00
#PBS -M bergazin@uci.edu
#PBS -N trial1_equil
#PBS -j oe

. $HOME/anaconda3/etc/profile.d/conda.sh
conda activate
conda activate sampl
conda list
cd ${PBS_O_WORKDIR}
echo "Job directory: ${PBS_O_WORKDIR}"
echo "Nodes chosen are:"
cat $PBS_NODEFILE
module load cuda/9.1.85
#export CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES
#echo "Running on GPU IDX: $CUDA_VISIBLE_DEVICES"
nvcc -V

job_id=1
n_jobs=76

# Run the simulation. Distinguish between array
# of jobs and multiple singular jobs.
if [ -n "$PBS_ARRAYID" ]; then
  echo "Running array job $PBS_ARRAYID/${n_jobs}..."
  python run2.py $PBS_ARRAYID ${n_jobs}
else
  echo "Running single job ${job_id}/${n_jobs}"
  python run2.py ${job_id} ${n_jobs}
fi

conda deactivate sampl
