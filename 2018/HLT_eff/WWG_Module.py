#!/usr/bin/env python
# Analyzer for WWG Analysis based on nanoAOD tools

import os, sys
import math
import ROOT
from math import sin, cos, sqrt
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer

class WWG_Producer(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        self.out = wrappedOutputTree

        self.out.branch("event",  "i")
        self.out.branch("run",  "i")
        self.out.branch("lumi",  "i")
	self.out.branch("pass_selection",  "B");
	self.out.branch("channel",  "I");

        self.out.branch("lep1_pid",  "I")
        self.out.branch("lep2_pid",  "I")
        self.out.branch("lep1pt",  "F")
        self.out.branch("lep2pt",  "F")
        self.out.branch("lep1eta",  "F")
        self.out.branch("lep2eta",  "F")
        self.out.branch("lep1phi",  "F")
        self.out.branch("lep2phi",  "F")
        self.out.branch("lepton1_isprompt", "I")
        self.out.branch("lepton2_isprompt", "I")
        self.out.branch("n_loose_mu", "I")
        self.out.branch("n_loose_ele", "I")
        self.out.branch("mll",  "F")
        self.out.branch("ptll",  "F")
        self.out.branch("met",  "F")
        self.out.branch("metup",  "F")
        self.out.branch("puppimet","F")
        self.out.branch("puppimetphi","F")
        self.out.branch("rawmet","F")
        self.out.branch("rawmetphi","F")
        self.out.branch("metphi","F")
        self.out.branch("gen_weight","F")
        self.out.branch("npu",  "I");
        self.out.branch("ntruepu",  "F");
        self.out.branch("n_pos", "I")
        self.out.branch("n_minus", "I")
        self.out.branch("n_num", "I")
        self.out.branch("MET_pass","I")
        self.out.branch("npvs","I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
	pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)
#        print event.event,event.luminosityBlock,event.run
        if hasattr(event,'Generator_weight'):
            if event.Generator_weight > 0 :
                n_pos=1
                n_minus=0
            else:
                n_minus=1
                n_pos=0
            self.out.fillBranch("gen_weight",event.Generator_weight)
            self.out.fillBranch("n_pos",n_pos)
            self.out.fillBranch("n_minus",n_minus)
        else:    
            self.out.fillBranch("gen_weight",0)
            self.out.fillBranch("n_pos",0)
            self.out.fillBranch("n_minus",0)

        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")
	if hasattr(event, 'nGenPart'):
           genparts = Collection(event, "GenPart")

        jet_select = [] 
        dileptonp4 = ROOT.TLorentzVector()
        photons_select = []
        electrons_select = []
        muons_select = [] 
        jets_select = []
        leptons_select=[]

        #selection on muons
        muon_pass =0
	loose_muon_pass=0
        for i in range(0,len(muons)):
            if muons[i].pt < 10:
                continue
            if abs(muons[i].eta) > 2.5:
                continue
            if muons[i].pfRelIso04_all > 0.20:
                continue   
            if muons[i].mediumId == True:
                muons_select.append(i)
                muon_pass += 1
                leptons_select.append(i)
            if muons[i].looseId == True:
                loose_muon_pass += 1

        # selection on electrons
        electron_pass=0
        loose_electron_pass=0
        for i in range(0,len(electrons)):
            if electrons[i].pt < 10:
                continue
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) > 2.5:
                continue
            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    electrons_select.append(i)
                    electron_pass += 1
                    leptons_select.append(i)

                if electrons[i].cutBased >= 1:
                    loose_electron_pass += 1

#       print 'the number of leptons: ',len(electrons_select)+len(muons_select)
        if len(electrons_select)+len(muons_select) != 2:      #reject event if there are not exactly two leptons
	   return False
        self.out.fillBranch("n_loose_ele", loose_electron_pass)
        self.out.fillBranch("n_loose_mu", loose_muon_pass)

        channel = 0 
        # emu:     1
        # ee:      2
        # mumu:    3

        # emu
        mll = -10
        ptll = -10
        lepton1_isprompt=-10
        lepton2_isprompt=-10
        if len(muons_select)==1 and len(electrons_select)==1:  # emu channel 
            if deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi) < 0.5:
               return False 
            if muons[muons_select[0]].charge * (electrons[electrons_select[0]].charge) >= 0:
                return False
