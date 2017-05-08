#!/bin/bash
#SBATCH -o analyse-free-nrg-%A.%a.out
#SBATCH -p GTX
#SBATCH -n 1
#SBATCH --time 00:05:00

srun ~/sire.app/bin/analyse_freenrg_mbar -i lambda-0.0000/simfile.dat lambda-0.0400/simfile.dat lambda-0.0800/simfile.dat lambda-0.1200/simfile.dat lambda-0.1600/simfile.dat lambda-0.2000/simfile.dat lambda-0.2400/simfile.dat lambda-0.2800/simfile.dat lambda-0.3200/simfile.dat lambda-0.3600/simfile.dat lambda-0.4000/simfile.dat lambda-0.4400/simfile.dat lambda-0.4800/simfile.dat lambda-0.5200/simfile.dat lambda-0.5600/simfile.dat lambda-0.6000/simfile.dat lambda-0.6400/simfile.dat lambda-0.6800/simfile.dat lambda-0.7200/simfile.dat lambda-0.7600/simfile.dat lambda-0.8000/simfile.dat lambda-0.8400/simfile.dat lambda-0.8800/simfile.dat lambda-0.9200/simfile.dat lambda-0.9600/simfile.dat lambda-1.0000/simfile.dat --lam 0.0000 0.0400 0.0800 0.1200 0.1600 0.2000 0.2400 0.2800 0.3200 0.3600 0.4000 0.4400 0.4800 0.5200 0.5600 0.6000 0.6400 0.6800 0.7200 0.7600 0.8000 0.8400 0.8800 0.9200 0.9600 1.0000 --temperature 298.0 -o mbar.pmf --subsampling percentage --percentage 95 > freenrg-MBAR.dat

bzip2 lambda-*/*
