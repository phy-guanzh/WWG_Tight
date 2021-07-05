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

        self.out.branch("event",  "F")
        self.out.branch("run",  "F")
        self.out.branch("lumi",  "F")
	self.out.branch("channel",  "I");
        self.out.branch("pass_selection1",  "B")
        self.out.branch("pass_selection2",  "B")
        self.out.branch("photon_selection",  "I")
        self.out.branch("njets_fake",  "I")
        self.out.branch("njets_fake_template",  "I")

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
        self.out.branch("n_photon", "I")
        self.out.branch("photonet",  "F")
        self.out.branch("photoneta",  "F")
        self.out.branch("photonphi",  "F")
	self.out.branch("photonchiso",  "F")
	self.out.branch("photonsieie",  "F")
        self.out.branch("photon_isprompt", "I")
        self.out.branch("photon_gen_matching", "I")
        self.out.branch("photonet_f",  "F")
        self.out.branch("photoneta_f",  "F")
        self.out.branch("photonphi_f",  "F")
	self.out.branch("photonchiso_f",  "F")
	self.out.branch("photonsieie_f",  "F")
        self.out.branch("photon_isprompt_f", "I")
        self.out.branch("photon_gen_matching_f", "I")
        self.out.branch("mll",  "F")
        self.out.branch("ptll",  "F")
        self.out.branch("mt",  "F")
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
        self.out.branch("n_bjets","I")
        self.out.branch("njets","I")
        self.out.branch("njets50","I")
        self.out.branch("njets40","I")
        self.out.branch("njets30","I")
        self.out.branch("njets20","I")
        self.out.branch("njets15","I")

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

        pass_selection1 = False
        pass_selection2 = False

        muons = Collection(event, "Muon")
	electrons = Collection(event, "Electron")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")
	if hasattr(event, 'nGenPart'):
           genparts = Collection(event, "GenPart")

        jet_select = [] 
        dileptonp4 = ROOT.TLorentzVector()
        selected_medium_or_control_photons = []
        selected_fake_template_photons = []
        electrons_select = []
        muons_select = [] 
        jets_select = []
        leptons_select=[]

        #selection on muons
        muon_pass =0
	loose_muon_pass=0
        for i in range(0,len(muons)):
            if muons[i].pt < 20:
                continue
            if abs(muons[i].eta) > 2.4:
                continue
            if muons[i].tightId == True and muons[i].pfRelIso04_all < 0.15:
                muons_select.append(i)
                muon_pass += 1
                leptons_select.append(i)
            if muons[i].looseId == True and muons[i].pfRelIso04_all < 0.25:
                loose_muon_pass += 1

        # selection on electrons
        electron_pass=0
        loose_electron_pass=0
        for i in range(0,len(electrons)):
            if electrons[i].pt < 20:
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