#           print 'test emu channel',len(genparts)
            if hasattr(event, 'nGenPart'):
                print 'calculate the lepton flag in channel emu'
                for i in range(0,len(genparts)):
		   if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                       lepton1_isprompt=1
                       break 
                for i in range(0,len(genparts)):
		   if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                       lepton2_isprompt=1 
                       break 
            channel = 1
            self.out.fillBranch("channel",channel)
	    self.out.fillBranch("lepton1_isprompt",lepton1_isprompt)
	    self.out.fillBranch("lepton2_isprompt",lepton2_isprompt)
            self.out.fillBranch("lep1_pid",13)
            self.out.fillBranch("lep2_pid",11)
            self.out.fillBranch("lep1pt",muons[muons_select[0]].pt)
            self.out.fillBranch("lep1eta",muons[muons_select[0]].eta)
            self.out.fillBranch("lep1phi",muons[muons_select[0]].phi)
            self.out.fillBranch("lep2pt",electrons[electrons_select[0]].pt)
            self.out.fillBranch("lep2eta",electrons[electrons_select[0]].eta)
            self.out.fillBranch("lep2phi",electrons[electrons_select[0]].phi)
            self.out.fillBranch("mll",(muons[muons_select[0]].p4() + electrons[electrons_select[0]].p4()).M())
            self.out.fillBranch("ptll",(muons[muons_select[0]].p4() + electrons[electrons_select[0]].p4()).Pt())
        # ee
        elif len(muons_select)==0 and len(electrons_select)==2:
            if deltaR(electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi,electrons[electrons_select[1]].eta,electrons[electrons_select[1]].phi)<0.5:
               return False 
            if electrons[electrons_select[0]].charge * electrons[electrons_select[1]].charge >=0:
	       return False 
#           print 'test',len(genparts)
	    if hasattr(event, 'nGenPart'):
                print 'calculate the lepton flag in channel ee'
                for i in range(0,len(genparts)):
		   if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                       lepton1_isprompt=1 
                       break 
                for i in range(0,len(genparts)):
		   if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(electrons[electrons_select[1]].eta,electrons[electrons_select[1]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                       lepton2_isprompt=1 
                       break 
            channel = 2
            self.out.fillBranch("channel",channel)
	    self.out.fillBranch("lepton1_isprompt",lepton1_isprompt)
	    self.out.fillBranch("lepton2_isprompt",lepton2_isprompt)
            self.out.fillBranch("lep1_pid",11)
            self.out.fillBranch("lep2_pid",11)
            self.out.fillBranch("lep1pt",electrons[electrons_select[0]].pt)
            self.out.fillBranch("lep1eta",electrons[electrons_select[0]].eta)
            self.out.fillBranch("lep1phi",electrons[electrons_select[0]].phi)
            self.out.fillBranch("lep2pt",electrons[electrons_select[1]].pt)
            self.out.fillBranch("lep2eta",electrons[electrons_select[1]].eta)
            self.out.fillBranch("lep2phi",electrons[electrons_select[1]].phi)
            self.out.fillBranch("mll",(electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()).M())
            self.out.fillBranch("ptll",(electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()).Pt())

        # mumu 
        elif len(electrons_select)==0 and len(muons_select)==2:
            if deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,muons[muons_select[1]].eta,muons[muons_select[1]].phi)<0.5:
               return False 
            if muons[muons_select[0]].charge * muons[muons_select[1]].charge >= 0:
               return False 
	    if hasattr(event, 'nGenPart'):
                print 'calculate the lepton flag in channel mumu'
                for i in range(0,len(genparts)):
		   if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                       lepton1_isprompt=1
                       break 
                for i in range(0,len(genparts)):
		   if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)) and deltaR(muons[muons_select[1]].eta,muons[muons_select[1]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                       lepton2_isprompt=1
                       break 
            channel = 3
            self.out.fillBranch("channel",channel)
	    self.out.fillBranch("lepton1_isprompt",lepton1_isprompt)
	    self.out.fillBranch("lepton2_isprompt",lepton2_isprompt)
            self.out.fillBranch("lep1_pid",13)
            self.out.fillBranch("lep2_pid",13)
            self.out.fillBranch("lep1pt",muons[muons_select[0]].pt)
            self.out.fillBranch("lep1eta",muons[muons_select[0]].eta)
            self.out.fillBranch("lep1phi",muons[muons_select[0]].phi)
            self.out.fillBranch("lep2pt",muons[muons_select[1]].pt)
            self.out.fillBranch("lep2eta",muons[muons_select[1]].eta)
            self.out.fillBranch("lep2phi",muons[muons_select[1]].phi)
            self.out.fillBranch("mll",(muons[muons_select[0]].p4() + muons[muons_select[1]].p4()).M())
            self.out.fillBranch("ptll",(muons[muons_select[0]].p4() + muons[muons_select[1]].p4()).Pt())
        else:
            return False

        if hasattr(event,'Pileup_nPU'):    
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)
    
        if hasattr(event,'Pileup_nTrueInt'):    
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu",0)

        print 'channel', channel,'mu_pass:',muon_pass,' ele_pass:',electron_pass,' is lepton1 real ',lepton1_isprompt,' is lepton2 real ',lepton2_isprompt
        print '------\n'

        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("metup",sqrt(pow(event.MET_pt*cos(event.MET_phi) + event.MET_MetUnclustEnUpDeltaX,2) + pow(event.MET_pt*sin(event.MET_phi) + event.MET_MetUnclustEnUpDeltaY,2)))
        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("puppimetphi",event.PuppiMET_phi)
        self.out.fillBranch("rawmet",event.RawMET_pt)
        self.out.fillBranch("rawmetphi",event.RawMET_phi)
        self.out.fillBranch("metphi",event.MET_phi)
        return True

WWG_Module = lambda: WWG_Producer()

