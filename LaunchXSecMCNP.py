#! /bin/env python3
import os
from argparse import ArgumentParser
from os.path import join
from MCNPLauncher import *
from JobHelper import readFile
"""use parallel -jobs <n> < nameoffile.txt where <n> is some fraction of numbner of cpus"""

ELEDAT = """
208 82 11.34
74 32 5.323
76 32 5.323
63 29 8.96
158 64 7.90
40 18 1.44
1 1 0.0708
12 6 2.20
14 7 0.804
16 8 1.13
"""

def main():
    parser = ArgumentParser()
    parser.add_argument("-k", "--kill", action="store_true", help="kill running jobs")
    parser.add_argument("--Z",     help="element Z value")
    parser.add_argument("--n",     help="number of events for each energy")
    options = parser.parse_args()
    if options.kill:
        os.system("killall -9 parallel")
        os.system("killall -9 mcnp6")
    tempdir = "templates"
    datdir =  join(os.environ["MAGEDIR"],"validation/NeutronInteractions/dat")
    energies = readFile(join(datdir,"neutronEnergies.txt"))
    energies = [e.rstrip() for e in energies]
    energies = energies[0:2]
    template = join(tempdir,"xsec_template.c")
    data = {}
    for line in ELEDAT.split("\n"):
        line = line.rstrip()
        dat = line.split(" ")
        if(len(dat) > 1):
            data[dat[1] + "000"] = dat[2].rstrip()
    extra = {}
    if(options.Z):
        extra["matnum"] = options.Z + "000"
        extra["density"] = data[options.Z + "000"]
    L = JobLauncher(join("XSec",extra["matnum"]),template,options.n,0,extra)
    L.launch_en_sims(energies)

if __name__=="__main__":
    main()



