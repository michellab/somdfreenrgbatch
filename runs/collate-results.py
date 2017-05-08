#!/usr/bin/python
import os,sys
from math import *


def getDGTI(path):
    if not os.path.exists(path):
        return [999.0, 999.0]

    stream = open(path,'r')
    buffer = stream.readlines()
    stream.close()
    elems = buffer[0].split()
    DG = float( elems[2] )
    err = 0.0

    return [DG, err]


def getDGMBAR(path):

    if not os.path.exists(path):
        return [999.0, 999.0]

    stream = open(path,'r')
    buffer = stream.readlines()
    stream.close()
    if len(buffer) < 5:
        return [999.0, 999.0]    
    elems = buffer[-4].split()
    if len(elems) < 10:
        return [999.0, 999.0]
    DG = float( elems[7] )
    err = float( elems[10] )

    return [DG, err]

def getDGLJLRC(path):
    if not os.path.exists(path):
        return [999.0, 999.0]

    stream = open(path,'r')
    buffer = stream.readlines()
    stream.close()
    if ( len(buffer) < 1):
        return [999.0, 999.0]

    elems = buffer[0].split()
    DG = float( elems[2] )
    err = float( elems[4] )

    return [DG, err]


def getDGCOUL(path):

    if not os.path.exists(path):
        return [999.0, 999.0], [999.0, 999.0], [999.0, 999.0]

    stream = open(path,'r')
    buffer = stream.readlines()
    stream.close()
    if (len(buffer) < 2):
        return [999.0, 999.0], [999.0, 999.0], [999.0, 999.0]       
    elems = buffer[-4].split()
    if len(elems) < 4:
        return [999.0, 999.0], [999.0, 999.0], [999.0, 999.0]
    DG_POL = float( elems[2] )
    err_POL = float( elems[4] )

    elems = buffer[-3].split()
    DG_PSUM = float( elems[2] )
    err_PSUM = float( elems[4] )

    elems = buffer[-2].split()
    DG_FUNC = float( elems[2] )
    err_FUNC = float( elems[4] )

    return [DG_POL, err_POL], [DG_PSUM, err_PSUM], [DG_FUNC, err_FUNC]

def addResults( results ):
    DG = 0.0
    err = 0.0

    for result in results:
        #print result
        DG += result[0]
        err += pow(result[1],2)
    err = sqrt(err)
    return [DG, err]

def subResultsTwo( results ):
    DG = 0.0
    err = 0.0
    
    DG = results[0][0]-results[1][0]
    err += pow(results[0][1],2)
    err += pow(results[1][1],2)
    err = sqrt(err)
    return [DG, err]

cwd = os.getcwd()

files = os.listdir( cwd )

excluded = ['protocol']

results = {}

for mol in files:
    if mol in excluded:
        continue
    #if mol.find("~") < 1:
    #    print mol
    #    print "AAAAS"
    #    continue
    if os.path.isdir(mol):
        if mol.find("~") < 1:
            continue
        print mol
        results[mol] = {}
        
        results[mol]['DG_bound'] = getDGMBAR("%s/bound/run001/sim/output/freenrg-MBAR.dat" % mol)
        results[mol]['DG_POL_bound'], \
        results[mol]['DG_PSUM_bound'],\
        results[mol]['DG_FUNC_bound'] = getDGCOUL("%s/bound/run001/sim/output/freenrg-COULCOR.dat" % mol)
        results[mol]['DG_LJ_LRC_bound'] = getDGLJLRC("%s/bound/run001/sim/output/freenrg-LJCOR.dat" % mol)

        results[mol]['DG_free'] = getDGMBAR("%s/free/run001/sim/output/freenrg-MBAR.dat" % mol)
        results[mol]['DG_POL_free'], \
        results[mol]['DG_PSUM_free'],\
        results[mol]['DG_FUNC_free'] = getDGCOUL("%s/free/run001/sim/output/freenrg-COULCOR.dat" % mol)
        results[mol]['DG_LJ_LRC_free'] = getDGLJLRC("%s/free/run001/sim/output/freenrg-LJCOR.dat" % mol)

        results[mol]['DG_vac'] = getDGMBAR("%s/vac/run001/sim/output/freenrg-MBAR.dat" % mol)

#print results

outstream = open('summary.csv','w')

outstream.write("#@@@@@@\n")
outstream.write("#perturbation\t\t\t\t\tDG_free_to_bound  err\n")#\tDG_vac_to_free\terr\n")


done = []

for pert in results:
    if pert in done:
        continue
    print "#####################"
    print pert
    A, B = pert.split("~")
    pert_comma = "%s,%s" %(A,B)
    results[pert]['DG_free_to_bound'] = subResultsTwo( [ results[pert]['DG_bound'], results[pert]['DG_free'] ] )
    results[pert]['DG_vac_to_free'] = subResultsTwo( [ results[pert]['DG_free'], results[pert]['DG_vac'] ] )

    outline = "%s," % pert_comma
    outline += "%.2f,%.2f" % (results[pert]['DG_free_to_bound'][0], results[pert]['DG_free_to_bound'][1])
    #outline += "%.2f\t%8.2f\t" % (results[pert]['DG_vac_to_free'][0], results[pert]['DG_vac_to_free'][1])
    outline += '\n'

    outstream.write(outline)

    keys  = results[pert].keys()
    keys.sort()
    for key in keys:
        #print key
        print ("%s %8.5f +/- %8.5f kcal/mol" % (key, results[pert][key][0], results[pert][key][1]) )

    done.append(pert)

    A, B = pert.split("~")
    reverse = "%s~%s" % (B,A)
    reverse_comma = "%s,%s" % (B,A)
    if results.has_key(reverse):
            print "###################"
            print reverse
            results[reverse]['DG_free_to_bound'] = subResultsTwo( [ results[reverse]['DG_bound'], results[reverse]['DG_free'] ] )
            results[reverse]['DG_vac_to_free'] = subResultsTwo( [ results[reverse]['DG_free'], results[reverse]['DG_vac'] ] )
            outline = "%s," % reverse_comma
            outline += "%.2f,%.2f" % (results[reverse]['DG_free_to_bound'][0], results[reverse]['DG_free_to_bound'][1])
            #outline += "%8.2f\t%8.2f\t" % (results[reverse]['DG_vac_to_free'][0], results[reverse]['DG_vac_to_free'][1])
            outline += '\n#####\n'
        
            outstream.write(outline)

            keys  = results[reverse].keys()
            keys.sort()
            for key in keys:
                #print key
                print ("%s %8.5f +/- %8.5f kcal/mol" % (key, results[reverse][key][0], results[reverse][key][1]) )

            done.append(reverse)
            #sys.exit(-1)

#print results

