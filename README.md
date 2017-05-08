# somdfreenrgbatch

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

bash ./setupall.sh
bash ./run1all.sh

@@@ Stage 4 = Collect free energies once the jobs have completed

NOTE: This script has been deprecated by https://github.com/michellab/freenrgworkflows 

python ./collate-results.py




