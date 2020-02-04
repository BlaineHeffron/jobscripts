import os

def readFile(filename):
# opens a file ("filename") and returns the content as a list of strings ("l")
    l = []
    f = open(filename, 'r')
    for line in f:
        l.append(line)
    f.close()
    return l

def writeFile(filename,l):
# creates a file ("filename") from a list of strings ("l")    
    f = open(filename, 'w')
    for i in range(len(l)):
        f.write(l[i])
    f.close()
    
class qsubmitter:
    """Submission as qsub jobs array"""
    def __init__(self,nm):
        self.settings = {"jobname":nm, "xcmds":""}
        self.setup = """#!/bin/bash
#PBS -j oe
#PBS -N %(jobname)s
#PBS -q batch
#PBS -l walltime=4:00:00"""

    def start_index(self): return 1

    def run_jobs(self, jcmd, lcmd, r0, r1):
        subcmd = (self.setup + "\n#PBS -t %i-%i"%(r0+1, r1) + "\n%(xcmds)s\n")%self.settings
        subcmd += "source ${HOME}/.bashrc\n"
        subcmd += jcmd%{"jobnum":"${PBS_ARRAYID}"} + "\n"
        open("job_submit","w").write(subcmd)
        os.system("cat job_submit")
        os.system("qsub -p -500 job_submit")
        os.system("rm job_submit")

class MaGeLauncher:

    def __init__(self, simname, nevt):
        self.settings = {"nevts":nevt, "rnum":0}
        self.settings["simName"] = simname
        self.settings["preinit"] = ""
        self.settings["postinit"] = ""
        self.settings["run_name"] = "Run_%(jobnum)s"
        self.maxtime = 4*3600
        self.template = "templates/Generic.mac"
        self.bin_name = "MaGe"
        self.submitter = qsubmitter(self.settings["simName"])

    def set_dirs(self):
        self.settings["outdir"] = os.environ["MAGEOUTDIR"]+"/"+self.settings["simName"]
        self.macro_dir = self.settings["outdir"]+"/mac/"
        self.log_dir = self.settings["outdir"]+"/log/"

        os.system("mkdir -p %s"%self.settings["outdir"])
        os.system("mkdir -p %s"%self.macro_dir)
        os.system("mkdir -p %s"%self.log_dir)

    def build_and_launch_macros(self, jobsettings, rnmin=0):
        if "outdir" not in self.settings:
            self.set_dirs()

        nruns = len(jobsettings)
        i0 = self.submitter.start_index()
        self.submitter.maxtime = self.maxtime

        # build macros for each setting
        for n,st0 in enumerate(jobsettings):
            st = self.settings.copy()
            st.update(st0)
            if "jobnum" not in st:
                st["jobnum"] =  "%i"%(rnmin+n+i0)
            rname = st["run_name"]%st
            st["maxtime"] = self.maxtime - 120;
            #print(st)
            macrodat = open(self.template,"r").read()%st
            open(os.path.expanduser("%s/%s.mac"%(self.macro_dir,rname)),"w").write(macrodat)

        # make job command and launch
        jcmd = "%s %s/%s.mac > /dev/null"%(self.bin_name, self.macro_dir, self.settings["run_name"])
        lcmd = "%s/%s.txt"%(self.log_dir, self.settings["run_name"])
        self.submitter.run_jobs(jcmd,lcmd,rnmin,nruns+rnmin)

    def launch_sims(self, nruns, rnmin=0):
        """Default launching for runs identical besides run number"""
        self.set_dirs()
        i0 = self.submitter.start_index()
        jobsettings = []
        for rn in range(rnmin, nruns):
            st = {"rnum": rn+i0, "jobnum": "%i"%(rn+i0)}
            rname = self.settings["run_name"]%st
            st["outfile"] = "%s/%s.root"%(self.settings["outdir"], rname)
            jobsettings.append(st)
        self.build_and_launch_macros(jobsettings, rnmin)



