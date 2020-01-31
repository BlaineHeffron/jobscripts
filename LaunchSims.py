#! /bin/env python3
from JobLauncher import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-k", "--kill", action="store_true", help="kill running jobs")
parser.add_argument("--name",     help="simulation output name")
parser.add_argument("--template", help="macro template file")
parser.add_argument("--nruns",    type=int, help="number of runs")
parser.add_argument("--nevts",    type=int, help="events per run")
parser.add_argument("--startn",   type=int, help="starting run")
parser.add_argument("--maxtime",  type=int, help="expected run time limit (s) for batch queue submissions")
parser.add_argument("--root",     action="store_true", help=".root output instead of default .h5")

options = parser.parse_args()

if options.kill:
    os.system("killall -9 parallel")
    os.system("killall -9 MaGe")
    os.system("killall -9 LaunchSims.py")
    exit(0)

if options.template and options.nruns and options.nevts and options.name:
    print("Launching '%s' with %i runs of %i events using template '%s'"
          % (options.name,options.nruns,options.nevts,options.template))
    L = PG4_Launcher(options.name, options.nevts)
    if options.maxtime: L.maxtime = options.maxtime
    if options.root: L.settings["out_sfx"] = "root"
    L.template = options.template
    L.launch_sims(options.nruns, options.startn if options.startn else 0)

#################
# P50:
# nBG: 4e5 in 1500s (=1625s sim) on borax
# ./LaunchSims.py --name=P50D_nBG --template=Templates/P50_nBG.mac --nruns=800 --nevts=400000 --maxtime=2000
# muBG: 2e7 in 2500s (= 184s sim) on borax
# ./LaunchSims.py --name=P50D_muBG --template=Templates/P50_muBG.mac --nruns=800 --nevts=20000000 --maxtime=3600

#########
## AD1 ##
#########
#
# IBD: 1e5 in 20min
# ./LaunchSims.py --name=AD1_IBD --template=Templates/AD1_IBD.mac --nruns=200 --nevts=100000 --maxtime=1800
# AD1_muBG.mac: 1e7 in 3600s (= 90s sim) on borax
# ./LaunchSims.py --name=AD1_muBG --template=Templates/AD1_muBG.mac --nruns=800 --nevts=10000000 --maxtime=4800
# AD1 nBG: 1e5 "indoors" (=167s sim) in 20min
# ./LaunchSims.py --name=AD1_indoor_nBG --template=Templates/AD1_indoor_nBG.mac --nruns=400 --nevts=300000 --maxtime=4800
# AD1 nBG with building: 1e5 (=15.7s sim) in 16min
# ./LaunchSims.py --name=AD1_nBG --template=Templates/AD1_nBG.mac --nruns=100 --nevts=30000 --maxtime=3600
# GammaBG: 1e7 in 15min (=8s sim)
# InternalGamma (3MeV): 2e5 in 88s
# Phase2 nBG: 1e5 in 25min (=19s sim)
# muBG: 2e3 events/s (=0.02s sim); bare: 2e6 in 393s (=18s sim)
