#!/bin/bash
#SBATCH -o analyse-free-nrg-%A.%a.out
#SBATCH -p Tesla
#SBATCH -n 1
#SBATCH --time 00:10:00

module load sire/17.1.0_no_avx
module load openmm/6.3

srun analyse_freenrg mbar -i lambda-*/simfile.dat --temperature 298.0 --percent 95 --overlap > freenrg-MBAR.dat

sleep 60

bzip2 lambda-*/*

