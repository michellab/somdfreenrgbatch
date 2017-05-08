#!/usr/bin/python

import os
import sys


freeinput = "solvated"
boundinput = "complex"
morph = "MORPH.onestep.pert"
jobtype = "jobtype.dat"

if len(sys.argv) != 4:
    print ("USAGE IS setup.py protocolfolder pertsfolder pert")
    sys.exit(-1)

protocol = sys.argv[1]
pertsfolder = sys.argv[2]
if pertsfolder.endswith("/"):
    pertsfolder = pertsfolder[0:-1]

pert=sys.argv[3]

stream = open(jobtype,'r')
buffer = stream.readlines()
stream.close()
nw = -1
for line in buffer:
    elems = line.split()
    if elems[0] == pert:
        nw = elems[1] 
        break
print (pertsfolder, pert, nw)

if os.path.exists(pert):
    print ("There is already a folder named %s. Abort" % pert)
    sys.exit(-1)

cmd = "cp -a %s %s" % (protocol, pert)
print (cmd)
os.system(cmd)

#
# Now set correct protocol
#
os.chdir("%s/scripts/" % pert)

cmd  = "ln -s sim-solvated-ncycles-100-%s.cfg sim-solvated-ncycles-100.cfg" % nw
os.system(cmd)

cmd  = "ln -s somd-gpu-%s.sh somd-gpu.sh" % nw
os.system(cmd)

cmd  = "ln -s mbar-%s.sh mbar.sh" % nw
os.system(cmd)

os.chdir("../../")

#sys.exit(-1)

cmd = "cp %s/%s/%s/solvated.* %s/free/input" % (pertsfolder,pert,freeinput,pert)
print (cmd)
os.system(cmd)

cmd = "cp %s/%s/%s/solvated.* %s/bound/input" % (pertsfolder,pert,boundinput,pert)
print (cmd)
os.system(cmd)

#cmd = "cp  %s/%s/%s/distres %s/bound/input" % (pertsfolder,pert,boundinput,pert)
#print (cmd)
#os.system(cmd)

cmd = "cp %s/%s/vacuum.* %s/vac/input/" % (pertsfolder,pert,pert)
print (cmd)
os.system(cmd)

cmd = "cp %s/%s/%s %s/pert/MORPH.pert" % (pertsfolder,pert,morph,pert)
print (cmd)
os.system(cmd)


