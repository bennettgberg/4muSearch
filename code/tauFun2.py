# !/usr/bin/env python

""" tauFun.py: apply selection sequence to four-lepton final state """

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
with io.open('cuts_HAA.yaml', 'r') as stream:
    selections = yaml.load(stream)
print "Using selections:\n", selections

#returns the list of muon trigger paths for the given year.
def muonTriggers_4tau(year):
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

#returns list of electron trigger paths for the given year.
def electronTriggers_4tau(year):
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
def tauTriggers_4tau(year):
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
def goodTrigger_4tau(e, year, debug=False):
    printOn = debug

    muonTrigs = muonTriggers_4tau(year)
    electronTrigs = electronTriggers_4tau(year)
    tauTrigs = tauTriggers_4tau(year)

    goodmuon = False
    goodelectron = False
    goodtau = False
    for p in ["muon", "electron", "tau"]:
        exec("trigs = %sTrigs"%(p))
        for t in trigs:
            if printOn:
                print("trigger: {}".format(t))
            try:
                exec("passed = e.%s"%(t))
            except AttributeError:
                passed = False
            if passed:
                exec("good%s = True"%(p))

    return goodmuon or goodelectron or goodtau
                

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



def getTauList(channel, entry, pairList=[],printOn=False, isTight=True) :
    """ tauFun.getTauList(): return a list of taus that
                             pass the basic selection cuts
    """

    if not channel in ['mmtt','eett'] :
        print("Warning: invalid channel={0:s} in tauFun.getTauList()".format(channel))
        exit()

    if printOn : print ' getTauList : will be checking nTau', entry.nTau

    if entry.nTau == 0:
        if printOn : print ' failed nTau', entry.nTau
        return []

    tauList = []
    tt = selections['tt'] # selections for H->tau(h)+tau(h)
    for j in range(entry.nTau):
        #print entry.Tau_pt[j]
        # apply tau(h) selections
        if printOn : print 'looking for Tau j', j, 'Q', entry.Tau_charge[j]
        if entry.Tau_pt[j] < tt['tau_pt']:
            if printOn : print("        fail Tau pT {0:f}".format(entry.Tau_pt[j]))
            continue
        if abs(entry.Tau_eta[j]) > tt['tau_eta']:

            if printOn : print("        fail Tau eta {0:f}".format(abs(entry.Tau_eta[j])))
            continue
        if abs(entry.Tau_dz[j]) > tt['tau_dz']:
            if printOn : print("        fail Tau dZ {0:f}".format(entry.Tau_dz[j]))
            continue
        if not entry.Tau_idDecayModeNewDMs[j]:
            if printOn : print("        fail Tau decayModeNewDM {0:f}".format(entry.Tau_idDecayModeNewDMs[j]))
            continue
        if  entry.Tau_decayMode[j] == 5 or entry.Tau_decayMode[j] == 6 :
            if printOn : print("        fail Tau decayMode {0:f}".format(entry.Tau_decayMode[j]))
            continue
        if abs(entry.Tau_charge[j]) != 1:
            if printOn : print("        fail Tau Q {0:d}".format(entry.Tau_charge[j]))
            continue

        if tt['tau_vJet'] > 0  and not ord(entry.Tau_idDeepTau2017v2p1VSjet[j]) & tt['tau_vJet'] > 0 :
            if printOn : print("        fail DeepTau vs. Jet={0:d}".format(ord(entry.Tau_idDeepTau2017v2p1VSjet[j])))
            continue
        if tt['tau_vEle'] > 0 and not ord(entry.Tau_idDeepTau2017v2p1VSe[j]) & tt['tau_vEle'] > 0 :
            if printOn : print("        fail DeepTau vs. ele={0:d}".format(ord(entry.Tau_idDeepTau2017v2p1VSe[j])))
            continue
        if tt['tau_vMu'] > 0 and not ord(entry.Tau_idDeepTau2017v2p1VSmu[j]) & tt['tau_vMu'] > 0 :
            if printOn : print("        fail DeepTau vs.  mu={0:d}".format(ord(entry.Tau_idDeepTau2017v2p1VSmu[j])))
            continue

        eta, phi = entry.Tau_eta[j], entry.Tau_phi[j]
        DR0, DR1 =  lTauDR(eta,phi, pairList[0]), lTauDR(eta,phi,pairList[1])
        if isTight :
            if DR0 < tt['tt_DR'] or DR1 < tt['tt_DR']:

                if printOn : print("        fail DR0={0:f} or DR1={1:f}". format(DR0, DR1))
                continue
        tauList.append(j)
        #print ord(entry.Tau_idDeepTau2017v2p1VSmu[j]), ord(entry.Tau_idDeepTau2017v2p1VSe[j]), ord(entry.Tau_idDeepTau2017v2p1VSjet[j])

    if printOn  : print 'returning with tauList from getTauList', tauList
    return tauList



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



def tauDR(entry, j1,j2) :
    if j1 == j2 : return 0.
    phi1, eta1, phi2, eta2 = entry.Tau_phi[j1], entry.Tau_eta[j1], entry.Tau_phi[j2], entry.Tau_eta[j2]
    return sqrt( (phi2-phi1)**2 + (eta2-eta1)**2 )


def lTauDR(eta1,phi1,Lep) :
    phi2, eta2 = Lep.Phi(), Lep.Eta()
    dPhi = min(abs(phi2-phi1),2.*pi-abs(phi2-phi1))
    return sqrt(dPhi**2 + (eta2-eta1)**2)


def DRobj(eta1,phi1,eta2,phi2) :
    dPhi = min(abs(phi2-phi1),2.*pi-abs(phi2-phi1))
    return sqrt(dPhi**2 + (eta2-eta1)**2)

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

def comparePair(entry, pair1, pair2) :
    """ tauFun.comparePair.py: return true if pair2 is
                               better than pair1
    """

    j1, j2 = pair1[0], pair2[0] # look at leading pt tau in each pair
    j3, j4 = pair1[1], pair2[1] # look at leading pt tau in each pair
    if entry.Tau_rawDeepTau2017v2p1VSjet[j2] > entry.Tau_rawDeepTau2017v2p1VSjet[j1] :
        return True
    if  entry.Tau_rawDeepTau2017v2p1VSjet[j2] < entry.Tau_rawDeepTau2017v2p1VSjet[j1] :
        return False
    if  entry.Tau_rawDeepTau2017v2p1VSjet[j2] == entry.Tau_rawDeepTau2017v2p1VSjet[j1] :
        if entry.Tau_pt[j2] > entry.Tau_pt[j1] :
            return True
        if entry.Tau_pt[j2] < entry.Tau_pt[j1] :
            return False
        if entry.Tau_pt[j2] == entry.Tau_pt[j1] :
            if  entry.Tau_rawDeepTau2017v2p1VSjet[j4] > entry.Tau_rawDeepTau2017v2p1VSjet[j3] :
                return True
            if  entry.Tau_rawDeepTau2017v2p1VSjet[j4] < entry.Tau_rawDeepTau2017v2p1VSjet[j3] :
                return False
            if  entry.Tau_rawDeepTau2017v2p1VSjet[j4] == entry.Tau_rawDeepTau2017v2p1VSjet[j3] :
                if entry.Tau_pt[j4] > entry.Tau_pt[j3] : return True
                if entry.Tau_pt[j4] < entry.Tau_pt[j3] : return False
                if entry.Tau_pt[j4] == entry.Tau_pt[j3] : return False

    # do it once more swapping the tau pairs
    j1, j2 = pair1[1], pair2[1] # look at leading pt tau in each pair
    j3, j4 = pair1[0], pair2[0] # look at leading pt tau in each pair
    if entry.Tau_rawDeepTau2017v2p1VSjet[j2] > entry.Tau_rawDeepTau2017v2p1VSjet[j1] :
        return True
    if  entry.Tau_rawDeepTau2017v2p1VSjet[j2] < entry.Tau_rawDeepTau2017v2p1VSjet[j1] :
        return False
    if  entry.Tau_rawDeepTau2017v2p1VSjet[j2] == entry.Tau_rawDeepTau2017v2p1VSjet[j1] :
        if entry.Tau_pt[j2] > entry.Tau_pt[j1] :
            return True
        if entry.Tau_pt[j2] < entry.Tau_pt[j1] :
            return False
        if entry.Tau_pt[j2] == entry.Tau_pt[j1] :
            if  entry.Tau_rawDeepTau2017v2p1VSjet[j4] > entry.Tau_rawDeepTau2017v2p1VSjet[j3] :
                return True
            if  entry.Tau_rawDeepTau2017v2p1VSjet[j4] < entry.Tau_rawDeepTau2017v2p1VSjet[j3] :
                return False
            if  entry.Tau_rawDeepTau2017v2p1VSjet[j4] == entry.Tau_rawDeepTau2017v2p1VSjet[j3] :
                if entry.Tau_pt[j4] > entry.Tau_pt[j3] : return True
                if entry.Tau_pt[j4] < entry.Tau_pt[j3] : return False
                if entry.Tau_pt[j4] == entry.Tau_pt[j3] : return False



