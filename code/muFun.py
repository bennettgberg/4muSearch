# !/usr/bin/env python

""" muFun.py: apply selection sequence to four-lepton final state """

import io
import yaml
import subprocess
from ROOT import TLorentzVector,TFile
from math import sqrt, sin, cos, pi
from itertools import combinations
import os
import os.path
import sys
sys.path.append('../TauPOG')
#from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
#from TauPOG.TauIDSFs.TauIDSFTool import TauESTool
#from TauPOG.TauIDSFs.TauIDSFTool import TauFESTool

__author__ = "Dan Marlow, Alexis Kalogeropoulos, Gage DeZoort"
__date__   = "Monday, Oct. 28th, 2019"


# get selections from configZH.yaml:
#with io.open('cuts.yaml', 'r') as stream:
#with io.open('cuts_ZH.yaml', 'r') as stream:
with io.open('cuts_4mu.yaml', 'r') as stream:
    selections = yaml.load(stream)
print "Using selections:\n", selections

#returns the list of muon trigger paths for the given year.
def muonTriggers(year):
    if year in [2016, 2017, 2018]:
        triggers = [
            "HLT_IsoMu22",
            "HLT_IsoMu22_eta2p1",
            "HLT_IsoTkMu22",
            "HLT_IsoTkMu22_eta2p1",
            "HLT_IsoMu27",
            "HLT_IsoMu24",
            "HLT_IsoTkMu24",
            "HLT_TripleMu_12_10_5",
            "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
            "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
            "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
            "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",
            "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_Mass8" ]
    else:
        print("Error! Muon triggers for year {} unknown.")
        triggers = []
        
    return triggers

def doubleMuonTriggers(year='2017'):
    if year == '2018':
        triggers = ['DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched',
        'DoubleL2Mu23NoVtx_2Cha_CosmicSeed',
        'DoubleL2Mu23NoVtx_2Cha_NoL2Matched',
        'DoubleL2Mu23NoVtx_2Cha',
        'DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4',
        'DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched',
        'DoubleL2Mu25NoVtx_2Cha_CosmicSeed',
        'DoubleL2Mu25NoVtx_2Cha_Eta2p4',
        'DoubleL2Mu25NoVtx_2Cha_NoL2Matched',
        'DoubleL2Mu25NoVtx_2Cha',
        'DoubleL2Mu30NoVtx_2Cha_CosmicSeed_Eta2p4',
        'DoubleL2Mu30NoVtx_2Cha_Eta2p4',
        'DoubleL2Mu50',
        'DoubleMu33NoFiltersNoVtxDisplaced',
        'DoubleMu3_DCA_PFMET50_PFMHT60',
        'DoubleMu3_DZ_PFMET50_PFMHT60',
        'DoubleMu3_DZ_PFMET70_PFMHT70',
        'DoubleMu3_DZ_PFMET90_PFMHT90',
        'DoubleMu40NoFiltersNoVtxDisplaced',
        'DoubleMu43NoFiltersNoVtx',
        'DoubleMu48NoFiltersNoVtx',
        'DoubleMu4_Mass3p8_DZ_PFHT350',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',
        'Mu17_TrkIsoVVL',
        'Mu17',
        'Mu18_Mu9_DZ',
        'Mu18_Mu9_SameSign_DZ',
        'Mu18_Mu9_SameSign',
        'Mu18_Mu9',
        'Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8',
        'Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8',
        'Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ',
        'Mu19_TrkIsoVVL_Mu9_TrkIsoVVL',
        'Mu19_TrkIsoVVL',
        'Mu19',
        'Mu20_Mu10_DZ',
        'Mu20_Mu10_SameSign_DZ',
        'Mu20_Mu10_SameSign',
        'Mu20_Mu10',
        'Mu23_Mu12_DZ',
        'Mu23_Mu12_SameSign_DZ',
        'Mu23_Mu12_SameSign',
        'Mu23_Mu12',
        'Mu37_TkMu27',
        'Mu8_TrkIsoVVL',
        'Mu8',
        'TripleMu_10_5_5_DZ',
        'TripleMu_12_10_5',
        'TripleMu_5_3_3_Mass3p8_DCA',
        'TripleMu_5_3_3_Mass3p8_DZ',
        'TrkMu12_DoubleTrkMu5NoFiltersNoVtx',
        'TrkMu16_DoubleTrkMu6NoFiltersNoVtx',
        'TrkMu17_DoubleTrkMu8NoFiltersNoVtx' ]
    elif year == '2017':
        triggers = ['DoubleL2Mu50',
        'DoubleMu3_DCA_PFMET50_PFMHT60',
        'DoubleMu3_DZ_PFMET50_PFMHT60',
        'DoubleMu3_DZ_PFMET70_PFMHT70',
        'DoubleMu3_DZ_PFMET90_PFMHT90',
        'DoubleMu43NoFiltersNoVtx',
        'DoubleMu48NoFiltersNoVtx',
        'DoubleMu4_Mass8_DZ_PFHT350',
        'DoubleMu8_Mass8_PFHT350',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',
        'Mu17_TrkIsoVVL',
        'Mu17',
        'Mu18_Mu9_DZ',
        'Mu18_Mu9_SameSign_DZ',
        'Mu18_Mu9_SameSign',
        'Mu18_Mu9',
        'Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8',
        'Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8',
        'Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ',
        'Mu19_TrkIsoVVL_Mu9_TrkIsoVVL',
        'Mu19_TrkIsoVVL',
        'Mu19',
        'Mu20_Mu10_DZ',
        'Mu20_Mu10_SameSign_DZ',
        'Mu20_Mu10_SameSign',
        'Mu20_Mu10',
        'Mu23_Mu12_DZ',
        'Mu23_Mu12_SameSign_DZ',
        'Mu23_Mu12_SameSign',
        'Mu23_Mu12',
        'Mu37_TkMu27',
        'Mu8_TrkIsoVVL',
        'Mu8',
        'TripleMu_10_5_5_DZ',
        'TripleMu_12_10_5',
        'TripleMu_5_3_3_Mass3p8to60_DCA',
        'TripleMu_5_3_3_Mass3p8to60_DZ',
        'TrkMu12_DoubleTrkMu5NoFiltersNoVtx',
        'TrkMu16_DoubleTrkMu6NoFiltersNoVtx',
        'TrkMu17_DoubleTrkMu8NoFiltersNoVtx']
    elif year == '2016':
        triggers = ['DoubleMu0',
        'DoubleMu18NoFiltersNoVtx',
        'DoubleMu23NoFiltersNoVtxDisplaced',
        'DoubleMu28NoFiltersNoVtxDisplaced',
        'DoubleMu33NoFiltersNoVtx',
        'DoubleMu38NoFiltersNoVtx',
        'DoubleMu8_Mass8_PFHT300',
        'L2DoubleMu23_NoVertex',
        'L2DoubleMu28_NoVertex_2Cha_Angle2p5_Mass10',
        'L2DoubleMu38_NoVertex_2Cha_Angle2p5_Mass10',
        'Mu10_CentralPFJet30_BTagCSV_p13',
        'Mu17_Mu8_DZ',
        'Mu17_Mu8_SameSign_DZ',
        'Mu17_Mu8_SameSign',
        'Mu17_Mu8',
        'Mu17_TkMu8_DZ',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
        'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',
        'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
        'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL',
        'Mu17_TrkIsoVVL',
        'Mu17',
        'Mu20_Mu10_DZ',
        'Mu20_Mu10_SameSign_DZ',
        'Mu20_Mu10_SameSign',
        'Mu20_Mu10',
        'Mu27_TkMu8',
        'Mu30_TkMu11',
        'Mu3_PFJet40',
        'Mu40_TkMu11',
        'Mu8_TrkIsoVVL',
        'Mu8',
        'TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
        'TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL',
        'TripleMu_12_10_5',
        'TripleMu_5_3_3_DZ_Mass3p8',
        'TrkMu15_DoubleTrkMu5NoFiltersNoVtx',
        'TrkMu17_DoubleTrkMu8NoFiltersNoVtx']
    else:
        print("Error: unrecognized year %s, options are 2016, 2017, 2018."%(year))

    return triggers

