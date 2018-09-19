#!/bin/bash
#SBATCH -o analyse-free-nrg-%A.%a.out
#SBATCH -p GTX
#SBATCH -n 1
#SBATCH --time 00:10:00

srun ~/sire.app/bin/analyse_freenrg mbar -i lambda-*/simfile.dat --temperature 298.0 --percent 95 --overlap > freenrg-MBAR.dat

sleep 60

bzip2 lambda-*/*