def getBestTauPair(channel, entry, tauList,printOn=False) :
    """ tauFun.getBestTauPair(): return two taus that
                                 best represent H->tt
    """

    if not channel in ['mmtt','eett'] :
        if printOn : print("Invalid channel={0:s} in tauFun.getBestTauPair()".format(channel))
        exit()

    if len(tauList) < 2:
        if printOn : print 'failed to find good TauTau Pair'
        if printOn : print("Entering getTauPairs failing nTauList={0:s}".format(tauList))
        return []

    # form all possible pairs that satisfy DR requirement
    tauPairList = []
    tt = selections['tt'] # selections for H->(tau_h)(tau_h)
    for i in range(len(tauList)) :
        idx_tau1 = tauList[i]
        for j in range(len(tauList)) :
            if i == j: continue
            idx_tau2 = tauList[j]
            if tauDR(entry, idx_tau1, idx_tau2) < tt['tt_DR'] :
                tdR= tauDR(entry, idx_tau1, idx_tau2) < tt['tt_DR']
                if printOn : print "failed tDR=",tdR, "tt_DR =", tt['tt_DR']
                continue
            #tauPairList.append([idx_tau1, idx_tau2])
            if idx_tau1 not in tauPairList : tauPairList.append(idx_tau1)
            if idx_tau2 not in tauPairList : tauPairList.append(idx_tau2)


    if len(tauPairList) == 0 :
        if printOn : print 'fail tauPairList =0'
        return []

    c = set(combinations(tauPairList, 2))
    if printOn : print 'these are the combinations', c, 'from', tauPairList
    tauPairList=list(c)

    if printOn : print 'Do I need to do the comparePair ? ', len(tauPairList),  tauPairList

    maxI= comparePairvspT(entry, tauPairList, printOn)
    tauPairList=tauPairList[maxI]

    if printOn : print 'this is the list of sums', maxI, tauPairList, tauPairList[0], tauPairList[1]

    idx_tau1, idx_tau2 = tauPairList[0], tauPairList[1]
    if entry.Tau_pt[idx_tau2] > entry.Tau_pt[idx_tau1] :
        if printOn : print 'Sorting tt tauPair', entry.Tau_pt[idx_tau2], entry.Tau_pt[idx_tau1], idx_tau2, idx_tau1
        tauPairList = {}
        tauPairList[0] = idx_tau2
        tauPairList[1] = idx_tau1

    if printOn : print 'returning tt tauPairList', tauPairList
    return tauPairList


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

    all_pairs = []
    for a in list0:
        for b in list1:
            #don't repeat twice for same lep type, eg [0,1] and [1,0]
            if lepTypes[0] == lepTypes[1] and b <= a:
                continue
            #find the dR between these two particles.
            dr = find_dR(lepTypes, entry, a, b)
            #determine if dr is sufficient
            if dr < dr_cut:
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

#partially sort list 'items' so that only the first item is in the right place.
def bubble2(lepTypes, entry, items):
    # Sort the list of pairs-of-pairs using a bubble sort
    # The list is not fully sorted, since only the top pair-of-pairing is needed
    for i in range(len(items)-1,0,-1) :
        #corrected 2020/07/20
        if not comparePair2(entry, items[i], items[i-1], lepTypes) : 
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
        mlep = .0005
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
    #get the 2 lists of particles
#    plist = [[],[]]
#    for i in range(2):
#        if ll[i] == 't':
#            plist[i] = tList
#        elif ll[i] == 'm':
#            plist[i] = mList
#        elif ll[i] == 'e':
#            plist[i] = eList
#        else:
#            print("Error: unrecognized pairing {}".format(lepTypes))
#            return []
    #get all valid pairs with these 2 lists
    #all_pairs = getAllPairs(ll, entry, plist[0], plist[1], pairList)
#    print("getBestPair ll: {}".format(ll))
    all_pairs = getAllPairs(ll, entry, list0, list1, pairList)
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
def getAllPair2s(leps, ev, pairlist0, pairlist1,debug=False):
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
                    if dr < dr_cut:
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

    #if tt channel (or mm or ee) involved, make sure the highest pT tau comes first.
    #for each of the 2 pairs
    for ii in range(2):
        jj = ii*2
        #mm is the 2 leptons under current consideration.
        mm = lepTypes[jj:jj+2]
        if mm[0] == mm[1]:
            if debug:
                import generalFunctions as GF
                GF.printEvent(entry)
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
    for i in range(2):
        vecs.append( get4vec(lepTypes[i], entry, all_pair2s[0][0][i]) )
    return vecs, all_pair2s[0][0], all_pair2s[0][1]

def getBestTauPairPt(channel, entry, tauList) :
    """ tauFun.getBestTauPair(): return two taus that 
                                 best represent H->tt
    """ 

    if not channel in ['mmtt','eett', 'tttt'] : 
        print("Invalid channel={0:s} in tauFun.getBestTauPair()".format(channel))
        exit()

    if len(tauList) < 2: return [] 
    
    # form all possible pairs that satisfy DR requirement
    tauPairList = []
    tt = selections['tt'] # selections for H->(tau_h)(tau_h)
    for i in range(len(tauList)) :
        idx_tau1 = tauList[i]
        for j in range(len(tauList)) :
            if i == j: continue
            idx_tau2 = tauList[j]
            if tauDR(entry, idx_tau1, idx_tau2) < tt['tt_DR'] : continue
            tauPairList.append([idx_tau1, idx_tau2])

    # Sort the pair list using a bubble sort
    # The list is not fully sorted, since only the top pairing is needed
    for i in range(len(tauPairList)-1,0,-1) :
        #corrected 2020/07/20
        if not comparePairPt(entry, tauPairList[i],tauPairList[i-1]) : 
            tauPairList[i-1], tauPairList[i] = tauPairList[i], tauPairList[i-1] 

    if len(tauPairList) == 0 : return []
    #placing the lead first
    idx_tau1, idx_tau2 = tauPairList[0][0], tauPairList[0][1]
    if entry.Tau_pt[idx_tau2] > entry.Tau_pt[idx_tau1] : 
        temp = tauPairList[0][0]
        tauPairList[0][0] = tauPairList[0][1]
        tauPairList[0][1] = temp
        
    return tauPairList[0]


