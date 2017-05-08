# somdfreenrgbatch

This is a brief summary of the steps taken to setup, simulate and analyse relative binding free energy calculations 
as part of the D3R 2016 grand challenge using the codes FESetup and somd-freenrg. 
The scripts are customised for deployment on a specific cluster. The protocol is evolving with every projects and 
the code below was tested with sire 2016.1. 

@@@ Stage 1 = Generate input files with FESetup

cd $BASEDIR/fesetup

* Add the prepared protein pdb file to protein/SIM/ folder. See protein-example 
* Create poses subfolders in the poses folder. See poses-example
* Edit the setup protocol in setmeup.py as needed. Most parameters should be ok if you want to setup input files for somd. 
You will have to change file/folder names in the [protein] section.
The templatesub variable is cluster specific and will need editing
* Submit a FESetup job for each pose of interest e.g.

python setmeup.y FXR_10_BM1

* Once the setup jobs for all poses of interest have completed, prepare a morph.in file and generate morphs.
See morph.in.example for an example where manual mappings are made in some instances to enforce desired substructure matches. 

FESetup morph.in > MORPHS.out

@@@ Stage 2 = Edit the simulation protocol files

cd $BASEDIR/protocol

Most files do not need to be changed here. However take a look at the scripts subfolder

cd scripts

This contains three types of files
mbar-*.sh --> mbar slurm analysis scripts. Cluster specific. There are three variants, each for a given lambda schedule (NOTE: This was for sire 2016.X. The analyse_freenrg UI has been overhauled in sire 2017.1)
somd-gpu*.sh --> somd-freenrg submission scripts with three different lambda schedule. Cluster specific.
sim-solvated-ncycles-100-* --> config files. Set to run a 4ns simulation for each lambda value. Adjust nmoves, ncycles to change the length of the trajectory. 

@@@ Stage 3 = Setup and submit the somd-freenrg simulatons

cd $BASEDIR/run

Edit the file jobtype.dat to specify the number of windows to use for a given perturbation (9, 17 or 26). This depends on whether you consider a perturbation to be 
'easy', 'medium' or 'hard'. In this use case we based our decision on preliminary results we obtained from a previous batch. 

bash ./setupall.sh
bash ./run1all.sh

@@@ Stage 4 = Collect free energies once the jobs have completed

NOTE: This script has been deprecated by https://github.com/michellab/freenrgworkflows 

python ./collate-results.py




