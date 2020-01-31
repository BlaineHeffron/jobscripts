#! /bin/env python3
import os
from JobHelper import *
from argparse import ArgumentParser
from os.path import join

parser = ArgumentParser()
parser.add_argument("-k", "--kill", action="store_true", help="kill running jobs")
parser.add_argument("--nruns",    type=int, help="number of runs for each energy")
parser.add_argument("--nevts",    type=int, help="events per run")
parser.add_argument("--startn",   type=int, help="starting run")
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
    energies = readfile(join(datdir,"neutronEnergies.txt"))
    template = readfile(join(tempdir,options.el + ".mac"))
    for en in energies:
        st = {"energy":en}
        macrodat = open(template,"r").read()%st
        thistemplate = join("template","_{0}MeV.mac".format(en))
        open(thistemplate,"w").write(macrodat)
        L = MaGeLauncher(options.name, options.nevts)
        if options.maxtime: L.maxtime = options.maxtime
        L.template = thistemplate
        L.launch_sims(options.nruns,options.startn if options.startn else 0)
else:
    print("usage: NeutronValidationLauncher.py --nevts {number of events} --nruns {number of runs for each energy} --el {element name}\nexample: NeutronValidationLauncher.py --nevts 10000 --nruns 10 --el Cu")