def getMuTauPairs(entry,cat='mt',pairList=[],printOn=False) :
    """  tauFun.getMuTauPairs.py: return list of acceptable pairs
                                 of muons and taus
    """

    if entry.nMuon < 1 or entry.nTau < 1:
        if printOn : print("Entering getMuTauPairs failing nMuon={0:d} nTau={1:d}".format(entry.nMuon,entry.nTau))
        return []
    if cat == 'mmmt' and entry.nMuon < 3: return []

    muTauPairs = []
    mt = selections['mt'] # H->tau(mu)+tau(h) selections
    if printOn : print("Entering tauFun.getMuTauPairs() nMuon={0:d} nTau={1:d}".format(entry.nMuon,entry.nTau))
    for i in range(entry.nMuon):

        # apply tau(mu) selections
        if mt['mu_type']:
            if not (entry.Muon_isGlobal[i] or entry.Muon_isTracker[i]) :
                if printOn : print("    fail mu_type Global or Tracker={0}".format(entry.Muon_isGlobal[i]))
                continue
        if mt['mu_ID']:
            if not (entry.Muon_mediumId[i] or entry.Muon_tightId[i]) :
                if printOn : print("    fail mu_ID mediumId={0}".format(entry.Muon_mediumId[i]))
                continue
        if abs(entry.Muon_dxy[i]) > mt['mu_dxy']:
            if printOn : print("    fail mu_dxy={0:f}".format(entry.Muon_dxy[i]))
            continue
        if abs(entry.Muon_dz[i]) > mt['mu_dz']:
            if printOn : print("    fail mu_dz={0:f}".format(entry.Muon_dz[i]))
            continue
        mu_eta, mu_phi = entry.Muon_eta[i], entry.Muon_phi[i]
        if entry.Muon_pt[i] < mt['mu_pt']:
            if printOn : print("    fail mu_pt={0:f}".format(entry.Muon_pt[i]))
            continue
        if abs(mu_eta) > mt['mu_eta']:
            if printOn : print("    fail mu_eta={0:f}".format(entry.Muon_eta[i]))
            continue
        if  mt['mu_iso_f'] and entry.Muon_pfRelIso04_all[i] > mt['mu_iso']:
            if printOn : print("    fail mu_iso={0:f}".format(entry.Muon_pfRelIso04_all[i]))
            continue

        DR0 = lTauDR(mu_eta,mu_phi,pairList[0]) # l1 vs. tau(mu)
        DR1 = lTauDR(mu_eta,mu_phi,pairList[1]) # l2 vs. tau(mu)
        if DR0 < mt['ll_DR'] or DR1 < mt['ll_DR']:
            if printOn : print("    fail muon DR  DR0={0:f} DR1={1:f} for muon={2:s} vs 0.pT={3:f} vs 1.pT={4:f}".format(DR0,DR1, str(i), pairList[0].Pt(), pairList[1].Pt()))
            continue
        if printOn : print("    Good muon i={0:d}".format(i))

        for j in range(entry.nTau):

            # apply tau(h) selections
            if printOn : print("        tau j={0:d}".format(j))
            if abs(entry.Tau_eta[j]) > mt['tau_eta']:
                if printOn : print("        fail tau eta={0:f}".format(entry.Tau_eta[j]))
                continue
            if entry.Tau_pt[j] < mt['tau_pt']:
                if printOn : print("        fail tau  pt={0:f}".format(entry.Tau_pt[j]))
                continue
            if abs(entry.Tau_dz[j]) > mt['tau_dz']:
                if printOn : print("        fail tau  dz={0:f}".format(entry.Tau_dz[j]))
                continue
            if mt['tau_ID']:
                if not entry.Tau_idDecayModeNewDMs[j]:
                    if printOn : print("        fail tau idDecayModeNewDMs={0}".format(entry.Tau_idDecayModeNewDMs[j]))
                    continue
            if  mt['tau_decayMode'] and (entry.Tau_decayMode[j] == 5 or entry.Tau_decayMode[j] == 6) :
                if printOn : print("        fail tau decayMode={0:d}".format(entry.Tau_decayMode[j]))
                continue

            ''' # this is the old (pre-DeepTau) selection
            if ord(entry.Tau_idAntiMu[j]) <= mt['tau_antiMu']: continue
            if ord(entry.Tau_idAntiEle[j]) <= mt['tau_antiEle']: continue
            if cat == 'eemt':
                if ord(entry.Tau_idAntiMu[j]) < mt['tau_eemt_antiMu']: continue
            '''

            if mt['tau_vJet'] > 0  and not ord(entry.Tau_idDeepTau2017v2p1VSjet[j]) & mt['tau_vJet'] > 0 :
                if printOn : print("        fail DeepTau vs. Jet={0:d}".format(ord(entry.Tau_idDeepTau2017v2p1VSjet[j])))
                continue
            if mt['tau_vEle'] > 0 and not ord(entry.Tau_idDeepTau2017v2p1VSe[j]) & mt['tau_vEle'] > 0 :
                if printOn : print("        fail DeepTau vs. ele={0:d}".format(ord(entry.Tau_idDeepTau2017v2p1VSe[j])))
                continue
            if mt['tau_vMu'] > 0 and not ord(entry.Tau_idDeepTau2017v2p1VSmu[j]) & mt['tau_vMu'] > 0 :
                if printOn : print("        fail DeepTau vs.  mu={0:d}".format(ord(entry.Tau_idDeepTau2017v2p1VSmu[j])))
                continue

            tau_eta, tau_phi = entry.Tau_eta[j], entry.Tau_phi[j]
            dPhi = min(abs(tau_phi-mu_phi),2.*pi-abs(tau_phi-mu_phi))
            DR = sqrt(dPhi**2 + (tau_eta-mu_eta)**2) # tau(mu) vs. tau(h)
            if DR < mt['mt_DR']:
                if printOn : print("        fail mtDR DR={0:f} for tau={1:d}".format(DR, j))
                continue
            DR0 = lTauDR(tau_eta, tau_phi, pairList[0]) #l1 vs. tau(h)
            DR1 = lTauDR(tau_eta, tau_phi, pairList[1]) #l2 vs. tau(h)
            if DR0 < mt['mt_DR'] or DR1 < mt['mt_DR']:
                if printOn : print("        fail DR  DR0={0:f} DR1={1:f} for tau={2:i}, mu={3:d}".format(DR0,DR1, j ))
                continue
            if printOn: print("        Tau j={0:d} passes all cuts.".format(j))
            muTauPairs.append([i,j])

    return muTauPairs


def compareMuTauPair(entry,pair1,pair2) :
    # a return value of True means that pair2 is "better" than pair 1
    i1, i2, j1, j2 = pair1[0], pair2[0], pair1[1], pair2[1]
    if entry.Muon_pfRelIso04_all[i2]  <  entry.Muon_pfRelIso04_all[i1] : return True
    if entry.Muon_pfRelIso04_all[i2] ==  entry.Muon_pfRelIso04_all[i1] :
        if entry.Muon_pt[i2] >  entry.Muon_pt[i1] : return True
        if entry.Muon_pt[i2] == entry.Muon_pt[i1] :
            if entry.Tau_rawDeepTau2017v2p1VSjet[j2] > entry.Tau_rawDeepTau2017v2p1VSjet[j1] : return True
            if entry.Tau_rawDeepTau2017v2p1VSjet[j2] == entry.Tau_rawDeepTau2017v2p1VSjet[j1] :
                if entry.Tau_pt[j2] > entry.Tau_pt[j1] : return True

    return False