#returns list of electron trigger paths for the given year.
def electronTriggers(year):
    if year in [2016, 2017, 2018]:
        triggers = [
            "HLT_Ele25_eta2p1_WPTight_Gsf",
            "HLT_Ele27_WPTight_Gsf",
            "HLT_Ele32_WPTight_Gsf",
            "HLT_Ele35_WPTight_Gsf",
            "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",
            "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]
    else:
        print("Error! Electron triggers unknown for year {}.")
        triggers = []
        
    return triggers

#returns list of tau trigger paths for the given year.
def tauTriggers(year):
    if year in [2016, 2017, 2018]:
        triggers = ["HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15",
                    "HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1",
                    "HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15",
                    "HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1",
                    "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg",
                    "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg",
                    "HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg",
                    "HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_eta2p1_Reg",
                    "HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg",
                    "HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg",
                    "HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg",
                    "HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg",
                    "HLT_VBF_DoubleLooseChargedIsoPFTauHPS20_Trk1_eta2p1",
                    "HLT_VBF_DoubleMediumChargedIsoPFTauHPS20_Trk1_eta2p1",
                    "HLT_VBF_DoubleTightChargedIsoPFTauHPS20_Trk1_eta2p1",
                    "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
#word0 ^^^
                    "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
                    "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
                    "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
                    "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
                    "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
                    "HLT_DoubleMu3_Trk_Tau3mu",
                    "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
                    "HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1",
                    "HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1",
                    "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1",
                    "HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1",
                    "HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1",
                    "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1",
                    "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1",
                    "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1",
                    "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1",
#word1 ^^^
                    "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1",
                    "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1",
                    "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
                    "HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTau30_eta2p1_CrossL1",
                    "HLT_Ele24_eta2p1_WPTight_Gsf_TightChargedIsoPFTau30_eta2p1_CrossL1",
                    "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_TightID_CrossL1",
                    "HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTau30_eta2p1_TightID_CrossL1",
                    "HLT_Ele24_eta2p1_WPTight_Gsf_TightChargedIsoPFTau30_eta2p1_TightID_CrossL1",
                    "HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg",
                    "HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg",
                    "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg",
                    "HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg",
                    "HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg",
                    "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
                    "HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
                    "HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
#word2 ^^^
                    "HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
                    "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
                    "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
                    "HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg" ]
#word3 ^^^
    else:
        print("Error! Tau trigger code for year {} not yet written.")
        triggers = []
        
    return triggers

#returns True if e passes the trigger for year, else False (for 4tau only).
def goodTrigger_4mu(e, year, debug=False):
    printOn = debug

    #muonTrigs = muonTriggers(year)
    #electronTrigs = electronTriggers(year)
    #tauTrigs = tauTriggers(year)
    doubleMuonTrigs = doubleMuonTriggers(year)

    #goodmuon = False
    #goodelectron = False
    #goodtau = False
    gooddoubleMuon = False
    #for p in ["muon", "electron", "tau"]:
    for p in ["doubleMuon"]:
        exec("trigs = %sTrigs"%(p))
        for t in trigs:
            if printOn:
                print("trigger: {}".format(t))
            try:
                exec("passed = e.HLT_%s"%(t))
            except AttributeError:
                passed = False
            if passed:
                exec("good%s = True"%(p))
                break

    #return goodmuon or goodelectron or goodtau
    return gooddoubleMuon
                

def goodTrigger(e, year):
    trig = selections['trig']
    if not (trig['singleLepton'] or trig['doubleLepton'] or trig['tripleLepton']) : return True
    #single mu 2016: HLT IsoMu22 v, HLT IsoMu22 eta2p1 v, HLT IsoTkMu22 v, HLT IsoTkMu22 eta2p1 v and cut pt(mu)>23, eta(mu)<2.1
    #single ele 2016: HLT Ele25 eta2p1 WPTight Gsf v and cut pt(ele)>26, eta(ele)<2.1
    #single mu 2017: HLT IsoMu24 v, HLT IsoMu27 v and cut pt(mu)>25, eta(mu)<2.4
    #single ele 2017: HLT Ele27 WPTight Gsf v, HLT Ele32 WPTight Gsf v, HLT Ele35 WPTight Gsf v and cut pt(ele)>28, eta(ele)<2.1
    #single mu 2018: HLT IsoMu24 v, HLT IsoMu27 v and cut pt(mu)>25, eta(mu)<2.4
    #single ele 2018:  HLT Ele32 WPTight Gsf v, HLT Ele35 WPTight Gsf v and cut pt(ele)>33, eta(ele)<2.1

    #HLT_TripleMu_10_5_5_DZ
    #HLT_TripleMu_12_10_5
    #HLT_TripleMu_5_3_3_Mass3p8_DCA
    #HLT_TripleMu_5_3_3_Mass3p8_DZ


    if year == 2016 :
        goodSingle = (e.HLT_IsoMu22 or e.HLT_IsoMu22_eta2p1 or e.HLT_IsoTkMu22 or e.HLT_IsoTkMu22_eta2p1 or e.HLT_Ele25_eta2p1_WPTight_Gsf or e.HLT_Ele27_eta2p1_WPTight_Gsf or e.HLT_IsoMu24 or e.HLT_IsoTkMu24 or e.HLT_IsoMu27)

        goodDouble = (e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ or e.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ )
        goodTriple = (e.HLT_TripleMu_12_10_5)
    elif (year == 2017 or year == 2018) :
        goodSingle = (e.HLT_Ele27_WPTight_Gsf or e.HLT_Ele35_WPTight_Gsf or e.HLT_Ele32_WPTight_Gsf or e.HLT_IsoMu24 or e.HLT_IsoMu27)

        goodDouble = (e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL or e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ  or e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 or e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)
        goodTriple = (e.HLT_TripleMu_12_10_5)



    else :
        print("Invalid year={0:d} in goodTrigger()".format(year))
        return False

    return (trig['singleLepton'] and goodSingle) or (trig['doubleLepton'] and goodDouble) or (trig['tripleLepton'] and goodTriple)


def getGoodTauList(channel, entry, printOn=False) :
    """ tauFun.getTauList(): return a list of taus that
                             pass the basic selection cuts
    """

    if entry.nTau == 0: return []

    tauList = []
    tt = selections['tt'] # selections for H->tau(h)+tau(h)

    #for j in range(entry.nTau):
    '''
    for reco tauh matched to electrons at gen level in the format (dm0, dm1): for 2016 (-0.5%, +6.0%), for 2017 (+0.3%, +3.6%), for 2018 (-3.2%, +2.6%)
    for reco tauh matched to muons at gen level in the format (dm0, dm1): for 2016 (+0.0%, -0.5%), for 2017 (+0.0%, +0.0%), for 2018 (-0.2%, -1.0%)
    '''
    for j in range(entry.nTau):
        # apply tau(h) selections
        if entry.Tau_pt[j] < tt['tau_pt']: continue
        if abs(entry.Tau_eta[j]) > tt['tau_eta']: continue
        if abs(entry.Tau_dz[j]) > tt['tau_dz']: continue
        if not entry.Tau_idDecayModeNewDMs[j]: continue
        if  entry.Tau_decayMode[j] == 5 or entry.Tau_decayMode[j] == 6 : continue
        if abs(entry.Tau_charge[j]) != 1: continue

        if tt['tau_vJet'] > 0  and not ord(entry.Tau_idDeepTau2017v2p1VSjet[j]) & tt['tau_vJet'] > 0 :
            if printOn : print("        fail DeepTau vs. Jet={0:d}".format(ord(entry.Tau_idDeepTau2017v2p1VSjet[j])))
            continue
        if tt['tau_vEle'] > 0 and not ord(entry.Tau_idDeepTau2017v2p1VSe[j]) & tt['tau_vEle'] > 0 :
            if printOn : print("        fail DeepTau vs. ele={0:d}".format(ord(entry.Tau_idDeepTau2017v2p1VSe[j])))
            continue
        if tt['tau_vMu'] > 0 and not ord(entry.Tau_idDeepTau2017v2p1VSmu[j]) & tt['tau_vMu'] > 0 :
            if printOn : print("        fail DeepTau vs.  mu={0:d}".format(ord(entry.Tau_idDeepTau2017v2p1VSmu[j])))
            continue

        tauList.append(j)

    return tauList

def mllCut(mll) :
    mllcuts = selections['mll']
    if mll < mllcuts['mll_low'] or mll > mllcuts['mll_high'] : return False
    return True

def getTauPointer(entry, eta1, phi1) :
    # find the j value that most closely matches the specified eta or phi value
    bestMatch, jBest = 999., -1
    for j in range(entry.nTau) :
        eta2, phi2 = entry.Tau_eta[j], entry.Tau_phi[j]
        dPhi = min(abs(phi2-phi1),2.*pi-abs(phi2-phi1))
        DR = sqrt(dPhi**2 + (eta2-eta1)**2)
        if DR < bestMatch : bestMatch, jBest = DR, j
    if bestMatch > 0.1 :
        jBest = -1
        print("Error in getTauPointer():   No match found eta={0:.3f} phi={1:.3f}".format(eta1,phi1))
    return jBest

def comparePairvspT(entry, tauPairList, printOn=False) :
    """ comparevsPt : return the index of the pair with the highest scalar sum
    """
    SumList=[]
    for i in range(0,len(tauPairList)) :

        j1, j2 = tauPairList[i][0], tauPairList[i][1] # look at leading pt tau in each pair
        if printOn : print 'appending now', entry.Tau_pt[j1] + entry.Tau_pt[j2], j1, j2, tauPairList[i]
        SumList.append(entry.Tau_pt[j1] + entry.Tau_pt[j2])


    maxI=SumList.index(max(SumList))

    return maxI

#for AA->4Tau
#opp is True if you are requring the leading taus to be oppositely charged.
def get2BestTauPairPt(channel, entry, tauList, opp=False) :
    """ tauFun.get2BestTauPairPt(): return two tau pairs that 
                                 best represent H->tt
    """ 

    if not channel == 'tttt' : 
        print("Invalid channel={0:s} in tauFun.get2BestTauPair()".format(channel))
        exit()

    if len(tauList) < 4: return [] 
    print("Before cuts, taulist = {}".format(str(tauList)))
    # form all possible pairs that satisfy DR requirement
    tauPairList = []
    tt = selections['tt'] # selections for H->(tau_h)(tau_h)
    for i in range(len(tauList)) :
        idx_tau1 = tauList[i]
        #don't need both [i,j] and [j,i].
        for j in range(i+1, len(tauList)) :
#            if i == j: continue
            idx_tau2 = tauList[j]
            if tauDR(entry, idx_tau1, idx_tau2) < tt['tt_DR'] : continue
            tauPairList.append([idx_tau1, idx_tau2])
    print("Pairlist before sorting: {}".format(str(tauPairList)))
    # Sort the pair list using a bubble sort
    # The list is not fully sorted, since only the top 2 pairings are needed
        #BUT these two pairings cannot share any taus.
    idx_pair1 = -1
    idx_pair2 = -1 #correct index for the second pair (with taus that are not shared with the first pair)
    for k in range(len(tauPairList)):
        for i in range(len(tauPairList)-1,k,-1) :
            if not comparePairPt(entry, tauPairList[i],tauPairList[i-1]) : 
                #swap i and i-1.
#                tauPairList[i-1], tauPairList[i] = tauPairList[i], tauPairList[i-1] 
                temp = tauPairList[i-1]
                tauPairList[i-1] = tauPairList[i]
                tauPairList[i] = temp
            if entry.event == 362468: print("k={}, i={}, tauPairList={}".format(k, i, str(tauPairList)))
        #if opp is false then idx_pair1 is always 0
        if idx_pair1 < 0:
            if not opp:
                idx_pair1 = 0
            #if the two taus are oppositely charged, then they are a viable candidate for pair1.
            elif entry.Tau_charge[tauPairList[k][0]]*entry.Tau_charge[tauPairList[k][1]] < 0:
                idx_pair1 = k
        #if we have 2 pairs with 4 unique taus then we're done.
        elif tauPairList[k][0] not in tauPairList[idx_pair1] and tauPairList[k][1] not in tauPairList[idx_pair1]:
            #for pair2, the taus don't necessarily have to be oppositely charged. They just have to be unique from pair1.
            idx_pair2 = k
            print("good 4tau event! event={}, idx_pair2={}".format(entry.event, idx_pair2))
            break
#    if len(tauPairList) < 2 : return []
    #if idx_pair2 is not a valid index then there were not 2 fully unique pairs.
    if idx_pair2 < 0: return []
    #now make sure the 2 taus within each pair are sorted by pT.
    for k in [idx_pair1, idx_pair2]:
        idx_tau1, idx_tau2 = tauPairList[k][0], tauPairList[k][1]
        if entry.Tau_pt[idx_tau2] > entry.Tau_pt[idx_tau1] : 
            temp = tauPairList[k][0]
            tauPairList[k][0] = tauPairList[k][1]
            tauPairList[k][1] = temp
       #return as a list of length 4 
    return [tauPairList[idx_pair1][0], tauPairList[idx_pair1][1], tauPairList[idx_pair2][0], tauPairList[idx_pair2][1]]

#new comparePairPt function which is compatible with any particle types (just specify with lepTypes argument)
def comparePairPt(entry,pair1,pair2, lepTypes='tt'):
    # a return value of True means that pair2 is "better" than pair 1 
    #"better" meaning has higher scalar pt sum
    pairs = [pair1, pair2]
    ptsums = [0.0, 0.0]
    #for each of the 2 pairs
    for ii in range(2):
        #for each of the 2 members of the pair
        for jj in range(2):
            #add the correct amount of pt to the correct place.
            if lepTypes[jj] == 't':
                add_pt = entry.Tau_pt[pairs[ii][jj]]
            elif lepTypes[jj] == 'm':
                add_pt = entry.Muon_pt[pairs[ii][jj]]
            elif lepTypes[jj] == 'e':
                add_pt = entry.Electron_pt[pairs[ii][jj]]
            else:
                print("Error in comparePairPt: unrecognized lepTypes: {}".format(lepTypes))
                return False
            ptsums[ii] += add_pt
#    i1, i2, j1, j2 = pair1[0], pair2[0], pair1[1], pair2[1]
#    if (entry.Tau_pt[i2] + entry.Tau_pt[j2] > entry.Tau_pt[i1] + entry.Tau_pt[j1]):
#        return True 
    
#    return False
    return (ptsums[1] > ptsums[0])

#return the full lepton name based on just the letter.
def lepname(letter): 
    if letter == 'e':
        lname = "Electron"
    elif letter == 'm':
        lname = "Muon"
    elif letter == 't':
        lname = "Tau"
    else:
        print("Error! unrecognized lepton letter %s"%(letter))
        sys.exit()
    return lname

#return dR between 2 particles with eta/phi coords (eta0,phi0) and (eta1,phi1).
def pair_dR(eta0, phi0, eta1, phi1):
    deta = eta1 - eta0
    dphi = abs(phi1 - phi0)
    #phi is circular, goes from -pi to pi
    dphi = min(dphi, abs(2*pi - dphi))
    return (deta**2 + dphi**2)**0.5

#find the dR between two particles of lepton types lt, event ev, particle numbers n0, n1.
def find_dR(lt, ev, n0, n1):
    etas = [0., 0.]
    phis = [0., 0.]
    #fill etas and phis for each of the two particles.
    for i in range(2):
        c = n0 if i==0 else n1
        #lepton name
        lname = lepname(lt[i])
        exec("etas[i] = ev.%s_eta[c]"%(lname))
        exec("phis[i] = ev.%s_phi[c]"%(lname))
    #now calculate DR
    dr = pair_dR(etas[0], phis[0], etas[1], phis[1])

    return dr

    
#function to return a list of all valid pairs of valid particles
#lepTypes: 2-char string of lepton types of each list (eg: ee, em, tt, mt,...)
#list0,list1: list of all numbers (corresponding to the entry and the lepton type)
def getAllPairs(lepTypes, entry, list0, list1):
#    print("getAllPairs lepTypes: {}".format(lepTypes))
    #mm and ee selections should instead use the mt/et selections for distance.
    ll = lepTypes
    #if ll[0] == ll[1]:
    #    ll = '{}{}'.format(ll[0], 't')

    #minimum dr between particles
    dr_cut = selections[ll]['lt_DR']

    #demand that pairs have opposite charge or nah
    oppo = selections[ll]['oppQ']

    all_pairs = []
    for a in list0:
        for b in list1:
            #don't repeat twice for same lep type, eg [0,1] and [1,0]
            if lepTypes[0] == lepTypes[1] and b <= a:
                continue
            #print("All Muon pt's:" + str(entry.Muon_pt))
            #print("Muon pt0: " + str(entry.Muon_pt[0]))
            #find the dR between these two particles.
            dr = find_dR(lepTypes, entry, a, b)
            #determine if dr is sufficient
            if dr < dr_cut:
                continue
            #if oppo false, then REQUIRE same sign!
            if oppo or not oppo:
                #find charge of each lepton.
                lname0 = lepname(lepTypes[0])
                lname1 = lepname(lepTypes[1])
                exec("q0 = entry.%s_charge[a]"%(lname0))
                exec("q1 = entry.%s_charge[b]"%(lname1))
                #only want oppositely charged leptons.
                if q0 == q1 and oppo:
                    continue
                elif q0 != q1 and not oppo:
                    continue
            #if sufficient, append to all_pairs.
            all_pairs.append([a,b])

    return all_pairs
            
#partially sort list 'items' so that the first item is in the right place.
def bubble1(lepTypes, entry, items):
    # Sort the pair list using a bubble sort
    # The list is not fully sorted, since only the top pairing is needed
    for i in range(len(items)-1,0,-1) :
        #corrected 2020/07/20
        if not comparePairPt(entry, items[i], items[i-1], lepTypes) : 
            items[i-1], items[i] = items[i], items[i-1] 
    return items

#compare scalar pt sum of 2 different pairs-of-pairs of particles.
# if equal, compare pt of first pair (of the pair of pairs)
def comparePair2(entry, pair1, pair2, lepTypes):
    # a return value of True means that pair2 is "better" than pair 1 
    #"better" meaning has higher scalar pt sum of the 4 particles!
    pair2s = [pair1, pair2]
    #full (4-particle) pt sums
    ptsums = [0.0, 0.0]
    #pt sums of only the first 2 particles (eg tt for ttmt)
    pairpts = [0.0, 0.0]
    #for each of the 2 pair2s
    for ii in range(2):
        #for each of the 2 pairs in the pair of pairs
        for jj in range(2):
            #for each of the 2 members of the pair
            for kk in range(2):
                #get correct lepton type.
                lname = lepname(lepTypes[2*jj+kk])
                #add the correct amount of pt to the correct place.
                exec("add_pt = entry.%s_pt[pair2s[ii][jj][kk]]"%(lname))
                ptsums[ii] += add_pt
                if jj == 0:
                    pairpts[ii] += add_pt

    if ptsums[1] > ptsums[0]:
        return True
    if ptsums[1] < ptsums[0]:
        return False
    #if equal, compare only the first pair.
    return (pairpts[1] > pairpts[0])

#return False if should swap (ie pair2 is better)
def comparePair2_ip3d(entry, pair1, pair2, lepTypes):
    # a return value of True means that pair2 is "better" than pair 1 
    #"better" meaning has higher scalar pt sum of the 4 particles!
    pair2s = [pair1, pair2]
    #full (4-particle) pt sums
    ip3dsums = [0.0, 0.0]
    #for each of the 2 pair2s
    for ii in range(2):
        ip3ds = [0. for jj in range(4)]
        #for each of the 2 pairs in the pair of pairs
        for jj in range(2):
            #for each of the 2 members of the pair
            for kk in range(2):
                #get correct lepton type.
                lname = lepname(lepTypes[2*jj+kk])
                #add the correct amount of pt to the correct place.
                exec("ip3ds[jj*2+kk] = entry.%s_ip3d[pair2s[ii][jj][kk]]"%(lname))
        #now sum the ip3d of the 4 pairings
        for jj in range(4):
            for kk in range(jj+1, 4):
                ip3dsums[ii] += abs(ip3ds[kk]-ip3ds[jj])
        
    if ip3dsums[1] < ip3dsums[0]:
        return True
    return False

#partially sort list 'items' so that only the first item is in the right place.
def bubble2(lepTypes, entry, items):
    # Sort the list of pairs-of-pairs using a bubble sort
    # The list is not fully sorted, since only the top pair-of-pairing is needed
    for i in range(len(items)-1,0,-1) :
        #corrected 2020/07/20
        if not comparePair2(entry, items[i], items[i-1], lepTypes) : 
            items[i-1], items[i] = items[i], items[i-1] 
    return items

#bubble but for min diff ip3d instead of max pt
def bubble_ip3d(lepTypes, entry, items):
    # Sort the list of pairs-of-pairs using a bubble sort
    # The list is not fully sorted, since only the top pair-of-pairing is needed
    for i in range(len(items)-1,0,-1) :
        #corrected 2020/07/20
        if not comparePair2_ip3d(entry, items[i], items[i-1], lepTypes) : 
            items[i-1], items[i] = items[i], items[i-1] 
    return items

#return a 4-vector representing this leptons in entry.
def get4vec(lepType, entry, lep):
    #get their 4-momenta.
    lep4 = TLorentzVector() #leading muon
    #lepton mass
    mlep = 0.0
    pt = 0.0
    eta = 0.0
    phi = 0.0
    #electron
    if lepType == 'e':
        mlep = .000511
        pt = entry.Electron_pt[lep]
        eta = entry.Electron_eta[lep]
        phi = entry.Electron_phi[lep]
    #muon
    elif lepType == 'm':
        mlep = .105
        pt = entry.Muon_pt[lep]
        eta = entry.Muon_eta[lep]
        phi = entry.Muon_phi[lep]
    #tauon
    elif lepType == 't':
        mlep = 1.777
        pt = entry.Tau_pt[lep]
        eta = entry.Tau_eta[lep]
        phi = entry.Tau_phi[lep]
    else:
        print("WARNING: unknown lepton type {}".format(lepType))
    lep4.SetPtEtaPhiM(pt, eta, phi, mlep)
    return lep4

#return the best pair (depending on the channel, either tt, et, or mt, or em, or mm, or ee).
# That is, the pair with the highest scalar sum pT.
# Inputs list0, list1 should already be 'good', ie all individual
#  lepton cuts are already made (channel-specific pair cuts will be made here).
#def getBestPair(lepTypes, entry, eList, mList, tList, pairList=[]) :
def getBestPair(lepTypes, entry, list0, list1, pairList=[]) :
    """ tauFun.getBestPair(): return two taus that 
                                 best represent H->tt
    """ 
    #types of leptons
    ll = lepTypes #channel[2:]
    #all_pairs = getAllPairs(ll, entry, list0, list1, pairList)
    all_pairs = getAllPairs(ll, entry, list0, list1)
    debug = False #True
    if len(all_pairs) == 0:
#        print("No valid pairs.")
        #if pairList is empty then this was supposed to be the lead pair, so need [] for the 4vec too.
        if pairList == []:
            return [], []
        return []
    elif debug:
        print("All pairs: {}".format(str(all_pairs)))
    #sort these pairs enough to get the very best one.
   # all_pairs = bubble1(ll, entry, all_pairs)
    
    #if tt channel, make sure the highest pT tau comes first.
    if ll[0] == ll[1]:
        pt0, pt1 = 0., 0.
        if ll == 'tt':
            pt0 = entry.Tau_pt[all_pairs[0][0]]
            pt1 = entry.Tau_pt[all_pairs[0][1]]
        elif ll == 'mm':
            pt0 = entry.Muon_pt[all_pairs[0][0]]
            pt1 = entry.Muon_pt[all_pairs[0][1]]
        elif ll == 'ee':
            pt0 = entry.Electron_pt[all_pairs[0][0]]
            pt1 = entry.Electron_pt[all_pairs[0][1]]
        else:
            print("Error in getBestSubPair: unrecognized pairing {}.".format(ll))
        if pt1 > pt0:
            all_pairs[0][0], all_pairs[0][1] = all_pairs[0][1], all_pairs[0][0]
    #if this is the lead tau pair, we also need a Lorentz vector. 
    if pairList == []:
        vecs = []
        for i in range(2):
            vecs.append( get4vec(ll[i], entry, all_pairs[0][i]) )
        return vecs, all_pairs[0] 
    return all_pairs[0]

#return pairlist0 \cross pairlist1 (restricted to not overlap in dr)
# set allow_repeat to False in order to make sure only one pair2 of all the same particles is allowed.
def getAllPair2s(leps, ev, pairlist0, pairlist1, debug=False):
    pair2s = []
    
    #lepTypes to use just for getting the dR value
    # (use 2nd two bc mm is the only channel with no lt_dR cut in the yaml.)
    ll = leps[2:]
    #minimum dr between particles
    dr_cut = selections[ll]['lt_DR']
    if debug:
        print("ll: {}, dr_cut: {}".format(ll, dr_cut))

    #go through every possible pairing of the pairs
    for ii,pl0 in enumerate(pairlist0):
        for jj,pl1 in enumerate(pairlist1):
            #good unless any particles too close
            goodPair2 = True
            #form the pair2
            #check every combo of particles for dr spacing
            for aa,a in enumerate(pl0):
                if not goodPair2:
                    break
                for bb,b in enumerate(pl1):
                    #lep types of the particles
                    lt0 = leps[aa]
                    lt1 = leps[2 + bb]
                    #string concatenation
                    lt = lt0 + lt1
                    
                    #find the dR between a and b.
                   # print("leps={}, ii={},pl0={}, jj={},pl1={}, aa={},a={}, bb={},b={}, lt0={},lt1={},lt={}".format(leps,ii,pl0,jj,pl1,aa,a,bb,b,lt0,lt1,lt))
                    dr = find_dR(lt, ev, a, b)
                    if debug:
                        print("pl0={}, pl1={}, a={}, b={}, dr={}".format(pl0,pl1,a,b,dr))
                    #determine if dr is sufficient
                    #if dr < dr_cut:
                    if lt[0] == lt[1] and a == b:
                        goodPair2 = False
                        if debug:
                            print("Bad pair2 [{},{}]".format(pl0,pl1))
                        break
            if goodPair2:
                pair2s.append([pl0, pl1])
                if debug:
                    print("good pair2: [{},{}]".format(pl0,pl1))
                        
    return pair2s

#return the best 2 pairs (depending on the channels, either tt, et, or mt, or em, or mm, or ee).
# That is, the valid pairs with the highest scalar sum pT.
# Inputs lists should already be 'good', ie all individual
#  lepton cuts are already made (channel-specific pair cuts will be made here).
def getBestPairs(lepTypes, entry, pair2s, debug=False) :
    #debug = False
    #ok, now find the 2 best pairs, with the restriction that particles can't be too close to each other.
    #sort these pairs enough to get the very best one.
    all_pair2s = bubble2(lepTypes, entry, pair2s)
    if debug:
        print("all_pair2s: {}".format(all_pair2s))

    if len(lepTypes) != 4:
        print("Error: lepTypes should be 4 letters, one for each of the four leptons.")
        sys.exit()
    #if tt channel (or mm or ee) involved, make sure the highest pT tau comes first.
    #for each of the 2 pairs
    for ii in range(2):
        jj = ii*2
        #mm is the 2 leptons under current consideration.
        mm = lepTypes[jj:jj+2]
        if mm[0] == mm[1]:
            if debug:
                import generalFunctions as GF
                #setting isMC to false just so don't have to include another useless argument to this function
                GF.printEvent(entry, False)
                print("lepTypes={}, ii={},jj={},mm={}".format(lepTypes, ii, jj, mm))
            #array of pts for the two particles
            pts = [0., 0.]
            #get correct lepton type
            lname = lepname(mm[0])
            for kk in range(2):
                #get the pt of the kkth particle of the iith pair of the best pair-of-pairs
                exec("pts[kk] = entry.%s_pt[all_pair2s[0][ii][kk]]"%(lname))
            #if 2nd particle has more pt, then swap with first particle (just to keep it nice and orderly).
            if pts[1] > pts[0]:
                all_pair2s[0][ii][0], all_pair2s[0][ii][1] = all_pair2s[0][ii][1], all_pair2s[0][ii][0]

    #for the lead tau pair, we also need a Lorentz vector. 
    vecs = []
    for i in range(4):
        #for j in range(2):
        pairnum = i / 2 #pair 0 or pair 1
        partnum = i % 2 #particle 0 or 1 within that pair
        vecs.append( get4vec(lepTypes[i], entry, all_pair2s[0][pairnum][partnum]) )
    return vecs, all_pair2s[0][0], all_pair2s[0][1]

#just like getBestPairs, but instead of using max pt, use min |diff in ip3d|
def getBestPairs_ip3d(lepTypes, entry, pair2s, debug=False) :
    #debug = False
    #ok, now find the 2 best pairs, with the restriction that particles can't be too close to each other.
    #sort these pairs enough to get the very best one.
    all_pair2s = bubble_ip3d(lepTypes, entry, pair2s)
    if debug:
        print("all_pair2s: {}".format(all_pair2s))

    if len(lepTypes) != 4:
        print("Error: lepTypes should be 4 letters, one for each of the four leptons.")
        sys.exit()
    #if tt channel (or mm or ee) involved, make sure the highest pT tau comes first.
    #for each of the 2 pairs
    for ii in range(2):
        jj = ii*2
        #mm is the 2 leptons under current consideration.
        mm = lepTypes[jj:jj+2]
        if mm[0] == mm[1]:
            if debug:
                import generalFunctions as GF
                #setting isMC to false just so don't have to include another useless argument to this function
                GF.printEvent(entry, False)
                print("lepTypes={}, ii={},jj={},mm={}".format(lepTypes, ii, jj, mm))
            #array of ip3ds for the two particles
            ip3ds = [0., 0.]
            #get correct lepton type
            lname = lepname(mm[0])
            for kk in range(2):
                #get the pt of the kkth particle of the iith pair of the best pair-of-pairs
                exec("ip3ds[kk] = entry.%s_ip3d[all_pair2s[0][ii][kk]]"%(lname))

    #for the lead tau pair, we also need a Lorentz vector. 
    vecs = []
    for i in range(4):
        #for j in range(2):
        pairnum = i / 2 #pair 0 or pair 1
        partnum = i % 2 #particle 0 or 1 within that pair
        vecs.append( get4vec(lepTypes[i], entry, all_pair2s[0][pairnum][partnum]) )
    return vecs, all_pair2s[0][0], all_pair2s[0][1]

#literally just print out info about why this cut was made.
def printCut(event, lepTypes, lepType, num, cutType, val):
    if lepType == 'e':
        lepType = "electron"
    elif lepType == 'm':
        lepType = "muon"
    elif lepType == 't':
        lepType = "tauon"
    print("      entry {}, lepTypes {}, {} {} failed {} cut: {}= {}".format(event, lepTypes, lepType, num, cutType, cutType, val))

#return True if the electron is good, False if it fails any cuts.
# lepTypes is the lepton flavor for each of the two particles, ie one of 'ee', 'em', 'et'.
def goodElectron_4mu(lepTypes, entry, j, printOn=False):
    if 'e' not in lepTypes:
        return False
    sel = selections[lepTypes]
    #if lepTypes is 'ee', we actually need to use the 'et' selections instead
    # (since 'ee' selections are really for prompt electrons, which we're not interested in for 4tau analysis.)
    #if lepTypes == 'ee':
    #    sel = selections['et']
    if entry.Electron_pt[j] < sel['ele_pt']:
        if printOn:
            printCut(entry.event, lepTypes, 'e', j, "pt", entry.Electron_pt[j])
        return False
    if sel['ele_ID'] and not entry.Electron_looseId[j] : 
        if printOn:
            printCut(entry.event, lepTypes, 'e', j, "looseId", entry.Electron_looseId[j])
        return False
    if abs(entry.Electron_eta[j]) > sel['ele_eta'] :
        if printOn:
            printCut(entry.event, lepTypes, 'e', j, "eta", entry.Electron_eta[j])
        return False
    if abs(entry.Electron_dxy[j]) > sel['ele_dxy'] :
        if printOn:
            printCut(entry.event, lepTypes, 'e', j, "dxy", entry.Electron_dxy[j])
        return False
    if abs(entry.Electron_dz[j]) > sel['ele_dz'] :
        if printOn:
            printCut(entry.event, lepTypes, 'e', j, "dz", entry.Electron_dz[j])
        return False
    if False and ord(entry.Electron_lostHits[j]) > sel['ele_lostHits']:
        if printOn:
            printCut(entry.event, lepTypes, 'e', j, "lostHits", entry.Electron_lostHits[j])
        return False 
    return True

#return True if the muon is good, False if it fails any cuts.
# lepTypes is the lepton flavor for each of the two particles, ie one of 'mm', 'em', 'mt'.
def goodMuon_4mu(lepTypes, entry, j, printOn=False):
    if 'm' not in lepTypes:
        return False
    sel = selections[lepTypes]
    #if lepTypes is 'ee', we actually need to use the 'et' selections instead
    # (since 'ee' selections are really for prompt electrons, which we're not interested in for 4tau analysis.)
    #if lepTypes == 'mm':
    #    sel = selections['mt']
    if entry.Muon_pt[j] < sel['mu_pt']:
        if printOn:
            printCut(entry.event, lepTypes, 'm', j, "pt", entry.Muon_pt[j])
        return False
    if abs(entry.Muon_eta[j]) > sel['mu_eta'] :
        if printOn:
            printCut(entry.event, lepTypes, 'm', j, "eta", entry.Muon_eta[j])
        return False
    if sel['mu_iso_f']: 
        try:
            #this is what it's called in nAOD
            iso = entry.Muon_pfRelIso04_all[j]
        except AttributeError:
            #this is what it's called in my new ntuples
            iso = entry.Muon_iso[j]

        if iso >  sel['mu_iso']: 
            if printOn:
                printCut(entry.event, lepTypes, 'm', j, "pfRelIso04", entry.Muon_pfRelIso04_all[j])
            return False
    if sel['mu_ID'] :
        if not (entry.Muon_mediumId[j] or entry.Muon_tightId[j]): 
            if printOn:
                printCut(entry.event, lepTypes, 'm', j, "med/tight muID", "{},{}".format(entry.Muon_mediumId[j], entry.Muon_tightId[j]))
            return False
    if sel['mu_ID'] and not entry.Muon_looseId[j] : 
        if printOn:
            printCut(entry.event, lepTypes, 'm', j, "loose muId", entry.Muon_loosId[j])
        return False
    if sel['mu_type'] :
        if not (entry.Muon_isGlobal[j] or entry.Muon_isTracker[j]) : 
            if printOn:
                printCut(entry.event, lepTypes, 'm', j, "muType global/tracker", "{},{}".format(entry.Muon_isGlobal[j], entry.Muon_isTracker[j]))
            return False
    if abs(entry.Muon_dxy[j]) > sel['mu_dxy'] :
        if printOn:
            printCut(entry.event, lepTypes, 'm', j, "dxy", entry.Muon_dxy[j])
        return False
    if abs(entry.Muon_dz[j]) > sel['mu_dz'] :
        if printOn:
            printCut(entry.event, lepTypes, 'm', j, "dz", entry.Muon_dz[j])
        return False
    #if it passed all the cuts, it's good!
    if sel['tight']:
        if not entry.Muon_tightId[j]:
            if printOn:
                printCut(entry.event, lepTypes, 'm', j, "tight muId", "{}".format(tightId[j])) 
            return False
    return True

#True if the specified tauon is valid, otherwise false.
def goodTau_4tau(lepTypes, entry, j, printOn=False) :
    
    if 't' not in lepTypes:
        return False
    sel = selections[lepTypes] # selections for H->tau(h)+tau(h)
    if printOn:
        print("lepTypes: %s, sel: %s"%(lepTypes, sel))
    # apply tau(h) selections 
    if entry.Tau_pt[j] < sel['tau_pt']: 
        if printOn: 
            printCut(entry.event, lepTypes, 't', j, "pt", entry.Tau_pt[j])
        return False
    if abs(entry.Tau_eta[j]) > sel['tau_eta']: 
        if printOn: 
            printCut(entry.event, lepTypes, 't', j, "eta", entry.Tau_eta[j])
        return False
    if abs(entry.Tau_dz[j]) > sel['tau_dz']: 
        if printOn: 
            printCut(entry.event, lepTypes, 't', j, "dz", entry.Tau_dz[j])
        return False
    if not entry.Tau_idDecayModeNewDMs[j]: 
        if printOn: 
            printCut(entry.event, lepTypes, 't', j, "idDecayModeNewDMs", entry.Tau_idDecayModeNewDMs[j])
        return False
    if  entry.Tau_decayMode[j] == 5 or entry.Tau_decayMode[j] == 6 : 
        if printOn: 
            printCut(entry.event, lepTypes, 't', j, "decayMode", entry.Tau_decayMode[j])
        return False
#    if abs(entry.Tau_charge[j]) != 1: 
#        if printOn: 
#            printCut(entry.event, lepTypes, 't', j, "charge", entry.Tau_decayMode[j]))
#        return False
    if sel['tau_vJet'] > 0  and not ord(entry.Tau_idDeepTau2017v2p1VSjet[j]) & sel['tau_vJet'] > 0 :
        if printOn : 
            printCut(entry.event, lepTypes, 't', j, "vJetIDDeepTau", ord(entry.Tau_idDeepTau2017v2p1VSjet[j]))
        return False
    if sel['tau_vEle'] > 0 and not ord(entry.Tau_idDeepTau2017v2p1VSe[j]) :
        if printOn : 
            printCut(entry.event, lepTypes, 't', j, "vEleIDDeepTau", ord(entry.Tau_idDeepTau2017v2p1VSe[j]))
        return False
    if sel['tau_vMu'] > 0 and not ord(entry.Tau_idDeepTau2017v2p1VSmu[j]) :
        if printOn : 
            printCut(entry.event, lepTypes, 't', j, "vMuIDDeepTau", ord(entry.Tau_idDeepTau2017v2p1VSmu[j]))
        return False

    return True

#for 4tau analysis, return the 4 lists (one for each flavor of particle in lepTypes).
def getGoodLists(lepTypes, entry, printOn=False):
    #one list for each of the lepton types
    lists = [[] for i in range(4)]
    for i in range(4):
        #don't repeat if it's the same lepton type as its partner.
        #if (i == 1 or i == 3) and lepTypes[i] == lepTypes[i-1]:
        if (i > 0 and lepTypes[i] == lepTypes[i-1]):
            lists[i] = lists[i-1]
            continue
        #first get the current pair
        lt = lepTypes[:2]
        if i > 1:
            lt = lepTypes[2:]
        #now get the correct lepton name.
        lname = lepname(lepTypes[i])
        #now get number of particles of this type
        exec("npart = entry.n%s"%(lname))
        #and finally form the list.
        for j in range(npart):
            #app will be true if we should append this particle; else false.
            exec("app = good%s_4mu(lt, entry, j, printOn)"%(lname))
            if app:
                lists[i].append(j)

    return lists #lists[0], lists[1]

def catToNumber(cat) :
    number = { 'eeet':1, 'eemt':2, 'eett':3, 'eeem':4, 'mmet':5, 'mmmt':6, 'mmtt':7, 'mmem':8, 'et':9, 'mt':10, 'tt':11, 'tttt':12, 'ttmt':13, 'ttet':14, 'ttem':15, 'mtmt':16, 'mtet':17, 'mtem':18, 'etet':19, 'etem':20, 'emem':21, 'mmmm':22 }
    return number[cat]


def numberToCat(number) :
    cat = { 1:'eeet', 2:'eemt', 3:'eett', 4:'eeem', 5:'mmet', 6:'mmmt', 7:'mmtt', 8:'mmem', 9:'et', 10:'mt', 11:'tt', 12:'tttt', 13:'ttmt', 14:'ttet', 15:'ttem', 16:'mtmt', 17:'mtet', 18:'mtem', 19:'etet', 20:'etem', 21:'emem', 22:'mmmm' }
    return cat[number]

def findAMother(entry,motherType,daughter):
    try:
        MotherIdx = entry.GenPart_genPartIdxMother[daughter]
    except:
        print "Catch error at findAMother ",sys.exc_info()[0]
        return -1
    #print "daughter index",daughter
    #print "mother index",MotherIdx
    if MotherIdx==-1:
        return -1
    if abs(entry.GenPart_pdgId[MotherIdx])==motherType:
        print "found the right mother",MotherIdx
        return  MotherIdx
    else:
        return findAMother(entry,motherType,MotherIdx) #case where we need the grandma... muons that radiate gammas are two generations...
        #return None 

def main():
    #just to run a test of the functions above.

    import generalFunctions as GF
    f = TFile.Open("inFile.root")
    t = f.Get("Events")

    cat = 'ttmt'
    print("total nevents: {}".format(t.GetEntries()))
    for i,e in enumerate(t):
        GF.printEvent(e, True)
        glists = getGoodLists(cat, e, False)
       # print("glists: {}".format(glists))        
        ap0 = getAllPairs(cat[:2], e, glists[0], glists[1])
        ap1 = getAllPairs(cat[2:], e, glists[2], glists[3])
       # print("ap0: {}".format(ap0))
       # print("ap1: {}".format(ap1))
        ap2s = getAllPair2s(cat, e, ap0, ap1)
        if ap2s != []: 
    #        print("ap2s: {}".format(ap2s))
            ap2s = bubble2(cat, e, ap2s)
            print("sorted ap2s: {}".format(ap2s))
            if len(ap2s) > 1:
                print("more than one valid pair of pairs!! i={}".format(i))
              #  break
            vecs, pair0, pair1 = getBestPairs(cat, e, glists)
            print("vecs={}, pair0={}, pair1={}".format(vecs, pair0, pair1))
        #if i > 1000: break

if __name__ == "__main__":
    main()
