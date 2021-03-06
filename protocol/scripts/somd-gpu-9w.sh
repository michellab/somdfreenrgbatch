#!/bin/bash
#SBATCH -o somd-array-gpu-%A.%a.out
#SBATCH -p Tesla
#SBATCH -n 1
#SBATCH --gres=gpu:1
#SBATCH --time 24:00:00
#SBATCH --array=0-8

module load cuda/7.5
module load sire/17.1.0_no_avx
module load openmm/6.3

echo "CUDA DEVICES:" $CUDA_VISIBLE_DEVICES

lamvals=( 0.0000 0.1250 0.2500 0.3750 0.5000 0.6250 0.7500 0.8750 1.0000 )
lam=${lamvals[SLURM_ARRAY_TASK_ID]}

sleep 5

echo "lambda is: " $lam

mkdir lambda-$lam
cd lambda-$lam

export OPENMM_PLUGIN_DIR=/home/julien/sire.app/lib/plugins/

srun somd-freenrg -C ../../input/sim.cfg -l $lam -p CUDA
cd ..

wait

if [ "$SLURM_ARRAY_TASK_ID" -eq "8" ]
then
    sleep 600
    sbatch ../mbar.sh
fi