def compareMuTauPairvspT(entry,tauPairList, printOn=False) :

    SumList=[]
    for i in range(0,len(tauPairList)) :

        j1, j2 = tauPairList[i][0], tauPairList[i][1] # look at leading pt tau in each pair
        if printOn : print 'appending now', entry.Muon_pt[j1] + entry.Tau_pt[j2], j1, j2, tauPairList[i]
        SumList.append(entry.Muon_pt[j1] + entry.Tau_pt[j2])

    maxI=SumList.index(max(SumList))

    return maxI


def getBestMuTauPair(entry,cat='mt',pairList=[],printOn=False) :

    # form all possible pairs that satisfy DR requirement
    if printOn : print("Entering getBestMuTauPair()")
    tauPairList = getMuTauPairs(entry,cat=cat,pairList=pairList,printOn=printOn)


    if len(tauPairList) == 0 :
        if printOn : print 'failed to find good MuTau Pair', cat
        return []


    maxI= compareMuTauPairvspT(entry, tauPairList, printOn)
    tauPairList=tauPairList[maxI]

    return tauPairList


def getEMuTauPairs(entry,cat='em',pairList=[],printOn=False) :
    """ tauFun.getEMuTauPairs(): returns a list of suitable
                                 H-> tau(mu) + tau(ele) cands
    """

    if printOn : print("Entering getEMuTauPairs() nMuon={0:d} nElectron={1:d}".format(entry.nMuon,entry.nElectron))
    if entry.nMuon < 1 or entry.nElectron < 1: return []
    if cat == 'mmem' and entry.nMuon < 3:      return []
    if cat == 'eeem' and entry.nElectron < 3:  return []

    elmuTauPairs = []
    em = selections['em'] # selections for H->tau(ele)+tau(mu)
    for i in range(entry.nMuon):

        # selections for tau(mu)
        if printOn : print("Muon i={0:d}".format(i))
        if em['mu_ID']:
            if not (entry.Muon_mediumId[i] or entry.Muon_tightId[i]) :
                if printOn : print("    failed muID={0}".format(entry.Muon_mediumId[i]))
                continue

        if em['mu_type']:
            if not (entry.Muon_isGlobal[i] or entry.Muon_isTracker[i]) :
                if printOn : print("    fail mu_type Global or Tracker={0}".format(entry.Muon_isGlobal[i]))
                continue
        if abs(entry.Muon_dxy[i]) > em['mu_dxy']:
            if printOn : print("    failed dxy={0:f}".format(entry.Muon_dxy[i]))
            continue
        if abs(entry.Muon_dz[i]) > em['mu_dz']:
            if printOn : print("    failed dz={0:f}".format(entry.Muon_dz[i]))
            continue
        mu_eta, mu_phi = entry.Muon_eta[i], entry.Muon_phi[i]
        if entry.Muon_pt[i] < em['mu_pt']:
            if printOn : print("    failed pt={0:f}".format(entry.Muon_pt[i]))
            continue
        if abs(mu_eta) > em['mu_eta']:
            if printOn : print("    failed eta={0:f}".format(entry.Muon_eta[i]))
            continue
        if em['mu_iso_f'] and entry.Muon_pfRelIso04_all[i] > em['mu_iso']:
            if printOn : print("    failed iso={0:f}".format(entry.Muon_pfRelIso04_all[i]))
            continue

        DR0 = lTauDR(mu_eta,mu_phi,pairList[0]) #l1 vs. tau(mu)
        DR1 = lTauDR(mu_eta,mu_phi,pairList[1]) #l2 vs. tau(mu)
        if DR0 < em['ll_DR'] or DR1 < em['ll_DR']:
            if printOn : print("    failed DR  DR0={0:f} DR1={1:f}".format(DR0,DR1))
            continue

        for j in range(entry.nElectron):

            # selections for tau(ele)
            if printOn: print("    electron={0:d}".format(j))
            if abs(entry.Electron_dxy[j]) > em['ele_dxy']:
                if printOn : print("        failed dxy={0:f}".format(entry.Electron_dxy[j]))
                continue
            if abs(entry.Electron_dz[j]) > em['ele_dz']:
                if printOn : print("        failed dz={0:f}".format(entry.Electron_dz[j]))
                continue
            ele_eta, ele_phi = entry.Electron_eta[j], entry.Electron_phi[j]
            if entry.Electron_pt[j] < em['ele_pt']:
                if printOn : print("        failed pt={0:f}".format(entry.Electron_pt[j]))
                continue
            if abs(ele_eta) > em['ele_eta']:
                if printOn : print("        failed eta={0:f}".format(entry.Electron_eta[j]))
                continue
            if ord(entry.Electron_lostHits[j]) > em['ele_lostHits']:
                if printOn : print("        failed lost hits={0:d}".format(entry.Electron_lostHits[j]))
                continue
            if em['ele_convVeto']:
                if not entry.Electron_convVeto[j]:
                    if printOn : print("        failed conv. veto={0}".format(entry.Electron_convVeto[j]))
                    continue
            if em['ele_ID']:
                if not entry.Electron_mvaFall17V2noIso_WP90[j]:
                    if printOn : print("        failed mvaWP90={0}".format(entry.entry.Electron_mvaFall17V2noIso_WP90[j]))
                    continue
            if em['ele_iso_f'] and entry.Electron_pfRelIso03_all[j] > em['ele_iso']:
                if printOn : print("        failed iso={0:f}".format(entry.Electron_pfRelIso03_all[j]))
                continue

            dPhi = min(abs(mu_phi-ele_phi),2.*pi-abs(mu_phi-ele_phi))
            DR = sqrt(dPhi**2 + (mu_eta-ele_eta)**2) # tau(mu) vs. tau(ele)
            if DR < em['em_DR']:
                if printOn : print("        failed emDR={0:f}".format(DR))
                continue
            DR0 = lTauDR(ele_eta,ele_phi,pairList[0]) # l1 vs. tau(ele)
            DR1 = lTauDR(ele_eta,ele_phi,pairList[1]) # l2 vs. tau(ele)
            if DR0 < em['ll_DR'] or DR1 < em['ll_DR']:
                if printOn : print("        failed ltDR DR0={0:f} DR1={1:f}".format(DR0,DR1))
                continue
            if printOn : print("        found a good pair i={0:i}, j={1:i}".format(i,j))
            elmuTauPairs.append([j,i])

    return elmuTauPairs

