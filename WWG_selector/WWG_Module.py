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

Np=0
Nm=0
test=0
MET_pass = 0
photon_pass = 0
electron_pass = 0
muon_pass = 0
none_lepton_reject = 0
none_2lepton_reject = 0
dilepton_pass = 0
emu_pass = 0
ee_pass = 0
mumu_pass = 0
btagjet_reject = 0
deltar_reject = 0
mll_reject = 0
pt_reject = 0
none_photon_reject = 0
different_charge_reject = 0
minus_mll=0
n_posi=0
n_minus=0
njet_reject = 0
n_num = 0



class WWG_Producer(Module):
    def __init__(self,isdata=False,kind='MC'):
        self.isdata = isdata
        self.kind = kind
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("event",  "i")
        self.out.branch("MET",  "F")
        self.out.branch("MET_emu",  "F")
        self.out.branch("MET_mumu",  "F")
        self.out.branch("MET_ee",  "F")
        self.out.branch("photon_pt",  "F")
        self.out.branch("photon_pt_emu",  "F")
        self.out.branch("photon_pt_ee",  "F")
        self.out.branch("photon_pt_mumu",  "F")
        self.out.branch("photon_eta",  "F")
        self.out.branch("photon_eta_ee",  "F")
        self.out.branch("photon_eta_emu",  "F")
        self.out.branch("photon_eta_mumu",  "F")
        self.out.branch("photon_phi",  "F")
        self.out.branch("photon_phi_ee",  "F")
        self.out.branch("photon_phi_emu",  "F")
        self.out.branch("photon_phi_mumu",  "F")

        self.out.branch("photon_sieie",  "F")
        self.out.branch("lepton1_pt_ee",  "F")
        self.out.branch("lepton2_pt_ee",  "F")
        self.out.branch("lepton1_pt_emu",  "F")
        self.out.branch("lepton2_pt_emu",  "F")
        self.out.branch("lepton1_pt_mumu",  "F")
        self.out.branch("lepton2_pt_mumu",  "F")


        self.out.branch("Njets",  "i")
        self.out.branch("Njets_emu",  "i")
        self.out.branch("Njets_mumu",  "i")
        self.out.branch("Njets_ee",  "i")
        

        self.out.branch("dilepton_mass_mumu",  "F")
        self.out.branch("dilepton_g_mass_mumu",  "F")
        self.out.branch("dilepton_pt_mumu",  "F")
        self.out.branch("dilepton_mass_emu",  "F")
        self.out.branch("dilepton_g_mass_emu",  "F")
        self.out.branch("dilepton_pt_emu",  "F")
        self.out.branch("dilepton_mass_ee",  "F")
        self.out.branch("dilepton_g_mass_ee",  "F")
        self.out.branch("dilepton_pt_ee",  "F")
        self.out.branch("dilepton_mass",  "F")
        self.out.branch("dilepton_g_mass",  "F")
        self.out.branch("dilepton_pt",  "F")
        self.out.branch("Generator_weight","F")
        self.out.branch("lepton_motherid_mumu",  "F")
        self.out.branch("lepton_motherid_emu",  "F")
        self.out.branch("electrons_is_real", "I")
        self.out.branch("muons_is_real", "I")
        self.out.branch("photons_is_real", "I")
        self.out.branch("lepton1_is_real_nano", "I")
        self.out.branch("lepton2_is_real_nano", "I")
        self.out.branch("photons_is_real_nano", "I")
        self.out.branch("n_posi", "I")
        self.out.branch("n_minus", "I")
        self.out.branch("n_num", "I")
        self.out.branch("emu_pass", "I")
        self.out.branch("ee_pass", "I")
        self.out.branch("mumu_pass", "I")

        self.out.branch("channel_mark","i")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out.fillBranch("n_posi", n_posi)
        self.out.fillBranch("n_minus", n_minus)
        self.out.fillBranch("n_num", n_num)
        self.out.fillBranch("emu_pass", emu_pass)
        self.out.fillBranch("ee_pass", ee_pass)
        self.out.fillBranch("mumu_pass", mumu_pass)


    def analyze(self, event):
	isdata=self.isdata
        kind=self.kind
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")

        jet_select = [] 
        dileptonp4 = ROOT.TLorentzVector()
        photons_select = []
        electrons_select = []
        muons_select = [] 
        jets_select = []
        leptons_select=[]
        if hasattr(event,'nGenPart'):
            genparts = Collection(event, "GenPart")

    # Record the pass numbers for each cut. Noticed that for efficiency, those who can't pass the MET cut may not be counted because it will pass to next event directly.
	        
        global MET_pass
        global photon_pass
        global electron_pass
        global muon_pass
        global none_lepton_reject
        global none_2lepton_reject
        global dilepton_pass
        global ee_pass 
        global emu_pass 
        global mumu_pass 
        global btagjet_reject
        global mll_reject
        global njet_reject
        global pt_reject
        global deltar_reject
        global test
        global none_photon_reject
        global different_charge_reject
        global minus_mll 
        global n_posi 
        global n_minus 
        # selection on MET. Pass to next event directly if fail.
        global n_num

        dileptonmass = -99
        dileptongmass=-99
        dileptonpt=-99
        njets=-99
        njets_ee = -99
        njets_emu = -99
        njets_mumu = -99
        dileptonmass_emu=-99
        dileptonpt_emu=-99
        met_emu=-99
        dileptonmass_ee=-99
        dileptonpt_ee=-99
        met_ee=-99
        dileptonmass_mumu=-99
        dileptonpt_mumu=-99
        met_mumu=-99
        n_num +=1
        pass_HLT_emu=-99
        pass_HLT_ee = -99
        pass_HLT_mumu = -99
        #if event.Generator_weight > 0 :
        #    n_posi +=1
        #else:
        #    n_minus +=1
        if hasattr(event, 'nGenPart'):
            if event.Generator_weight > 0 :
                n_posi +=1
            else:
                n_minus +=1

    #if event.Generator_weight > 0 :
    #    n_posi +=1
    #else:
    #    n_minus +=1
        #single HLT
        #if not ((event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) or (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)):
        #    return False
        #mixed HLT
        # check HLT
        pass_Ele23Ele12 = event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL
        pass_Ele23Ele12_DZ = event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ
        pass_Ele35 = event.HLT_Ele35_WPTight_Gsf
        pass_Ele32 = event.HLT_Ele32_WPTight_Gsf_L1DoubleEG

        pass_Mu17Mu8_3p8 = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8
        pass_Mu17Mu8 = event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8
        pass_Mu27 = event.HLT_IsoMu27

        pass_Mu12Ele23 = event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL
        pass_Mu23Ele12 = event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL
        pass_Ele35 = event.HLT_Ele35_WPTight_Gsf
        pass_Ele32 = event.HLT_Ele32_WPTight_Gsf_L1DoubleEG

        if (isdata):
            if (kind == 'EGamma'):
                if pass_Ele23Ele12 or pass_Ele23Ele12_DZ:
                    pass_HLT_ee = 1
                elif (not (pass_Ele23Ele12 or pass_Ele23Ele12_DZ)) and (pass_Ele35 or pass_Ele32):
                    pass_HLT_ee = 1
                elif (not (pass_Mu12Ele23 or pass_Mu23Ele12) and (pass_Ele35 or pass_Ele32)):
                    pass_HLT_emu = 1
            elif (kind == 'DoubleMuon'):
                if (pass_Mu17Mu8_3p8 or pass_Mu17Mu8):
                    pass_HLT_mumu = 1
            elif (kind == 'SingleMuon'):
                if (not (pass_Mu17Mu8_3p8 or pass_Mu17Mu8)) and (pass_Mu27):
                    pass_HLT_mumu = 1
                elif (not (pass_Mu12Ele23 or pass_Mu23Ele12) and (pass_Ele35 and pass_Ele32)):
                    pass_HLT_emu = 1
            elif (kind == 'MuonEG'):
                if (pass_Mu12Ele23 or pass_Mu23Ele12):
                    pass_HLT_emu = 1
            else:
                #print 'unkown dataset name for data or no proper channel'
                return False

        if (not isdata):
            if (kind == 'MC'):
                if (pass_Ele23Ele12 or pass_Ele23Ele12_DZ or pass_Ele35 or pass_Ele32):
                    pass_HLT_ee = 1
                elif (pass_Mu17Mu8_3p8 or pass_Mu17Mu8 or pass_Mu27):
                    pass_HLT_mumu = 1
                elif (pass_Mu12Ele23 or pass_Mu23Ele12 or pass_Ele35 or pass_Ele32):
                    pass_HLT_emu = 1
                else:
                #    print 'unkown dataset name for data or no proper channel'
                    return False

        if  event.MET_pt>20:
            MET_pass += 1
        else:
            return False

        #selection on muons
        for i in range(0,len(muons)):
            if muons[i].pt < 20:
                continue
            if abs(muons[i].eta) > 2.5:
                continue
            if muons[i].pfRelIso04_all > 0.25:
                continue   
            if muons[i].mediumId == True:
                muons_select.append(i)
                muon_pass += 1
                leptons_select.append(i)

        # selection on electrons
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

        if len(electrons_select)+len(muons_select) != 2:      #reject event if there are not exactly two leptons
            none_2lepton_reject += 1
            return False

        # selection on photons
        for i in range(0,len(photons)):
            #if not photons[i].electronVeto:
            #    continue
            if photons[i].pt < 20:
                continue
            if abs(photons[i].eta) > 2.5:
                continue
            if not (photons[i].isScEtaEE or photons[i].isScEtaEB):
                continue
            if photons[i].pixelSeed:
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
#            if photons[i].cutBasedBitmap >=1: #1==medium
            if photons[i].cutBased >=2:
                photons_select.append(i)
                photon_pass += 1

        if  len(photons_select)<1:
            none_photon_reject +=1 
            return False                        #reject event if there is not exact one photon in the event 


        njets = 0
        print len(jets)
        for i in range(0,len(jets)):
            btag_cut = False
            #if jets[i].btagCMVA > -0.5884:  # cMVAv2L
            # if jets[i].btagCMVA > 0.4432:  # cMVAv2M
            # if jets[i].btagCSVV2 > 0.5426:  # CSVv2L
            # if jets[i].btagCSVV2 > 0.8484:  # CSVv2M
            #if jets[i].btagDeepB > 0.2219:  # DeepCSVL
            #if jets[i].btagDeepB > 0.4184:  # DeepCSVM
            # if jets[i].btagDeepB > 0.6324:  # DeepCSVL
                #btag_cut = True      #initialize
            if abs(jets[i].eta) > 4.7:
                continue
            if jets[i].pt<30:
                continue
            for j in range(0,len(photons_select)):          # delta R cut, if all deltaR(lep,jet) and deltaR(gamma,jet)>0.3, consider jet as a b jet
                if deltaR(jets[i].eta,jets[i].phi,photons[photons_select[j]].eta,photons[photons_select[j]].phi) < 0.5:
                    btag_cut = True
                    #jets_select.append(i)
                    #njets +=1
            for j in range(0,len(electrons_select)):
                if deltaR(jets[i].eta,jets[i].phi,electrons[electrons_select[j]].eta,electrons[electrons_select[j]].phi) < 0.5:
                    btag_cut = True
                    #jets_select.append(i)
                    #njets +=1
            for j in range(0,len(muons_select)):
                if deltaR(jets[i].eta,jets[i].phi,muons[muons_select[j]].eta,muons[muons_select[j]].phi) < 0.5  :
                    btag_cut = True
            if btag_cut == True:
                btagjet_reject += 1
                #return False
            else:
                if jets[i].jetId >> 1 & 1:
                    jets_select.append(i)
                    njets += 1
        #njets = njets + 1
        print ("njets",njets)
        if njets >=2 :
            njet_reject +=1
            return False

        electrons_is_real=-99
        photons_is_real=-99
        muons_is_real = -99
        lepton1_is_real_nano=-99
        lepton2_is_real_nano=-99
        photons_is_real_nano = -99

        leptons_is_real=-99

        isprompt_mask = (1 << 0) #isPrompt
        isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct
        isdirecttaudecayproduct_mask = (1 << 4) #isDirectTauDecayProduct
        isprompttaudecayproduct = (1 << 3) #isPromptTauDecayProduct
        isfromhardprocess_mask = (1 << 8) #isPrompt


        if hasattr(event, 'nGenPart'):
            genparts = Collection(event, "GenPart")
            is_real_flag = 0
            is_real_flag_1 =0
            for i,lep in enumerate(electrons_select):
                for j,genpart in enumerate(genparts):
                    if electrons[electrons_select[i]].genPartIdx >=0:
                        if genpart.pt>5 and abs(genpart.pdgId)==11 and deltaR(electrons[electrons_select[i]].eta, electrons[electrons_select[i]].phi, genpart.eta, genpart.phi) < 0.3 and ((genparts[electrons[electrons_select[i]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[electrons[electrons_select[i]].genPartIdx].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)):
                            if i <1 : is_real_flag=1
                            if i >=1 : is_real_flag_1 =1
                            break
                        else:
                            if i <1 : is_real_flag =0
                            if i >= 1: is_real_flag_1 = 0

            if len(electrons_select) ==1 and is_real_flag ==1: electrons_is_real =1
            if len(electrons_select) == 2 and is_real_flag ==1 and is_real_flag_1 ==1:electrons_is_real =1

            is_real_flag = 0
            is_real_flag_1 = 0
            for i, mu in enumerate(muons_select):
                for j, genpart in enumerate(genparts):
                    if muons[muons_select[i]].genPartIdx >=0:
                        if genpart.pt > 5 and abs(genpart.pdgId) == 13 and deltaR(muons[muons_select[i]].eta, muons[muons_select[i]].phi,genpart.eta,genpart.phi) < 0.3 and ((genparts[muons[muons_select[i]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[muons[muons_select[i]].genPartIdx].statusFlags & isprompttaudecayproduct == isprompttaudecayproduct)):
                            if i < 1: is_real_flag = 1
                            if i >= 1: is_real_flag_1 = 1
                            break
                        else:
                            if i < 1: is_real_flag = 0
                            if i >= 1: is_real_flag_1 = 0
            if len(muons_select)==1 and is_real_flag == 1:  muons_is_real=1
            if len(muons_select)==2 and is_real_flag == 1 and is_real_flag_1 ==1: muons_is_real=1

            is_real_flag = 0
            for i, pho in enumerate(photons_select):
                for j, genpart in enumerate(genparts):
                    if photons[photons_select[i]].genPartIdx >=0:
                        if genpart.pt > 5 and abs(genpart.pdgId) == 22 and ((genparts[photons[photons_select[i]].genPartIdx].statusFlags & isprompt_mask == isprompt_mask) or (genparts[photons[photons_select[i]].genPartIdx].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask) or (genparts[photons[photons_select[i]].genPartIdx].statusFlags & isfromhardprocess_mask == isfromhardprocess_mask)) and deltaR(photons[photons_select[i]].eta,photons[photons_select[i]].phi,genpart.eta,genpart.phi) < 0.3:
                            is_real_flag =1
                            break
            if is_real_flag == 1: photons_is_real=1

        #dilepton mass selection and channel selection
        channel = 0 
        # emu:     1
        # ee:      2
        # mumu:    3

        # emu
        dileptonmass = -1.0
        if len(muons_select)==1 and len(electrons_select)==1:  # emu channel 
            #print (muons[muons_select[0]].pdgId,electrons[electrons_select[0]].pdgId)

            if deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi) < 0.5:
                deltar_reject +=1
                return False
            
            if muons[muons_select[0]].charge * (electrons[electrons_select[0]].charge) < 0:
                dileptonmass = (muons[muons_select[0]].p4() + electrons[electrons_select[0]].p4()).M()
                #dileptongmass = (muons[muons_select[0]].p4() + electrons[electrons_select[0]].p4()+photons[photons_select[0]].p4()).M()
                dileptonpt = (muons[muons_select[0]].p4() + electrons[electrons_select[0]].p4()).Pt()
                dileptonmass_emu = (muons[muons_select[0]].p4() + electrons[electrons_select[0]].p4()).M()
                dileptongmass_emu = (muons[muons_select[0]].p4() + electrons[electrons_select[0]].p4()+photons[photons_select[0]].p4()).M()
                dileptonpt_emu = (muons[muons_select[0]].p4() + electrons[electrons_select[0]].p4()).Pt()
                met_emu = event.MET_pt
                #if dileptonmass >= 50 and dileptonmass <= 100 :
                #    mll_reject +=1
                #    return False
                if dileptonpt <= 40:
                    pt_reject +=1
                    return False
                if met_emu <40:
                    return False

                # if dileptonmass >= 60 and dileptonmass <= 120:
                # print "a=",photons_select, "e=",electrons_select, "mu=",muons_select
            else:
                different_charge_reject +=1
                return False
            if dileptonmass > 0 and pass_HLT_emu:
                channel = 1
                emu_pass += 1
            else :
                minus_mll +=1
                return False

        # ee
        if len(muons_select)==0 and len(electrons_select)==2:
            if deltaR(electrons[electrons_select[0]].eta,electrons[electrons_select[0]].phi,electrons[electrons_select[1]].eta,electrons[electrons_select[1]].phi)<0.5:
                deltar_reject +=1
                return False
             
            if electrons[electrons_select[0]].charge * electrons[electrons_select[1]].charge <0:
                dileptonmass = (electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()).M()
                dileptongmass = (electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()+photons[photons_select[0]].p4()).M()
                dileptonpt = (electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()).Pt()
                dileptonmass_ee = (electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()).M()
                dileptongmass_ee = (electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()+photons[photons_select[0]].p4()).M()
                dileptonpt_ee = (electrons[electrons_select[0]].p4() + electrons[electrons_select[1]].p4()).Pt()
                
                met_ee = event.MET_pt
                if dileptonmass >= 50 and dileptonmass <= 100 :
                    mll_reject +=1
                    return False
                if dileptonpt <= 40: 
                    pt_reject +=1
                    return False
                if met_ee <60:
                    return False
            else:
                different_charge_reject +=1
                return False
            if dileptonmass > 0 and pass_HLT_ee:
                channel = 2
                ee_pass += 1
            else:
                minus_mll +=1
                return False


        # mumu 
        if len(electrons_select)==0 and len(muons_select)==2:
            if deltaR(muons[muons_select[0]].eta,muons[muons_select[0]].phi,muons[muons_select[1]].eta,muons[muons_select[1]].phi)<0.5:
                deltar_reject +=1
                return False
            if muons[muons_select[0]].charge * muons[muons_select[1]].charge < 0:
                dileptonmass = (muons[muons_select[0]].p4() + muons[muons_select[1]].p4()).M()
                dileptongmass = (muons[muons_select[0]].p4() + muons[muons_select[1]].p4()+photons[photons_select[0]].p4()).M()
                dileptonpt = (muons[muons_select[0]].p4() + muons[muons_select[1]].p4()).Pt()
                dileptonmass_mumu = (muons[muons_select[0]].p4() + muons[muons_select[1]].p4()).M()
                dileptongmass_mumu = (muons[muons_select[0]].p4() + muons[muons_select[1]].p4()+photons[photons_select[0]].p4()).M()
                met_mumu = event.MET_pt
                dileptonpt_mumu = (muons[muons_select[0]].p4() + muons[muons_select[1]].p4()).Pt()
                if dileptonmass >= 50 and dileptonmass <= 100 :
                    mll_reject +=1
                    return False
                if dileptonpt <= 40: 
                    pt_reject +=1
                    return False
                if met_mumu <60:
                    return False
                # print "a=",photons_select, "e=",electrons_select, "mu=",muons_select
            else:
                different_charge_reject +=1
                return False
            if dileptonmass > 0 and pass_HLT_mumu:
                channel = 3
                mumu_pass += 1
            else :
                minus_mll +=1
                return False

 #    test 
        if channel == 0:
            print len(electrons_select),len(muons_select)
            return False

        #self.out.fillBranch("MET",event.MET_pt)
        #self.out.fillBranch("photon_pt",photons[photons_select[0]].pt)
        #self.out.fillBranch("photon_eta",photons[photons_select[0]].eta)
        #self.out.fillBranch("photon_phi",photons[photons_select[0]].phi)
        #self.out.fillBranch("photon_sieie",photons[photons_select[0]].sieie)
        #self.out.fillBranch("Njets",njets)
        if channel == 1:
            self.out.fillBranch("electrons_is_real",electrons_is_real)
            self.out.fillBranch("photons_is_real", photons_is_real)
            self.out.fillBranch("muons_is_real", muons_is_real)
            self.out.fillBranch("dilepton_mass_emu",dileptonmass_emu)
            self.out.fillBranch("dilepton_g_mass_emu",dileptongmass_emu)
            self.out.fillBranch("dilepton_pt_emu",dileptonpt_emu)
            self.out.fillBranch("Njets_emu",njets)
            self.out.fillBranch("MET_emu",met_emu)
            self.out.fillBranch("photon_pt_emu",photons[photons_select[0]].pt)
            self.out.fillBranch("photon_eta_emu",photons[photons_select[0]].eta)
            self.out.fillBranch("photon_phi_emu",photons[photons_select[0]].phi)
            if hasattr(event, 'nGenPart'):self.out.fillBranch("photons_is_real_nano", photons[photons_select[0]].genPartFlav)
            #lep1_pt lep2_pt
            if muons[muons_select[0]].pt > electrons[electrons_select[0]].pt:
                self.out.fillBranch("lepton1_pt_emu",muons[muons_select[0]].pt)
                self.out.fillBranch("lepton2_pt_emu",electrons[electrons_select[0]].pt)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton1_is_real_nano", muons[muons_select[0]].genPartFlav)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton2_is_real_nano", electrons[electrons_select[0]].genPartFlav)
            else:
                self.out.fillBranch("lepton2_pt_emu",muons[muons_select[0]].pt)
                self.out.fillBranch("lepton1_pt_emu",electrons[electrons_select[0]].pt)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton2_is_real_nano", muons[muons_select[0]].genPartFlav)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton1_is_real_nano", electrons[electrons_select[0]].genPartFlav)

            #self.out.fillBranch("photon_sieie",photons[photons_select[0]].sieie)

        elif channel == 2:
            #self.out.fillBranch("Njets",njets)
            self.out.fillBranch("electrons_is_real",electrons_is_real)
            self.out.fillBranch("photons_is_real", photons_is_real)
            self.out.fillBranch("muons_is_real", muons_is_real)
            self.out.fillBranch("dilepton_mass_ee", dileptonmass_ee)
            self.out.fillBranch("dilepton_g_mass_ee",dileptongmass_ee)
            self.out.fillBranch("dilepton_pt_ee",dileptonpt_ee)
            self.out.fillBranch("Njets_ee",njets)
            self.out.fillBranch("MET_ee",met_ee)
            self.out.fillBranch("photon_pt_ee",photons[photons_select[0]].pt)
            self.out.fillBranch("photon_eta_ee",photons[photons_select[0]].eta)
            self.out.fillBranch("photon_phi_ee",photons[photons_select[0]].phi)
            if hasattr(event, 'nGenPart'):self.out.fillBranch("photons_is_real_nano", photons[photons_select[0]].genPartFlav)
            #lep1_pt lep2_pt
            if electrons[electrons_select[0]].pt > electrons[electrons_select[1]].pt:
                self.out.fillBranch("lepton1_pt_ee",electrons[electrons_select[0]].pt)
                self.out.fillBranch("lepton2_pt_ee",electrons[electrons_select[1]].pt)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton1_is_real_nano", electrons[electrons_select[0]].genPartFlav)
                if hasattr(event, 'nGenPart'): self.out.fillBranch("lepton2_is_real_nano", electrons[electrons_select[1]].genPartFlav)
            else:
                self.out.fillBranch("lepton2_pt_ee",electrons[electrons_select[0]].pt)
                self.out.fillBranch("lepton1_pt_ee",electrons[electrons_select[1]].pt)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton2_is_real_nano", electrons[electrons_select[0]].genPartFlav)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton1_is_real_nano", electrons[electrons_select[1]].genPartFlav)

        elif channel == 3:
            #self.out.fillBranch("lepton_motherid_mumu",genparts[genparts[muons[muons_select[0]].genPartIdx].genPartIdxMother].pdgId)
            #self.out.fillBranch("lepton_motherid_mumu",genparts[genparts[muons[muons_select[1]].genPartIdx].genPartIdxMother].pdgId)
            #self.out.fillBranch("Njets",njets)
            self.out.fillBranch("electrons_is_real",electrons_is_real)
            self.out.fillBranch("photons_is_real", photons_is_real)
            self.out.fillBranch("muons_is_real", muons_is_real)
            self.out.fillBranch("dilepton_mass_mumu",dileptonmass_mumu)
            self.out.fillBranch("dilepton_g_mass_mumu",dileptongmass_mumu)
            self.out.fillBranch("dilepton_pt_mumu",dileptonpt_mumu)
            self.out.fillBranch("Njets_mumu",njets)
            self.out.fillBranch("MET_mumu",met_mumu)
            self.out.fillBranch("photon_pt_mumu",photons[photons_select[0]].pt)
            self.out.fillBranch("photon_eta_mumu",photons[photons_select[0]].eta)
            self.out.fillBranch("photon_phi_mumu",photons[photons_select[0]].phi)
            if hasattr(event, 'nGenPart'):self.out.fillBranch("photons_is_real_nano", photons[photons_select[0]].genPartFlav)
            #lep1_pt lep2_pt
            if muons[muons_select[0]].pt > muons[muons_select[1]].pt:
                self.out.fillBranch("lepton1_pt_mumu",muons[muons_select[0]].pt)
                self.out.fillBranch("lepton2_pt_mumu",muons[muons_select[1]].pt)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton1_is_real_nano", muons[muons_select[0]].genPartFlav)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton2_is_real_nano", muons[muons_select[1]].genPartFlav)
            else:
                self.out.fillBranch("lepton2_pt_mumu",muons[muons_select[0]].pt)
                self.out.fillBranch("lepton1_pt_mumu",muons[muons_select[1]].pt)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton2_is_real_nano", muons[muons_select[0]].genPartFlav)
                if hasattr(event, 'nGenPart'):self.out.fillBranch("lepton1_is_real_nano", muons[muons_select[1]].genPartFlav)


        #self.out.fillBranch("event",event.event)
        #self.out.fillBranch("dilepton_mass",dileptonmass)
        #self.out.fillBranch("dilepton_g_mass",dileptongmass)
        #self.out.fillBranch("dilepton_pt",dileptonpt)
        #self.out.fillBranch("Generator_weight",event.Generator_weight)
        self.out.fillBranch("channel_mark",channel)
        return True

