#! /bin/env python3
import os
from JobHelper import *
from argparse import ArgumentParser
from os.path import join

def modifyEnergy(macro,en):
    newmacro = []
    for j in range(len(macro)):
        s = macro[j]
        if("%(energy)s" in s):
            s = s%(en)
        if("templatepath" in s):
            s = s%(en)
        newmacro.append(s)
    return newmacro


parser = ArgumentParser()
parser.add_argument("-k", "--kill", action="store_true", help="kill running jobs")
parser.add_argument("--nruns",    type=int, help="number of runs for each energy")
parser.add_argument("--nevts",    type=int, help="events per run")
parser.add_argument("--startn",   type=int, help="starting run")
parser.add_argument("--maxen",   type=float, help="maximum energy to run")
parser.add_argument("--minen",   type=float, help="minimum energy to run")
parser.add_argument("--el",       help="element name (e.g Cu)")
parser.add_argument("--maxtime",  type=int, help="expected run time limit (s) for batch queue submissions")

options = parser.parse_args()

if options.kill:
    os.system("killall -9 parallel")
    os.system("killall -9 MaGe")
    os.system("killall -9 NeutronValidationLauncher.py")
    exit(0)

if  options.nruns and options.nevts and options.el:
    print("Launching %i runs of %i events for all materials" % (options.nruns,options.nevts))
    tempdir = "templates"
    datdir =  join(os.environ["MAGEDIR"],"validation/NeutronInteractions/dat")
    energies = readFile(join(datdir,"neutronEnergies.txt"))
    template = readFile(join(tempdir,options.el + ".mac"))
    templatepath = os.path.abspath(tempdir)
    for en in energies:
        if(options.maxen):
            if(float(en) > options.maxen): 
                break
        if(options.minen):
            if(float(en) < options.minen):
                continue
        en = en.strip()
        st = {"energy":en,"rnum":"%(rnum)s","templatepath":templatepath,"outdir":"%(outdir)s"}
        newmacro = modifyEnergy(template,st)
        thistemplate = join(tempdir,"{0}_{1}MeV.mac".format(options.el,en))
        writeFile(thistemplate,newmacro)
        L = MaGeLauncher("{0}_NeutronValidation".format(options.el,en), options.nevts)
        if options.maxtime: L.maxtime = options.maxtime
        L.template = thistemplate
        L.launch_sims(options.nruns,options.startn if options.startn else 0)
else:
    print("usage: NeutronValidationLauncher.py --nevts {number of events} --nruns {number of runs for each energy} --el {element name}\nexample: NeutronValidationLauncher.py --nevts 10000 --nruns 10 --el Cu")