def getMuMuPairs(entry, cat='mm', pairList=[], printOn=False):

    if entry.nMuon < 2:
        if printOn: print ("Entering getMuMuPairs, failing nMuon={0:d}".format(entry.nMuon))
        return []
    if cat == 'mmmm' and entry.nMuon < 4: return []

    if printOn: print("Entering tauFun.getMuMuPairs() nMuon={0:d}".format(entry.nMuon))

    mm = selections['mt'] # inherit selections for tau(mu)
    selected_muons = []
    for i in range(entry.nMuon):

        if mm['mu_type']:
            if not (entry.Muon_isGlobal[i] or entry.Muon_isTracker[i]) :
                if printOn: print("\t fail mu_type Global or Tracker={0}".format(entry.Muon_isGlobal[i]))
                continue
        if mm['mu_ID']:
            if not (entry.Muon_mediumId[i] or entry.Muon_tightId[i]) :
                if printOn: print("\t fail mu_ID mediumId={0}".format(entry.Muon_mediumId[i]))
                continue
        if abs(entry.Muon_dxy[i]) > mm['mu_dxy']:
            if printOn: print("\t fail mu_dxy={0:f}".format(entry.Muon_dxy[i]))
            continue
        if abs(entry.Muon_dz[i]) > mm['mu_dz']:
            if printOn: print("\t fail mu_dz={0:f}".format(entry.Muon_dz[i]))
            continue

        mu_eta, mu_phi = entry.Muon_eta[i], entry.Muon_phi[i]
        if entry.Muon_pt[i] < mm['mu_pt']:
            if printOn: print("\t fail mu_pt={0:f}".format(entry.Muon_pt[i]))
            continue
        if abs(mu_eta) > mm['mu_eta']:
            if printOn: print("\t fail mu_eta={0:f}".format(entry.Muon_eta[i]))
            continue
        if  mm['mu_iso_f'] and entry.Muon_pfRelIso04_all[i] > mm['mu_iso']:
            if printOn: print("\t fail mu_iso={0:f}".format(entry.Muon_pfRelIso04_all[i]))
            continue

        DR0 = lTauDR(mu_eta,mu_phi,pairList[0]) # l1 vs. m
        DR1 = lTauDR(mu_eta,mu_phi,pairList[1]) # l2 vs. m
        if DR0 < mm['ll_DR'] or DR1 < mm['ll_DR']:
            if printOn : print("\t fail muon DR  DR0={0:f} DR1={1:f}".format(DR0,DR1))
            continue
        if printOn : print("\t Good muon i={0:d}".format(i))

        selected_muons.append(i)

    # pair up the selected muons
    mm_pairs = []
    for i in selected_muons:
        for j in selected_muons:

            if j <= i: continue
            if printOn: print("\t considering (i,j)=({0:d}, {1:d})".format(i, j))

            m1_eta, m1_phi = entry.Muon_eta[i], entry.Muon_phi[i]
            m2_eta, m2_phi = entry.Muon_eta[j], entry.Muon_phi[j]

            dPhi = min(abs(m1_phi-m2_phi), 2.*pi-abs(m1_phi-m2_phi))
            DR = sqrt(dPhi**2 + (m1_eta-m2_eta)**2)
            if DR < mm['mt_DR']:
                if printOn: print("\t fail mmDR DR={0:f}".format(DR))
                continue

            # store in [leading, sub-leading] order
            if entry.Muon_pt[i] > entry.Muon_pt[j]:
                mm_pairs.append([i,j])
            else: mm_pairs.append([j,i])

    return mm_pairs


def compareMuMuPairs(entry, pair1, pair2):
    i1, i2, j1, j2 = pair1[0], pair2[0], pair1[1], pair2[1]

    if entry.Muon_pfRelIso04_all[i2]  < entry.Muon_pfRelIso04_all[i1]:
        if entry.Muon_pfRelIso04_all[j2] <= entry.Muon_pfRelIso04_all[j1]:
            return True

    if entry.Muon_pfRelIso04_all[j2] < entry.Muon_pfRelIso04_all[j1]:
         if entry.Muon_pfRelIso04_all[i2]  <= entry.Muon_pfRelIso04_all[i1]:
             return True

    if entry.Muon_pfRelIso04_all[i1] == entry.Muon_pfRelIso04_all[i2]:
        if entry.Muon_pfRelIso04_all[j1] == entry.Muon_pfRelIso04_all[j2]:
            if (entry.Muon_pt[i2]+entry.Muon_pt[j2]) > (entry.Muon_pt[i1]+entry.Muon_pt[j1]):
                return True

    return False


def getBestMuMuPair(entry, cat='mm', pairList=[], printOn=False):

    # form all possible pairs that satisfy DR requirement
    if printOn: print("Entering getBestMuMuPair()")
    mm_pairs = getMuMuPairs(entry,cat=cat,pairList=pairList,printOn=printOn)

    for i in range(len(mm_pairs)-1,0,-1) :
        if compareMuMuPairs(entry, mm_pairs[i], mm_pairs[i-1]) :
            mm_pairs[i-1], mm_pairs[i] = mm_pairs[i], mm_pairs[i-1]

    if len(mm_pairs) == 0 : return []
    return mm_pairs[0]


# select a muon for the Z candidate
def goodMuon(entry, j ):
    """ tauFun.goodMuon(): select good muons
                           for Z -> mu + mu
    """

    mm = selections['mm'] # selections for Z->mumu
    if entry.Muon_pt[j] < mm['mu_pt']: return False
    if abs(entry.Muon_eta[j]) > mm['mu_eta']: return False
    if mm['mu_iso_f'] and entry.Muon_pfRelIso04_all[j] >  mm['mu_iso']: return False
    if mm['mu_ID'] :
        if not (entry.Muon_mediumId[j] or entry.Muon_tightId[j]): return False
    if mm['mu_ID'] and not entry.Muon_looseId[j] : return False
    if abs(entry.Muon_dxy[j]) > mm['mu_dxy']: return False
    if abs(entry.Muon_dz[j]) > mm['mu_dz']: return False
    if mm['mu_type'] :
        if not (entry.Muon_isGlobal[j] or entry.Muon_isTracker[j]) : return False

    return True

def makeGoodMuonList(entry) :
    goodMuonList = []
    for i in range(entry.nMuon) :
        if goodMuon(entry, i) : goodMuonList.append(i)
    #print("In tauFun.makeGoodMuonList = {0:s}".format(str(goodMuonList)))
    return goodMuonList


def getGoodMuonList(entry) :
    goodMuonList = []
    for i in range(entry.nMuon) :
        if goodMuon(entry, i) : goodMuonList.append(i)
    #print("In tauFun.makeGoodMuonList = {0:s}".format(str(goodMuonList)))
    return goodMuonList

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
def goodElectron_4tau(lepTypes, entry, j, printOn=False):
    if 'e' not in lepTypes:
        return False
    sel = selections[lepTypes]
    #if lepTypes is 'ee', we actually need to use the 'et' selections instead
    # (since 'ee' selections are really for prompt electrons, which we're not interested in for 4tau analysis.)
    if lepTypes == 'ee':
        sel = selections['et']
    if entry.Electron_pt[j] < sel['ele_pt']:
        if printOn:
            printCut(entry.event, lepTypes, 'e', j, "pt", entry.Electron_pt[j])
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
    if ord(entry.Electron_lostHits[j]) > sel['ele_lostHits']:
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
    if sel['mu_iso_f'] and entry.Muon_pfRelIso04_all[j] >  sel['mu_iso']: 
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

# select an electron for the Z candidate
def goodElectron(entry, j) :
    """ tauFun.goodElectron(): select good electrons
                               for Z -> ele + ele
    """
    ee = selections['ee'] # selections for Z->ee
    if entry.Electron_pt[j] < ee['ele_pt']: return False
    if abs(entry.Electron_eta[j]) > ee['ele_eta']: return False
    if abs(entry.Electron_dxy[j]) > ee['ele_dxy']: return False
    if abs(entry.Electron_dz[j]) > ee['ele_dz']: return False
    if ord(entry.Electron_lostHits[j]) > ee['ele_lostHits']: return False
    if ee['ele_iso_f'] and entry.Electron_pfRelIso03_all[j] >  ee['ele_iso']: return False
    if ee['ele_convVeto']:
        if not entry.Electron_convVeto[j]: return False
    if ee['ele_ID']:
        if not entry.Electron_mvaFall17V2noIso_WP90[j] : return False

    return True

def makeGoodElectronList(entry) :
    goodElectronList = []
    for i in range(entry.nElectron) :
        if goodElectron(entry, i) : goodElectronList.append(i)
    return goodElectronList


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

##############
def goodMuonExtraLepton(entry, j):
    """ tauFun.goodMuon(): select good muons
                           for Z -> mu + mu
    """

    mm = selections['mextra'] # selections for Z->mumu
    if entry.Muon_pt[j] < mm['mu_pt']: return False
    if abs(entry.Muon_eta[j]) > mm['mu_eta']: return False
    if mm['mu_iso_f'] and entry.Muon_pfRelIso04_all[j] >  mm['mu_iso']: return False
    if mm['mu_ID'] and not (entry.Muon_mediumId[j] or entry.Muon_tightId[j]): return False
    if abs(entry.Muon_dxy[j]) > mm['mu_dxy']: return False
    if abs(entry.Muon_dz[j]) > mm['mu_dz']: return False
    if mm['mu_type'] :
        if not (entry.Muon_isGlobal[j] or entry.Muon_isTracker[j]) : return False

    return True