#        print 'the number of leptons: ',len(electrons_select)+len(muons_select)
        if len(electrons_select)+len(muons_select) != 2:      #reject event if there are not exactly two leptons
	   return False

        self.out.fillBranch("n_loose_ele", loose_electron_pass)
        self.out.fillBranch("n_loose_mu", loose_muon_pass)

        # select medium photons
	photon_pass=0
        for i in range(0,len(photons)):
            if photons[i].pt < 20:
                continue
            if abs(photons[i].eta) > 2.5:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue

            #| pt | scEta | H over EM | sigma ieie | Isoch | IsoNeu | Isopho |
            mask1 = 0b10101010101010 # full medium ID
            mask2 = 0b00101010101010 # fail Isopho
            mask3 = 0b10001010101010 # fail IsoNeu
            mask4 = 0b10100010101010 # fail Isoch
            mask5 = 0b10101000101010 # fail sigma ieie

            bitmap = photons[i].vidNestedWPBitmap & mask1

            #the photon pass the full ID
            if not (bitmap == mask1):
                continue

            #this is redundant after the if statement above
            if not((bitmap == mask1) or (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4) or (bitmap == mask5)):
                continue

            pass_lepton_dr_cut = True
            for j in range(0,len(muons_select)):
                if deltaR(muons[muons_select[j]].eta,muons[muons_select[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(electrons_select)):
                if deltaR(electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            selected_medium_or_control_photons.append(i)  #append the medium photons passing full ID

        # select control photons
        for i in range(0,len(photons)):
            if photons[i].pt < 20:
                continue
            if abs(photons[i].eta) > 2.5:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue

            #| pt | scEta | H over EM | sigma ieie | Isoch | IsoNeu | Isopho |
            mask1 = 0b10101010101010 # full medium ID
            mask2 = 0b00101010101010 # fail Isopho
            mask3 = 0b10001010101010 # fail IsoNeu
            mask4 = 0b10100010101010 # fail Isoch
            mask5 = 0b10101000101010 # fail sigma ieie

            bitmap = photons[i].vidNestedWPBitmap & mask1

            #not pass the full ID
            if (bitmap == mask1):
                continue

            #fail one of varaible in the ID
            if not ((bitmap == mask1) or (bitmap == mask2) or (bitmap == mask3) or (bitmap == mask4) or (bitmap == mask5)):
                continue

            pass_lepton_dr_cut = True
            for j in range(0,len(muons_select)):
                if deltaR(muons[muons_select[j]].eta,muons[muons_select[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(electrons_select)):
                if deltaR(electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            photon_pass += 1
            selected_medium_or_control_photons.append(i)  # append the control photons

        self.out.fillBranch("n_photon",photon_pass)

        # select fake photons
	fakephoton_pass=0
        for i in range(0,len(photons)):
            if photons[i].pt < 20:
                continue
            if abs(photons[i].eta) > 2.5:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
                continue

            #| pt | scEta | H over EM | sigma ieie | Isoch | IsoNeu | Isopho |
            mask1 = 0b10101010101010 # full medium ID
            mask4 = 0b10100010101010 # fail Isoch and pass sigma ieie
            mask6 = 0b10100000101010 # fail both Isoch and sigma ieie

            bitmap = photons[i].vidNestedWPBitmap & mask1

            # (Isoch and pass sigma ieie) + (fail both Isoch and sigma ieie) = fail Isoch and float sigma ieie
            if not ( (bitmap == mask4) or (bitmap == mask6) ):
                continue
             
            pass_lepton_dr_cut = True
            for j in range(0,len(muons_select)):
                if deltaR(muons[muons_select[j]].eta,muons[muons_select[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            for j in range(0,len(electrons_select)):
                if deltaR(electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi,photons[i].eta,photons[i].phi) < 0.5:
                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            fakephoton_pass += 1
            selected_fake_template_photons.append(i) #for fake template from data

        pass_selection1 = len(selected_medium_or_control_photons) >= 1 # select medium and control photons
        pass_selection2 = len(selected_fake_template_photons) == 1     # select fake photons
        if not pass_selection1 and not pass_selection2:
            return False

        isprompt_mask = (1 << 0) #isPrompt
        isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct
        isprompttaudecayproduct = (1 << 3) #isPromptTauDecayProduct
        isfromhardprocess_mask = (1 << 8) #isPrompt

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
            # lepton photon dr have requied when append photon
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

            if len(selected_medium_or_control_photons) >= 1:
                for j in range(0,len(selected_medium_or_control_photons)):
                    if abs((electrons[electrons_select[0]].p4() + photons[selected_medium_or_control_photons[j]].p4()).M() - 91.2) >= 10:
                       pass_selection1 = True
                       break

            if len(selected_fake_template_photons) == 1:
                if abs((electrons[electrons_select[0]].p4() + photons[selected_fake_template_photons[0]].p4()).M() - 91.2) >= 10:
                    pass_selection2 = True

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
            mT = sqrt(2*(muons[muons_select[0]].p4() + electrons[electrons_select[0]].p4()).Pt()*event.MET_pt*(1 - cos((muons[muons_select[0]].p4()+electrons[electrons_select[0]].p4()).Phi()-event.MET_phi)))
            self.out.fillBranch("mt",mT)
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
            if len(selected_medium_or_control_photons) >= 1:
                for j in range(0,len(selected_medium_or_control_photons)):
                    if (abs((electrons[electrons_select[0]].p4() + photons[selected_medium_or_control_photons[j]].p4()).M() - 91.2) >= 10) and (abs((electrons[electrons_select[1]].p4() + photons[selected_medium_or_control_photons[j]].p4()).M() - 91.2) >= 10):
                         pass_selection1 = True
                         break

            if len(selected_fake_template_photons) == 1:
                if (abs((electrons[electrons_select[0]].p4() + photons[selected_fake_template_photons[0]].p4()).M() - 91.2) >= 10) and (abs((electrons[electrons_select[1]].p4() + photons[selected_fake_template_photons[0]].p4()).M() - 91.2) >= 10):
                    pass_selection2 = True

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
            mT = sqrt(2*(electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()).Pt()*event.MET_pt*(1 - cos((electrons[electrons_select[0]].p4()+electrons[electrons_select[1]].p4()).Phi()-event.MET_phi)))
            self.out.fillBranch("mt",mT)

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
            mT = sqrt(2*(muons[muons_select[0]].p4() + muons[muons_select[1]].p4()).Pt()*event.MET_pt*(1 - cos((muons[muons_select[0]].p4()+muons[muons_select[1]].p4()).Phi()-event.MET_phi)))
            self.out.fillBranch("mt",mT)

        else:
            return False

        njets = 0
        njets50 = 0
        njets40 = 0
        njets30 = 0
        njets20 = 0
        njets15 = 0
        n_bjets = 0
        njets_fake_template = 0
        njets_fake = 0
        pass_lepton_dr_cut = True
        for i in range(0,len(jets)):
            if jets[i].btagDeepB > 0.4184:  # DeepCSVM
               n_bjets+=1
            if abs(jets[i].eta) > 4.7:
               continue
            if jets[i].pt<10:
               continue
            for j in range(0,len(electrons_select)):
                if deltaR(jets[i].eta,jets[i].phi,electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi) < 0.5:
                   pass_lepton_dr_cut = False
            for j in range(0,len(muons_select)):
                if deltaR(jets[i].eta,jets[i].phi,muons[muons_select[j]].eta,muons[muons_select[j]].phi) < 0.5:
                   pass_lepton_dr_cut = False

            if  not pass_lepton_dr_cut == True:
	        continue
            if jets[i].jetId >> 1 & 1:
               jets_select.append(i)
               njets += 1
               if jets[i].pt > 50:
                   njets50+=1
               if jets[i].pt > 40:
                   njets40+=1
               if jets[i].pt > 30:
                   njets30+=1
               if jets[i].pt > 20:
                   njets20+=1
               if jets[i].pt > 15:
                   njets15+=1
            if len(selected_medium_or_control_photons) >= 1:
               for j in range(0,len(selected_medium_or_control_photons)):
                   if deltaR(photons[selected_medium_or_control_photons[j]].eta,photons[selected_medium_or_control_photons[j]].phi,jets[i].eta,jets[i].phi) > 0.5:
                    njets_fake+=1

            if len(selected_fake_template_photons) == 1:
                if deltaR(photons[selected_fake_template_photons[0]].eta,photons[selected_fake_template_photons[0]].phi,jets[i].eta,jets[i].phi) > 0.5:
                    njets_fake_template+=1
#        print len(jets),("njets",njets)
#        if njets >=2 :
#            return True
        self.out.fillBranch("pass_selection1",pass_selection1) # select medium and control photons
        self.out.fillBranch("pass_selection2",pass_selection2) # select fake photons

        if pass_selection1:
           photon_gen_matching=-10
           photon_isprompt =-10
           for j in range(0,len(selected_medium_or_control_photons)):
               if  channel==1 and deltaR(photons[selected_medium_or_control_photons[j]].eta,photons[selected_medium_or_control_photons[j]].phi,electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi) > 0.5 and deltaR(photons[selected_medium_or_control_photons[j]].eta,photons[selected_medium_or_control_photons[j]].phi,muons[muons_select[0]].eta,muons[muons_select[0]].phi) > 0.5:
                  photon_index=selected_medium_or_control_photons[j]
                  break
               elif channel==2 and deltaR(photons[selected_medium_or_control_photons[j]].eta,photons[selected_medium_or_control_photons[j]].phi,electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi) > 0.5 and deltaR(photons[selected_medium_or_control_photons[j]].eta,photons[selected_medium_or_control_photons[j]].phi,electrons[electrons_select[1]].eta,electrons[electrons_select[1]].phi) > 0.5:
                  photon_index=selected_medium_or_control_photons[j]
                  break
               elif channel ==3 and deltaR(photons[selected_medium_or_control_photons[j]].eta,photons[selected_medium_or_control_photons[j]].phi,muons[muons_select[0]].eta,muons[muons_select[0]].phi) > 0.5 and deltaR(photons[selected_medium_or_control_photons[j]].eta,photons[selected_medium_or_control_photons[j]].phi,muons[muons_select[1]].eta,muons[muons_select[1]].phi) > 0.5:
                  photon_index=selected_medium_or_control_photons[j]
                  break
               else:
                  photon_index=selected_medium_or_control_photons[0]
           if hasattr(photons[photon_index],'genPartIdx') :
               if photons[photon_index].genPartIdx >= 0 and genparts[photons[photon_index].genPartIdx].pdgId  == 22: 
                   if ((genparts[photons[photon_index].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[photon_index].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and (genparts[photons[photon_index].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask):
                       photon_gen_matching = 6
                   elif ((genparts[photons[photon_index].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[photon_index].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):       
                       if (genparts[photons[photon_index].genPartIdx].genPartIdxMother >= 0 and (abs(genparts[genparts[photons[photon_index].genPartIdx].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[photons[photon_index].genPartIdx].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[photons[photon_index].genPartIdx].genPartIdxMother].pdgId) == 15)):
                           photon_gen_matching = 4
                       else:    
                           photon_gen_matching = 5
                   else:
                       photon_gen_matching = 3
               elif photons[photon_index].genPartIdx >= 0 and abs(genparts[photons[photon_index].genPartIdx].pdgId) == 11:     
                   if ((genparts[photons[photon_index].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[photon_index].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):  
                       photon_gen_matching = 1
                   else:
                       photon_gen_matching = 2
                       
               else:
                   assert(photons[photon_index].genPartFlav == 0)
                   photon_gen_matching = 0
           if hasattr(event, 'nGenPart') :
               for j, genpart in enumerate(genparts):
	           if photons[photon_index].genPartIdx >=0 and genpart.pt > 5 and abs(genpart.pdgId) == 22 and ((genparts[photons[photon_index].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[photon_index].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask) or (genparts[photons[photon_index].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask)) and deltaR(photons[photon_index].eta,photons[photon_index].phi,genpart.eta,genpart.phi) < 0.3:
                      photon_isprompt =1
                      break
           mask1 = 0b10101010101010 # full medium ID
           mask2 = 0b00101010101010 # fail Isopho
           mask3 = 0b10001010101010 # fail IsoNeu
           mask4 = 0b10100010101010 # fail Isoch
           mask5 = 0b10101000101010 # fail sigma ieie
        
	   bitmap = photons[photon_index].vidNestedWPBitmap & mask1   
           if (bitmap == mask1):
               self.out.fillBranch("photon_selection",1) #all cuts applied
           elif (bitmap == mask2):
               self.out.fillBranch("photon_selection",2) # fail Isopho
           elif (bitmap == mask3):
               self.out.fillBranch("photon_selection",3) # fail IsoNeu
           elif (bitmap == mask4):
               self.out.fillBranch("photon_selection",4) # fail Isoch
           elif (bitmap == mask5):
               self.out.fillBranch("photon_selection",5) # fail sigma ieie
           #pass_selection1 && (photon_selection==1 || photon_selection==5) -> remove the sieie requirement in the full ID that can build data/true template
           #pass_selection1 && (photon_selection==2 || photon_selection==3 || photon_selection==4 || photon_selection ==5 )->build fake photon enriched sample
           else:
               assert(0)
           self.out.fillBranch("photonet",photons[photon_index].pt)
           self.out.fillBranch("photoneta",photons[photon_index].eta)
           self.out.fillBranch("photonphi",photons[photon_index].phi)
           self.out.fillBranch("photonchiso",photons[photon_index].pfRelIso03_chg*photons[photon_index].pt)
           self.out.fillBranch("photonsieie",photons[photon_index].sieie)
           self.out.fillBranch("photon_gen_matching",photon_gen_matching)
           self.out.fillBranch("photon_isprompt",photon_isprompt)

        if pass_selection2: # pass_selection1 and pass_selection1 can appear meantime
           photon_gen_matching=-10
           photon_isprompt =-10
           if hasattr(photons[selected_fake_template_photons[0]],'genPartIdx') :
               if photons[selected_fake_template_photons[0]].genPartIdx >= 0 and genparts[photons[selected_fake_template_photons[0]].genPartIdx].pdgId  == 22: 
                   if ((genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask):
                       photon_gen_matching = 6
                   elif ((genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):       
                       if (genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother >= 0 and (abs(genparts[genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 11 or abs(genparts[genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 13 or abs(genparts[genparts[photons[selected_fake_template_photons[0]].genPartIdx].genPartIdxMother].pdgId) == 15)):
                           photon_gen_matching = 4
                       else:    
                           photon_gen_matching = 5
                   else:
                       photon_gen_matching = 3
               elif photons[selected_fake_template_photons[0]].genPartIdx >= 0 and abs(genparts[photons[selected_fake_template_photons[0]].genPartIdx].pdgId) == 11:     
                   if ((genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)):  
                       photon_gen_matching = 1
                   else:
                       photon_gen_matching = 2
                       
               else:
                   assert(photons[selected_fake_template_photons[0]].genPartFlav == 0)
                   photon_gen_matching = 0
           if hasattr(event, 'nGenPart') :
               for j, genpart in enumerate(genparts):
	           if photons[selected_fake_template_photons[0]].genPartIdx >=0 and genpart.pt > 5 and abs(genpart.pdgId) == 22 and ((genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask) or (genparts[photons[selected_fake_template_photons[0]].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask)) and deltaR(photons[selected_fake_template_photons[0]].eta,photons[selected_fake_template_photons[0]].phi,genpart.eta,genpart.phi) < 0.3:
                      photon_isprompt =1
                      break
           self.out.fillBranch("photonet_f",photons[selected_fake_template_photons[0]].pt)
           self.out.fillBranch("photoneta_f",photons[selected_fake_template_photons[0]].eta)
           self.out.fillBranch("photonphi_f",photons[selected_fake_template_photons[0]].phi)
           self.out.fillBranch("photonchiso_f",photons[selected_fake_template_photons[0]].pfRelIso03_chg*photons[selected_fake_template_photons[0]].pt)
           self.out.fillBranch("photonsieie_f",photons[selected_fake_template_photons[0]].sieie)
           self.out.fillBranch("photon_gen_matching_f",photon_gen_matching)
           self.out.fillBranch("photon_isprompt_f",photon_isprompt)
           #pass_selection2  && low<photonchiso_f<high -> build fake template from data

        if hasattr(event,'Pileup_nPU'):    
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)
    
        if hasattr(event,'Pileup_nTrueInt'):    
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu",0)

        print 'channel', channel,'mu_pass:',muon_pass,' ele_pass:',electron_pass,' photon_pass:',photon_pass,' is lepton1 real ',lepton1_isprompt,' is lepton2 real ',lepton2_isprompt,' is photon real ',photon_isprompt,' or ',photon_gen_matching

        self.out.fillBranch("njets50",njets50)
        self.out.fillBranch("njets40",njets40)
        self.out.fillBranch("njets30",njets30)
        self.out.fillBranch("njets20",njets20)
        self.out.fillBranch("njets15",njets15)
        self.out.fillBranch("n_bjets",n_bjets)
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("metup",sqrt(pow(event.MET_pt*cos(event.MET_phi) + event.MET_MetUnclustEnUpDeltaX,2) + pow(event.MET_pt*sin(event.MET_phi) + event.MET_MetUnclustEnUpDeltaY,2)))
        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("puppimetphi",event.PuppiMET_phi)
        self.out.fillBranch("rawmet",event.RawMET_pt)
        self.out.fillBranch("rawmetphi",event.RawMET_phi)
        self.out.fillBranch("metphi",event.MET_phi)
        self.out.fillBranch("njets_fake", njets_fake)
        self.out.fillBranch("njets_fake_template", njets_fake)
        return True

WWGfakephoton_Module = lambda: WWG_Producer()

