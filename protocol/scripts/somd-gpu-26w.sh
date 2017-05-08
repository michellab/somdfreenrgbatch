#!/bin/bash
#SBATCH -o somd-array-gpu-%A.%a.out
#SBATCH -p GTX
#SBATCH -n 1
#SBATCH --gres=gpu:1
#SBATCH --time 24:00:00
#SBATCH --array=0-25

module load cuda/7.5

echo "CUDA DEVICES:" $CUDA_VISIBLE_DEVICES

lamvals=( 0.0000 0.0400 0.0800 0.1200 0.1600 0.2000 0.2400 0.2800 0.3200 0.3600 0.4000 0.4400 0.4800 0.5200 0.5600 0.6000 0.6400 0.6800 0.7200 0.7600 0.8000 0.8400 0.8800 0.9200 0.9600 1.0000 )

lam=${lamvals[SLURM_ARRAY_TASK_ID]}

sleep 5

echo "lambda is: " $lam

mkdir lambda-$lam
cd lambda-$lam

export OPENMM_PLUGIN_DIR=/home/julien/sire.app/lib/plugins/

srun /home/julien/sire.app/bin/somd-freenrg -C ../../input/sim.cfg -l $lam -p CUDA
cd ..

wait

if [ "$SLURM_ARRAY_TASK_ID" -eq "25" ]
then
    sleep 600
    sbatch ../mbar.sh
fi