def makeGoodMuonListExtraLepton(entry, listMu) :
    goodExtraMuonList = []
    for i in range(entry.nMuon) :
        if i not in listMu and goodMuonExtraLepton(entry, i) : goodExtraMuonList.append(i)
    #print("In tauFun.makeGoodMuonList = {0:s}".format(str(goodMuonList)))
    return goodExtraMuonList

# select an electron for the Z candidate
def goodElectronExtraLepton(entry, j) :
    """ tauFun.goodElectron(): select good electrons
                               for Z -> ele + ele
    """
    ee = selections['eextra'] # selections for Z->ee
    if entry.Electron_pt[j] < ee['ele_pt']: return False
    if abs(entry.Electron_eta[j]) > ee['ele_eta']: return False
    if abs(entry.Electron_dxy[j]) > ee['ele_dxy']: return False
    if abs(entry.Electron_dz[j]) > ee['ele_dz']: return False
    if ord(entry.Electron_lostHits[j]) > ee['ele_lostHits']: return False
    if ee['ele_iso_f'] and entry.Electron_pfRelIso03_all[j] >  ee['ele_iso']: return False
    if ee['ele_convVeto']:
        if not entry.Electron_convVeto[j]: return False
    if ee['ele_ID']:
        if not entry.Electron_mvaFall17V2noIso_WP90[j] : return False

    return True

def makeGoodElectronListExtraLepton(entry, listEl) :
    goodExtraElectronList = []
    for i in range(entry.nElectron) :
        if i not in listEl and goodElectronExtraLepton(entry, i) : goodExtraElectronList.append(i)
    return goodExtraElectronList

def eliminateCloseTauAndLepton(entry, goodElectronList, goodMuonList, goodTauList) :

    badMuon, badElectron, badTau = [], [], []
    # check tau vs tau
    for tau1 in goodTauList :
        for tau2 in goodTauList :
            if tau1 == tau2 : continue
            dEta = abs(entry.Tau_eta[tau1] - entry.Tau_eta[tau2])
            if dEta > 0.3 : continue
            dPhi = abs(entry.Tau_phi[tau1] - entry.Tau_phi[tau2])
            if dPhi > 0.3 : continue
            if sqrt(dEta*dEta + dPhi*dPhi) > 0.3 : continue
            if not (tau1 in badTau) and entry.Tau_pt[tau1] < entry.Tau_pt[tau2] : badTau.append(tau1)
            if not (tau2 in badTau) and entry.Tau_pt[tau1] > entry.Tau_pt[tau2] : badTau.append(tau2)

        #check tau vs mu
        for mu2 in goodMuonList :
            dEta = abs(entry.Tau_eta[tau1] - entry.Muon_eta[mu2])
            if dEta > 0.3 : continue
            dPhi = abs(entry.Tau_phi[tau1] - entry.Muon_phi[mu2])
            if dPhi > 0.3 : continue
            if sqrt(dEta*dEta + dPhi*dPhi) > 0.3 : continue
            if not (tau1 in badTau) and entry.Tau_pt[tau1] < entry.Muon_pt[mu2] : badTau.append(tau1)
            if not (mu2 in badMuon) and entry.Tau_pt[tau1] > entry.Muon_pt[mu2] : badMuon.append(mu2)

        #check tau vs el
        for e2 in goodElectronList :
            dEta = abs(entry.Tau_eta[tau1] - entry.Electron_eta[e2])
            if dEta > 0.3 : continue
            dPhi = abs(entry.Tau_phi[tau1] - entry.Electron_phi[e2])
            if dPhi > 0.3 : continue
            if sqrt(dEta*dEta + dPhi*dPhi) > 0.3 : continue
            if not (tau1 in badTau) : badTau.append(tau1)
            if not (e2 in badElectron) : badElectron.append(e2)
            if not (tau1 in badTau) and entry.Tau_pt[tau1] < entry.Electron_pt[e2] : badTau.append(tau1)
            if not (e2 in badElectron) and entry.Tau_pt[tau1] > entry.Electron_pt[e2] : badElectron.append(e2)

    # check el vs el
    for e1 in goodElectronList :
        for e2 in goodElectronList :
            if e1 == e2 : continue
            dEta = abs(entry.Electron_eta[e1] - entry.Electron_eta[e2])
            if dEta > 0.3 : continue
            dPhi = abs(entry.Electron_phi[e1] - entry.Electron_phi[e2])
            if dPhi > 0.3 : continue
            if sqrt(dEta*dEta + dPhi*dPhi) > 0.3 : continue
            if not (e1 in badElectron) and entry.Electron_pt[e1] < entry.Electron_pt[e2] : badElectron.append(e1)
            if not (e2 in badElectron) and entry.Electron_pt[e1] > entry.Electron_pt[e2] : badElectron.append(e2)

    #check mu vs mu and vs el
    for mu1 in goodMuonList :
        for mu2 in goodMuonList :
            if mu1 == mu2 : continue
            dEta = abs(entry.Muon_eta[mu1] - entry.Muon_eta[mu2])
            if dEta > 0.3 : continue
            dPhi = abs(entry.Muon_phi[mu1] - entry.Muon_phi[mu2])
            if dPhi > 0.3 : continue
            if sqrt(dEta*dEta + dPhi*dPhi) > 0.3 : continue
            if not (mu1 in badMuon) and entry.Muon_pt[mu1] < entry.Muon_pt[mu2] : badMuon.append(mu1)
            if not (mu2 in badMuon) and entry.Muon_pt[mu1] > entry.Muon_pt[mu2] : badMuon.append(mu2)


        for e2 in goodElectronList :
            dEta = abs(entry.Muon_eta[mu1] - entry.Electron_eta[e2])
            if dEta > 0.3 : continue
            dPhi = abs(entry.Muon_phi[mu1] - entry.Electron_phi[e2])
            if dPhi > 0.3 : continue
            if sqrt(dEta*dEta + dPhi*dPhi) > 0.3 : continue
            if not (mu1 in badMuon) and entry.Muon_pt[mu1] < entry.Electron_pt[e2] : badMuon.append(mu1)
            if not (e2 in badElectron) and entry.Muon_pt[mu1] > entry.Electron_pt[e2] : badElectron.append(e2)



    for bade in badElectron : goodElectronList.remove(bade)
    for badmu in badMuon : goodMuonList.remove(badmu)
    for badtau in badTau : goodTauList.remove(badtau)

    return goodElectronList, goodMuonList, goodTauList


