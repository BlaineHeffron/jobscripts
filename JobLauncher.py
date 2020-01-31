#! /bin/env python3
from JobHelper import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-k", "--kill", action="store_true", help="kill running jobs")
parser.add_argument("--name",     help="simulation output name")
parser.add_argument("--template", help="macro template file")
parser.add_argument("--nruns",    type=int, help="number of runs")
parser.add_argument("--nevts",    type=int, help="events per run")
parser.add_argument("--startn",   type=int, help="starting run")
parser.add_argument("--maxtime",  type=int, help="expected run time limit (s) for batch queue submissions")

options = parser.parse_args()

if options.kill:
    os.system("killall -9 parallel")
    os.system("killall -9 MaGe")
    os.system("killall -9 JobLauncher.py")
    exit(0)

if options.template and options.nruns and options.nevts and options.name:
    print("Launching '%s' with %i runs of %i events using template '%s'"
          % (options.name,options.nruns,options.nevts,options.template))
    L = MaGeLauncher(options.name, options.nevts)
    if options.maxtime: L.maxtime = options.maxtime
    L.template = options.template
    L.launch_sims(options.nruns,options.startn if options.startn else 0)
