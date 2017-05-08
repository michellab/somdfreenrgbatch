#!/bin/python

import os,sys

try:
    lig = sys.argv[1]
except IndexError:
    print "Usage is script ligand-name"
    sys.exit(-1)

template = """
[globals]
forcefield = amber, ff14SB, tip3p, hfe
gaff = gaff2
mdengine = amber, pmemd
logfile = dGPrep-%s.log
AFE.type = Sire
AFE.separate_vdw_elec = false 

[ligand]
basedir = poses
file.name = ligand.pdb
molecules = %s

box.type = rectangular
box.length = 12.0
neutralize = False

min.nsteps = 200
min.ncyc = 100
min.restr_force = 10.0
min.restraint = notsolvent

# heat the system to the final temperature running NVT
md.heat.nsteps = 1000
md.heat.T = 300.0
md.heat.restraint = notsolvent
md.heat.restr_force = 5.0

# fix the density of the system running NpT
md.press.nsteps = 5000
md.press.T = 300.0
md.press.p = 1.0
md.press.restraint = notsolvent
md.press.restr_force = 4.0

# restraints release in 4 steps, this is a NpT protocol
md.relax.nrestr = 4
md.relax.nsteps = 500
md.relax.T = 300.0
md.relax.p = 1.0
md.relax.restraint = notsolvent

[protein]
basedir = protein
file.name = fxr_set2_md_wat.pdb
molecules = SIM 

[complex]
pairs = SIM : %s

box.type = rectangular
box.length = 10.0
align_axes = True
neutralize = True

min.nsteps = 2000
min.ncyc   = 1000
min.restr_force = 10.0
min.restraint = :LIG

# heat the system to the final temperature running NVT
md.heat.nsteps = 1000
md.heat.T = 300.0
md.heat.restraint = bb_lig
md.heat.restr_force = 5.0

# fix the density of the system running NpT
md.press.nsteps = 5000
md.press.T = 300.0
md.press.p = 1.0
md.press.restraint = :LIG
md.press.restr_force = 4.0

# restraints release in 4 steps, this is a NpT protocol
md.relax.nrestr = 4
md.relax.nsteps = 500
md.relax.T = 300.0
md.relax.p = 1.0
md.relax.restraint = :LIG

""" % (lig,lig,lig)

setupfile = "setup-%s.in" % lig

stream = open(setupfile,'w')
stream.write(template)
stream.close()

templatesub="""#!/bin/bash
#SBATCH -o FESetup-%s.out
#SBATCH -p main
#SBATCH --time 48:00:00
#SBATCH -n 1
#SBATCH -N 1
#source /etc/profile.d/module.sh
#module load FESetup

FESetup %s
wait
""" % (lig,setupfile)

subfile = "fesetup-%s.sh" % lig
stream = open(subfile,"w")
stream.write(templatesub)
stream.close()

#cmd = "sbatch %s" % (subfile)
#print (cmd)
#os.system(cmd)


cmd = "FESetup %s > setup-%s.dat &" % (setupfile,lig)
os.system(cmd)