def eliminateCloseLeptons(entry, goodElectronList, goodMuonList) :
    badMuon, badElectron = [], []
    if len(goodMuonList)> 1 :
        for mu1 in goodMuonList :
            for mu2 in goodMuonList :
                if mu1 == mu2 : continue
                dEta = abs(entry.Muon_eta[mu1] - entry.Muon_eta[mu2])
                if dEta > 0.3 : continue
                dPhi = abs(entry.Muon_phi[mu1] - entry.Muon_phi[mu2])
                if dPhi > 0.3 : continue
                if sqrt(dEta*dEta + dPhi*dPhi) > 0.3 : continue
                if not (mu1 in badMuon) and entry.Muon_pt[mu1] < entry.Muon_pt[mu2] : badMuon.append(mu1)
                if not (mu2 in badMuon) and entry.Muon_pt[mu1] > entry.Muon_pt[mu2] : badMuon.append(mu2)

            for e2 in goodElectronList :
                dEta = abs(entry.Muon_eta[mu1] - entry.Electron_eta[e2])
                if dEta > 0.3 : continue
                dPhi = abs(entry.Muon_phi[mu1] - entry.Electron_phi[e2])
                if dPhi > 0.3 : continue
                if sqrt(dEta*dEta + dPhi*dPhi) > 0.3 : continue
                if not (mu1 in badMuon) and entry.Muon_pt[mu1] < entry.Electron_pt[e2] : badMuon.append(mu1)
                if not (e2 in badElectron) and entry.Muon_pt[mu1] > entry.Electron_pt[e2] : badElectron.append(e2)
    if len(goodElectronList)> 1 :
        for e1 in goodElectronList :
            for e2 in goodElectronList :
                if e1 == e2 : continue
                dEta = abs(entry.Electron_eta[e1] - entry.Electron_eta[e2])
                if dEta > 0.3 : continue
                dPhi = abs(entry.Electron_phi[e1] - entry.Electron_phi[e2])
                if dPhi > 0.3 : continue
                if sqrt(dEta*dEta + dPhi*dPhi) > 0.3 : continue
                if not (e1 in badElectron) and entry.Electron_pt[e1] < entry.Electron_pt[e2] : badElectron.append(e1)
                if not (e2 in badElectron) and entry.Electron_pt[e1] > entry.Electron_pt[e2] : badElectron.append(e2)

    for bade in badElectron : goodElectronList.remove(bade)
    for badmu in badMuon : goodMuonList.remove(badmu)

    return goodElectronList, goodMuonList

def findETrigger(goodElectronList,entry,era):
    EltrigList =[]
    nElectron = len(goodElectronList)

    if nElectron > 1 :
        if era == '2016' and not entry.HLT_Ele27_WPTight_Gsf : return EltrigList
        if era == '2017' and not entry.HLT_Ele35_WPTight_Gsf : return EltrigList
        for i in range(nElectron) :

            ii = goodElectronList[i]
            if era == '2016' and entry.Electron_pt[ii] < 29 : continue
            if era == '2017' and entry.Electron_pt[ii] < 37 : continue
            #print("Electron: pt={0:.1f} eta={1:.2f} phi={2:.2f}".format(entry.Electron_pt[ii], entry.Electron_eta[ii], entry.Electron_phi[ii]))
            #e1 = TLorentzVector()
            #e1.SetPtEtaPhiM(entry.Electron_pt[ii],entry.Electron_eta[ii],entry.Electron_phi[ii],0.0005)

            for iobj in range(0,entry.nTrigObj) :
                dR = DRobj(entry.Electron_eta[ii],entry.Electron_phi[ii], entry.TrigObj_eta[iobj], entry.TrigObj_phi[iobj])
                #print("    Trg Obj: eta={0:.2f} phi={1:.2f} dR={2:.2f} bits={3:x}".format(
                    #entry.TrigObj_eta[iobj], entry.TrigObj_phi[iobj], dR, entry.TrigObj_filterBits[iobj]))
                if entry.TrigObj_filterBits[iobj] & 2  and dR < 0.5: ##that corresponds 0 WPTight
                    EltrigList.append(ii)
                    #print "======================= iobj", iobj, "entry.Trig",entry.TrigObj_id[iobj], "Bits", entry.TrigObj_filterBits[iobj]," dR", dR, "electron",i,"ii",ii,entry.TrigObj_id[iobj]

    return EltrigList


def findMuTrigger(goodMuonList,entry,era):
    MutrigList =[]
    nMuon = len(goodMuonList)

    if nMuon > 1 :
        if era == '2016' and not entry.HLT_IsoMu24 : return MutrigList
        if era == '2017' and not entry.HLT_IsoMu27 : return MutrigList
        for i in range(nMuon) :


            ii = goodMuonList[i]
            if era == '2016' and entry.Muon_pt[ii] < 26 : continue
            if era == '2017' and entry.Muon_pt[ii] < 29 : continue
            #print("Muon: pt={0:.1f} eta={1:.4f} phi={2:.4f}".format(entry.Muon_pt[ii], entry.Muon_eta[ii], entry.Muon_phi[ii]))
            for iobj in range(0,entry.nTrigObj) :
                dR = DRobj(entry.Muon_eta[ii],entry.Muon_phi[ii], entry.TrigObj_eta[iobj], entry.TrigObj_phi[iobj])
                #print("    Trg Obj: eta={0:.4f} phi={1:.4f} dR={2:.4f} bits={3:x}".format(
                #    entry.TrigObj_eta[iobj], entry.TrigObj_phi[iobj], dR, entry.TrigObj_filterBits[iobj]))
                if entry.TrigObj_filterBits[iobj] & 8 or entry.TrigObj_filterBits[iobj] & 2 and dR < 0.5: ##that corresponds to Muon Trigger
                    MutrigList.append(ii)
                #print "======================= and === iobj", iobj, entry.TrigObj_id[iobj], "Bits", entry.TrigObj_filterBits[iobj]," dR", dR, "electron",i

    return MutrigList

def ComparepT(El, Mu, entry) :
    if entry.Electron_pt[El] > entry.Muon_pt[Mu] : return True
    else : return False

def findLeadMuMu(goodMuonList, entry) :
    nMuon = len(goodMuonList)
    if nMuon > 1 :
        # find leading muons
        maxpt = 0.0
        submaxpt = 0.0
        ptList=[]
        maxmu=1
        submaxmu=1
        tempMuList=[]

        for muNum in range(nMuon) :
            mu = goodMuonList[muNum]
            tempMuList.append(mu)
            ptList.append(entry.Muon_pt[mu])
            tempPt=entry.Muon_pt[mu]

            if tempPt>maxpt:
                maxpt=tempPt
                maxmu=mu


        maxMuCharge = entry.Muon_charge[maxmu]

        for muNum in range(nMuon) :
            submu = goodMuonList[muNum]
            tempPt=entry.Muon_pt[submu]

            if tempPt>submaxpt and maxMuCharge*entry.Muon_charge[submu]<0  :
                submaxpt=tempPt
                submaxmu=submu

        #pos in goodmuon list
        #maxmu = ptList.index(max(ptList))
        #maxpt = max(ptList)
        #ptList[maxmu]=0.0
        #for muNum in range(nMuon) :
        #submaxmu = ptList.index(max(ptList))
        #ptList[maxmu]=maxpt


        mu1 = TLorentzVector() #leading muon
        mu2 = TLorentzVector() #subleading muon
        #print submaxmu,ptList[submaxmu],submaxmu,ptList[submaxmu]

        #print "leading mu ",entry.event,entry.Muon_charge[maxmu],entry.Muon_pt[maxmu],entry.Muon_eta[maxmu],entry.Muon_phi[maxmu]
        #print "sublead mu ",entry.event,entry.Muon_charge[submaxmu],entry.Muon_pt[submaxmu],entry.Muon_eta[submaxmu],entry.Muon_phi[submaxmu]
        #print "full muon list"
        #for mu in goodMuonList:
        #    print "mu ",entry.Muon_charge[mu],entry.Muon_pt[mu],entry.Muon_eta[mu],entry.Muon_phi[mu]

        mu1.SetPtEtaPhiM(entry.Muon_pt[maxmu],entry.Muon_eta[maxmu],entry.Muon_phi[maxmu],0.105)
        mu2.SetPtEtaPhiM(entry.Muon_pt[submaxmu],entry.Muon_eta[submaxmu],entry.Muon_phi[submaxmu],0.105)
        #print "dimuon mass",(mu1 + mu2).M()

        #if entry.Muon_charge[maxmu] > 0. :
        #    pairList = [mu1,mu2]
        #    selpair = [maxmu,submaxmu]
        #else :
        #    pairList = [mu2,mu1]
        #    selpair = [submaxmu,maxmu]

        pairList = [mu1,mu2]
        selpair = [maxmu,submaxmu]

    return pairList, selpair

