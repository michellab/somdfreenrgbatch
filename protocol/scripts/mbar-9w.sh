#!/bin/bash
#SBATCH -o analyse-free-nrg-%A.%a.out
#SBATCH -p GTX
#SBATCH -n 1
#SBATCH --time 00:05:00

srun ~/sire.app/bin/analyse_freenrg_mbar -i lambda-0.0000/simfile.dat lambda-0.1250/simfile.dat lambda-0.2500/simfile.dat lambda-0.3750/simfile.dat lambda-0.5000/simfile.dat lambda-0.6250/simfile.dat lambda-0.7500/simfile.dat lambda-0.8750/simfile.dat lambda-1.0000/simfile.dat --lam 0.0000 0.1250 0.2500 0.3750 0.500 0.6250 0.7500 0.8750 1.000 --temperature 298.0 -o mbar.pmf --subsampling percentage --percentage 95 > freenrg-MBAR.dat

bzip2 lambda-*/* 
