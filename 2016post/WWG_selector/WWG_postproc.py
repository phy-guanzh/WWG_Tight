#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from WWG_Module import *

import argparse
import re
import optparse

parser = argparse.ArgumentParser(description='baseline selection')
parser.add_argument('-f', dest='infile', default='', help='local file input')
parser.add_argument('-y', dest='year', default='2016', help='year of dataset')
parser.add_argument('-m', dest='mode', default='local', help='runmode local/condor')
parser.add_argument('-d', dest='isdata',action='store_true',default=False)
parser.add_argument('-e', dest='era',default='B')
args = parser.parse_args()

print "mode: ", args.mode
print "year: ", args.year
print "dataset_name: ", args.infile
print "data_era", args.era

from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *

# classify input files
if args.infile:
    infilelist = [args.infile]
    jsoninput = None
    fwkjobreport = False

    if args.mode == 'condor':
        infilelist.append(search.getValidSite(args.file)+args.file) 
    else:
        infilelist = [args.infile]
else:
    from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
    infilelist = inputFiles()
    jsoninput = runsAndLumis()
    fwkjobreport = True

if args.isdata:
       Modules = [countHistogramsModule(),jmeCorrections_ak4_Data(),WWG_Module()]
else:
       if args.year=='2016':
          Modules = [countHistogramsModule(),WWG_Module(),puWeight_UL2016()]
       if args.year=='2017':
          Modules = [countHistogramsModule(),WWG_Module(),puWeight_UL2017()]
       if args.year=='2018':
          Modules = [countHistogramsModule(),WWG_Module(),puWeight_UL2018()]

p=PostProcessor(".",infilelist,
                branchsel="WWG_keep_and_drop.txt",
                modules = Modules,
                provenance=True,
                justcount=False,
                noOut=False,
                fwkJobReport=fwkjobreport, 
                jsonInput=jsoninput, 
                outputbranchsel = "WWG_output_branch.txt")
p.run()