#find highest pT tau pair (which is valid)
def findLeadTauTau(goodTauList, entry, printOn=False) :
        
    #list (length 2) of best tau pair. (channel is not used other than to ensure it is a tttt process)
    bestTaus = getBestTauPairPt('tttt', entry, goodTauList)
    
    if len(bestTaus) < 2:
        return [],[]
    if printOn:
        print("findLeadTauTau: \ngoodTaulist={}\nBest tau pair: {}".format(goodTauList, bestTaus))
    
    maxt = bestTaus[0]
    submaxt = bestTaus[1]
    #get their 4-momenta.
    tau1 = TLorentzVector() #leading muon
    tau2 = TLorentzVector() #subleading muon
    tau1.SetPtEtaPhiM(entry.Tau_pt[maxt],entry.Tau_eta[maxt],entry.Tau_phi[maxt],1.777)
    tau2.SetPtEtaPhiM(entry.Tau_pt[submaxt],entry.Tau_eta[submaxt],entry.Tau_phi[submaxt],1.777)

    pairList = [tau1,tau2]
    selpair = bestTaus

    return pairList, selpair

def findZ(goodElectronList, goodMuonList, entry) :
    mm = selections['mm'] # H->tau(mu)+tau(h) selections
    selpair,pairList, mZ, bestDiff = [],[], 91.19, 99999.
    nElectron = len(goodElectronList)
    #print 'going in tauFun', goodElectronList, nElectron, entry.event, entry.luminosityBlock, entry.run, bestDiff
    if nElectron > 1 :
        for i in range(nElectron) :
            ii = goodElectronList[i]
            e1 = TLorentzVector()
            e1.SetPtEtaPhiM(entry.Electron_pt[ii],entry.Electron_eta[ii],entry.Electron_phi[ii],0.0005)
            for j in range(i+1,nElectron) :
                jj = goodElectronList[j]
                #print 'going in tauFun masses', goodElectronList, nElectron, entry.event, entry.luminosityBlock, entry.run, 'for', jj, ii, entry.Electron_charge[ii],  entry.Electron_charge[jj]
                if entry.Electron_charge[ii] != entry.Electron_charge[jj] :
                    e2 = TLorentzVector()
                    e2.SetPtEtaPhiM(entry.Electron_pt[jj],entry.Electron_eta[jj],entry.Electron_phi[jj],0.0005)
                    cand = e1 + e2
                    mass = cand.M()
                    #if mass < 60 or mass > 120 : continue
                    #print 'going in tauFun masses', goodElectronList, nElectron, entry.event, entry.luminosityBlock, entry.run, bestDiff, 'is abs(mass-mZ > bestDiff', abs(mass-mZ), bestDiff, 'for', jj, ii
                    if abs(mass-mZ) < bestDiff :
                        bestDiff = abs(mass-mZ)
                        #print 'masses', bestDiff, mass, entry.Electron_charge[jj], entry.Electron_charge[ii], entry.event, entry.luminosityBlock, entry.run, 'elect', jj, ii, goodElectronList
                        if entry.Electron_charge[ii] > 0. :
                            pairList = [e1,e2]
                            selpair = [ii,jj]
                        else :
                            pairList = [e2,e1]
                            selpair = [jj,ii]

    nMuon = len(goodMuonList)
    if nMuon > 1 :
        # find mass pairings
        for i in range(nMuon) :
            ii = goodMuonList[i]
            #if entry.Muon_pfRelIso04_all[ii] >  mm['mu_iso']: continue
            mu1 = TLorentzVector()
            mu1.SetPtEtaPhiM(entry.Muon_pt[ii],entry.Muon_eta[ii],entry.Muon_phi[ii],0.105)
            for j in range(i+1,nMuon) :
                jj = goodMuonList[j]
                if entry.Muon_charge[ii] != entry.Muon_charge[jj] :
                    mu2 = TLorentzVector()
                    mu2.SetPtEtaPhiM(entry.Muon_pt[jj],entry.Muon_eta[jj],entry.Muon_phi[jj],0.105)
                    cand = mu1 + mu2
                    mass = cand.M()
                    #if mass < 60 or mass > 120 : continue
                    if abs(mass-mZ) < bestDiff :
                        bestDiff = abs(mass-mZ)
                        if entry.Muon_charge[ii] > 0. :
                            pairList = [mu1,mu2]
                            selpair = [ii,jj]
                        else :
                            pairList = [mu2,mu1]
                            selpair = [jj,ii]

    # first particle of pair is positive
    #print 'returning', selpair,  'is muon', nMuon, goodMuonList, 'isEl', nElectron, goodElectronList, entry.event, entry.luminosityBlock, entry.run
    return pairList, selpair


def findZmumu(goodMuonList, entry) :
    pairList, mZ, bestDiff = [], 91.19, 99999.
    nMuon = len(goodMuonList)
    if nMuon < 2 : return pairList
    # find mass pairings
    for i in range(nMuon) :
        mu1 = TLorentzVector()
        mu1.SetPtEtaPhiM(entry.Muon_pt[i],entry.Muon_eta[i],entry.Muon_phi[i],0.105)
        for j in range(i+1,nMuon) :
            if entry.Muon_charge[i] != entry.Muon_charge[j] :
                mu2 = TLorentzVector()
                mu2.SetPtEtaPhiM(entry.Muon_pt[j],entry.Muon_eta[j],entry.Muon_phi[j],0.105)
                cand = mu1 + mu2
                mass = cand.M()
                #if mass < 60 or mass > 120 : continue
                if abs(mass-mZ) < bestDiff :
                    bestDiff = abs(mass-mZ)
                    pairList.append([mu1,mu2])

    return pairList

def findZee(goodElectronList, entry) :
    pairList, mZ, bestDiff = [], 91.19, 99999.
    nElectron = len(goodElectronList)
    if nElectron < 2 : return pairList
    # find mass pairings
    for i in range(nElectron) :
        e1 = TLorentzVector()
        e1.SetPtEtaPhiM(entry.Electron_pt[i],entry.Electron_eta[i],entry.Electron_phi[i],0.0005)
        for j in range(i+1,nElectron) :
            if entry.Electron_charge[i] != entry.Electron_charge[j] :
                e2 = TLorentzVector()
                e2.SetPtEtaPhiM(entry.Electron_pt[j],entry.Electron_eta[j],entry.Electron_phi[j],0.0005)
                cand = e1 + e2
                mass = cand.M()
                #if mass < 60 or mass > 120 : continue
                if abs(mass-mZ) < bestDiff :
                    bestDiff = abs(mass-mZ)
                    pairList.append([e1,e2])

    return pairList


def catToNumber(cat) :
    number = { 'eeet':1, 'eemt':2, 'eett':3, 'eeem':4, 'mmet':5, 'mmmt':6, 'mmtt':7, 'mmem':8, 'et':9, 'mt':10, 'tt':11, 'tttt':12, 'ttmt':13, 'ttet':14, 'ttem':15, 'mtmt':16, 'mtet':17, 'mtem':18, 'etet':19, 'etem':20, 'emem':21 }
    return number[cat]


def numberToCat(number) :
    cat = { 1:'eeet', 2:'eemt', 3:'eett', 4:'eeem', 5:'mmet', 6:'mmmt', 7:'mmtt', 8:'mmem', 9:'et', 10:'mt', 11:'tt', 12:'tttt', 13:'ttmt', 14:'ttet', 15:'ttem', 16:'mtmt', 17:'mtet', 18:'mtem', 19:'etet', 20:'etem', 21:'emem' }
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
        GF.printEvent(e)
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