WWG_Producer_EGamma = lambda: WWG_Producer(isdata=True,kind='EGamma')
WWG_Producer_DoubleMuon = lambda: WWG_Producer(isdata=True,kind='DoubleMuon')
WWG_Producer_MuonEG = lambda: WWG_Producer(isdata=True,kind='MuonEG')
WWG_Producer_SingleMuon = lambda: WWG_Producer(isdata=True,kind='SingleMuon')
WWG_Producer_MC = lambda: WWG_Producer(isdata=False,kind='MC')

print "MET_pass","\t","=","\t",MET_pass
print "muon_pass","\t","=","\t",muon_pass 
print "electron_pass","\t","=","\t",electron_pass
print "photon_pass","\t","=","\t",photon_pass
print
print "none_photon_reject","\t","=","\t",none_photon_reject
print "none_lepton_reject","\t","=","\t",none_lepton_reject
print "none_2lepton_reject","\t","=","\t",none_2lepton_reject
print "different_charge_reject","\t","=","\t",different_charge_reject
print "minus_mll ","\t","=","\t",minus_mll 
print "all reject",none_photon_reject+none_2lepton_reject+different_charge_reject+minus_mll


print "emu_pass","\t","=","\t",emu_pass
print "ee_pass","\t","=","\t",ee_pass
print "mumu_pass","\t","=","\t",mumu_pass
print "btagjet_reject","\t","=","\t",btagjet_reject
print "deltar_reject","\t","=","\t",deltar_reject
print "n_posi","\t","=","\t",n_posi
print "n_minus","\t","=","\t",n_minus
print "n_num","\t","=","\t",n_num


