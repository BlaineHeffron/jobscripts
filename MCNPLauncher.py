from argparse import ArgumentParser
import os
import multiprocessing
import sys

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class JobLauncher:
    def __init__(self,nm,temp,nevt,startn=0,extra={}):
        self.settings = {"nevents":nevt, "simName":nm,"runName": "Run_%(jobnum)s"}
        self.template = temp
        self.bin_name = "mcnp6"
        self.startn = startn
        if(extra):
            self.settings["extra"] = {}
            for key in extra:
                self.settings["extra"][key] = extra[key]

    def set_dirs(self):
        self.settings["outdir"] = os.environ["MCNP_OUTDIR"]+"/"+self.settings["simName"]
        self.macro_dir = self.settings["outdir"] + "/cards"
        self.output_dir = self.settings["outdir"] + "/output"
        os.system("mkdir -p %s"%self.settings["outdir"])
        os.system("mkdir -p %s"%self.macro_dir)
        os.system("mkdir -p %s"%self.output_dir)

    def copyExtra(self,js):
        if("extra" in self.settings):
            for key in self.settings["extra"]:
                js[key] = self.settings["extra"][key]

    def launch_sims(self, nruns):
        self.set_dirs()
        inseed = 19073482328125
        jobsettings = {"nevts":self.settings["nevents"],"seed":""}
        self.copyExtra(jobsettings)
        jobcmds = []
        rnmin = self.startn
        print('run min is ',rnmin)
        for i in range(rnmin,nruns+rnmin):
            jobsettings["seed"] = inseed + 2*i
            jobsettings["jobnum"] = str(i)
            macrodat = open(self.template,"r").read()%jobsettings
            rname = self.settings["runName"]%jobsettings
            fpath  = os.path.expanduser("%s/%s.c"%(self.macro_dir,rname))
            open(fpath,"w").write(macrodat)
            jobcmds.append("mcnp6 R I=%s O=%s RUNTPE=%s"%(fpath,rname+"_outp",rname+"_tpe"))

        nproc = multiprocessing.cpu_count()
        with(cd(os.path.expanduser(self.output_dir))):
            print("attempting to use 4/5 of " + str(nproc) + " cores")
            pool = multiprocessing.Pool(processes=int(nproc*.8))
            pool.map(os.system,jobcmds)

    def launch_en_sims(self, energies):
        self.set_dirs()
        inseed = 19073482328125
        jobsettings = {"nevts":self.settings["nevents"],"seed":""}
        self.copyExtra(jobsettings)
        jobcmds = []
        rnmin = self.startn
        self.settings["runName"] = "Run_%(energy)s"
        for en in energies:
            #jobsettings["seed"] = inseed + 2*i
            jobsettings["seed"] = inseed
            jobsettings["energy"] = en
            macrodat = open(self.template,"r").read()%jobsettings
            rname = self.settings["runName"]%jobsettings
            fpath  = os.path.expanduser("%s/%s.c"%(self.macro_dir,rname))
            open(fpath,"w").write(macrodat)
            jobcmds.append("mcnp6 R I=%s O=%s RUNTPE=%s PTRAC=%s"%(fpath,rname+"_outp",rname+"_tpe",rname+"_ptrac"))
        nproc = multiprocessing.cpu_count()
        with(cd(os.path.expanduser(self.output_dir))):
            print("attempting to use 4/5 of " + str(nproc) + " cores")
            pool = multiprocessing.Pool(processes=int(nproc*.8))
            pool.map(os.system,jobcmds)


def main():
    parser = ArgumentParser()
    parser.add_argument("-k", "--kill", action="store_true", help="kill running jobs")
    parser.add_argument("--name",     help="simulation output name")
    parser.add_argument("--template", help="macro template file")
    parser.add_argument("--nruns",    type=int, help="number of runs")
    parser.add_argument("--nevts",    type=int, help="events per run")
    parser.add_argument("--startn",   type=int, help="starting run")

    options = parser.parse_args()

    if options.kill:
        os.system("killall -9 parallel")
        os.system("killall -9 mcnp6")
        exit(0)
    if options.template and options.nruns and options.nevts and options.name:
        print("Launching '%s' with %i runs of %i events using template '%s'"
              % (options.name,options.nruns,options.nevts,options.template))
        L = None
        if(options.startn):
            L = JobLauncher(options.name,options.template,options.nevts,options.startn)
        else:
            L = JobLauncher(options.name,options.template,options.nevts)
        L.launch_sims(options.nruns)
    else:
        print("set template, nruns, nevts, and name")
        exit(0)

if __name__=="__main__":
    main()
