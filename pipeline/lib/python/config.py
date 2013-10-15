import os, subprocess

# Name of institution where pipeline is being run
institution = "McGill"
# Name of HPC machine where pipeline is being run
machine     = "guillimin"
# Timezone of processing site
timezone    = "Canada/Eastern"
# User name on 'machine'
user        = "rlynch"
# Email address where job notifications will be sent (if enabled)
email       = "rlynch+gbncc_jobs@physics.mcgill.ca"
# Walltime limit (hh:mm:ss)
walltimelim = "285:00:00"
# Maximum size of the 'pending' job queue
queuelim    = 2
# Time to wait between submitting a new job when there are no new files or the
# 'pending' queue is full
sleeptime   = 5*60
# Top level analysis directory
topdir      = "/homes/borgii/rlynch/GBNCC/GBNCC/"
# Base working directory for data reduction (should have at least 13 GB free)
baseworkdir = os.path.join(topdir, "work")
# Base temporary directory for data reduction (should have at least 2 GB free)
basetmpdir  = os.path.join(topdir, "scratch")
# Directory where pipeline scripts are stored
pipelinedir = os.path.join(topdir, "pipeline")
# Directory where raw data files are stored before being processed
datadir     = os.path.join(topdir, "data")
# Directory where job submission files are stored
jobsdir     = os.path.join(topdir, "jobs")
# Directory wehre log files are stored
logsdir     = os.path.join(topdir, "logs")
# Directory where output files are permanently stored
baseoutdir  = os.path.join(topdir, "results")
# Location of FFT zaplist
zaplist     = os.path.join(pipelinedir, "lib", "GBNCC.zaplist")
# Pipeline version (as the git hash)
#version     = subprocess.Popen("cd %s ; git rev-parse HEAD"%pipelinedir,shell=True,stdout=subprocess.PIPE).stdout.readline().strip()

# Dictionary for holding job submission scripts
subscripts = {"guillimin": 
"""#!/bin/bash
#PBS -S /bin/bash
#PBS -V
#PBS -N {jobnm}
#PBS -M {email}
#PBS -m ae
#PBS -q sw
#PBS -l nodes={nodenm}:ppn=1
#PBS -l walltime={walltimelim}

export PYTHONPATH=""
export LD_LIBRARY_PATH="/software/compilers/intel/composerxe-2011.4.191/compiler/lib/intel64:/software/compilers/intel/composerxe-2011.4.191/mkl/lib/intel64:/sb/software/libraries/MKL/10.3/lib/intel64:/software/libraries/PGPLOT/5.2:/sb/software/libraries/CFITSIO/3.28/lib:/sb/project/bgf-180-aa/src/presto_floats_mkl/lib:/sb/project/bgf-180-aa/lib:/sb/project/bgf-180-aa/lib64:/usr/local/lib:/usr/lib/"
export PATH={workdir}/python-2.6.8/lib64/python2.6/site-packages/ratings2:{workdir}/python-2.6.8/bin:$PATH


if [ {nodenm} == 1 ]
  then
    mkdir -p {workdir}
    mv {filenm} {workdir}
    cp {zaplist} {workdir}
    tar -C {workdir} -xzf {pipelinedir}/lib/python-2.6.8-packages_GBNCC.tgz
fi

search.py {basenm}.fits {workdir} {tmpdir}
rm -rf {workdir}
""",

"condor":
"""Executable={pipelinedir}/bin/search.py
Universe=vanilla
# New configuration
+Online_GBNCC = True
Requirements = TARGET.Online_GBNCC =?= True && Machine == "nemo-slave1081.nemo.phys.uwm.edu"
Arguments= -s {tmpdir} -w {workdir} -o {outdir} -i {basenm}.fits -z {zaplist}
getenv=True
Output={logsdir}/GBNCC.$(cluster).$(process).out
Error={logsdir}/GBNCC.$(cluster).$(process).err
Log={logsdir}/GBNCC.log
queue
"""
}

subscript = subscripts[machine]