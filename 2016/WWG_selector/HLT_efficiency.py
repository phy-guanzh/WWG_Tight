#!/usr/bin/env python
# Analyzer for WWG Analysis based on nanoAOD tools

import os, sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer
import yaml
import argparse
#from pathlib import Path

file_list = '~/new/wwgamma_5f_NLO_com_1310185_101.root'
df=ROOT.RDataFrame("Events",file_list)
column_list=df.GetColumnNames()
branchList = []

for i in range(0,len(column_list)):
    branchList.append(column_list[i])
#print branchList
x='HLT'
point='.'
filtered_list = []
for elem in  branchList :
    if x in elem and point not in elem:
        filtered_list.append(elem)
print(filtered_list)

N_init=0
N_pass = 0
N_rej = 0

class WWG_HLT(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("event",  "i")
        self.out.branch("HLT",  "F")
    

  
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

	# Record the pass numbers for each cut. Noticed that for efficiency, those who can't pass the MET cut may not be counted because it will pass to next event directly.
        global N_init
        global N_pass
        global N_rej
        global filtered_list
        global HLT_tmp
        HLT_local = HLT_tmp

    #if event.Generator_weight > 0 :
    #    n_posi +=1
    #else:
    #    n_minus +=1
        N_init +=1
        if eval('event.'+HLT_local):
            N_pass+=1
        else:
            N_rej+=1  

        return True

files = ['~/new/wwgamma_5f_NLO_com_1310185_101.root']
with open ("HLT_eff_"+"WWA"+".log","w+") as f:
    for k in filtered_list:
        HLT_tmp = k
        N_init=0
        N_pass = 0
        N_rej = 0

        p=PostProcessor(".",files,branchsel="WWG_input_branch.txt",modules=[WWG_HLT()],provenance=True,outputbranchsel="WWG_output_branch.txt1")
        p.run()
        if N_pass >0: print HLT_tmp,"N_pass",N_pass,"N_reject",N_rej,"N_init",N_init
        eff= float(N_pass)/float(N_init) 
        f.write(HLT_tmp+"_eff"+"\t"+"="+"\t"+str(eff)+"\n")
    f.close()
    
