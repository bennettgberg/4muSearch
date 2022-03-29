# output ntuple for H->tautau analysis for CMSSW_10_2_X

from ROOT import TLorentzVector, TH1
from math import sqrt, sin, cos, pi
#import tauFun_4tau
#import tauFun2
import muFun
import ROOT, array
import os
import sys
import generalFunctions as GF

#how many particles of each type to keep (maximum)
nMax = 15
#list of particles of interest
pTypes = ["Muon", "Photon", "Electron"]
#list of variables that have a separate value for each particle.
#floats
fNames = ["dxy", "dz", "pt", "pt_tr", "pt_uncor", "m_uncor",  "phi", "eta", "mass", "charge", "phi_tr", "eta_tr",
            "mt", "pfmt", "iso", "eMVA",  "tightId", "mediumId", "mediumPromptId", "looseId", "isGlobal", "isTracker",
            "ip3d", "idDTve", "idDTvm", "idDTvj", "idDMNewDMs", "idMVANewDMs", "rawMVANewDMs"]
#longs
lNames = ["GenPart_statusFlags", "GenPart_status", "gen_match", "decayMode"]

electronMass = 0.0005
muonMass  = 0.105
class outTuple() :

    def __init__(self,fileName, era, doSyst=False,shift=[], isMC=True, onlyNom=False):
        from array import array
        from ROOT import TFile, TTree

        # Tau Decay types
        self.kUndefinedDecayType, self.kTauToHadDecay,  self.kTauToElecDecay, self.kTauToMuDecay = 0, 1, 2, 3
        ROOT.gInterpreter.ProcessLine(".include .")
        ########### JetMet systematics
        #self.listsyst=['njets', 'nbtag', 'jpt', 'jeta', 'jflavour','MET_T1_pt', 'MET_T1_phi', 'MET_pt', 'MET_phi', 'MET_T1Smear_pt', 'MET_T1Smear_phi']
        self.jessyst=['_nom']
        self.listsyst=['njets', 'nbtag', 'jpt', 'jeta', 'jflavour','MET_T1_pt', 'MET_T1_phi', 'MET_pt', 'MET_phi']
        if doSyst :
            self.jessyst=['_nom','_jesAbsolute', '_jesAbsolute_{0:s}'.format(str(era)), '_jesBBEC1', '_jesBBEC1_{0:s}'.format(str(era)), '_jesEC2', '_jesEC2_{0:s}'.format(str(era)), '_jesFlavorQCD', '_jesHF', '_jesHF_{0:s}'.format(str(era)), '_jesRelativeBal', '_jesRelativeSample_{0:s}'.format(str(era)), '_jesHEMIssue', '_jesTotal', '_jer']

        if onlyNom :
            self.jessyst=['_nom']
        #shift are the ES basd systematics


        varss=['Up','Down']
        self.n = array('f', [ 0 ])

        self.allsystMET = []
        self.allsystJets = []
        self.jetsVariations=[]
        self.list_of_arrays = []
        self.list_of_arrays_noES = []
        self.list_of_arraysJetsPt = []
        self.list_of_arraysJetsEta = []
        self.list_of_arraysJetsFlavour = []
        self.list_of_arraysJetsNbtag = []
        self.list_of_arraysJetsNjets = []
        self.list_of_arraysJetsFlavour = []
        self.tauMass = 1.7768

        if not isMC  :

            self.listsyst=['njets', 'nbtag', 'jpt', 'jeta', 'jflavour', 'MET_pt', 'MET_phi']
            self.jessyst=['_nom']
            varss=[]

        if doSyst :

            #self.jetsVariations.append('_nom')
            self.allsystMET = []
            self.allsystJets = []
            #create a list with Up/Down from the above combinations

            for i_ in self.listsyst :
                for jes in self.jessyst :
                    if 'nom' not in jes :
                        for var in varss :
                            if 'MET' in i_ and 'T1' in i_:
                                self.allsystMET.append(i_+jes+var)
                                self.list_of_arrays.append(array('f', [ 0 ]))
                                self.list_of_arrays_noES.append(array('f', [ 0 ]))

            for jes in self.jessyst :
                    if 'nom' in jes :
                        self.allsystJets.append(jes)
                        self.list_of_arraysJetsNjets.append( array('f',[0]))
                        self.list_of_arraysJetsNbtag.append( array('f',[0]))
                        self.list_of_arraysJetsFlavour.append( array('f',[-9.99]*15))
                        self.list_of_arraysJetsEta.append( array('f',[-9.99]*15))
                        self.list_of_arraysJetsPt.append( array('f',[-9.99]*15))
                    else :
                        for var in varss :
                            self.allsystJets.append(jes+var)
                            self.list_of_arraysJetsNjets.append( array('f',[0]))
                            self.list_of_arraysJetsNbtag.append( array('f',[0]))
                            self.list_of_arraysJetsFlavour.append( array('f',[-9.99]*15))
                            self.list_of_arraysJetsEta.append( array('f',[-9.99]*15))
                            self.list_of_arraysJetsPt.append( array('f',[-9.99]*15))

        print '------>systematics list', self.allsystMET
        print '------>jetssystematics list', self.allsystJets


        self.f = TFile( fileName, 'recreate' )
        self.t = TTree( 'Events', 'Output tree' )

        self.entries          = 0
        self.run              = array('l',[0])
        self.nElectron        = array('l',[0])
        self.nMuon            = array('l',[0])
        self.nTau            = array('l',[0])
        self.nPhoton         = array('l',[0])
        self.lumi             = array('l',[0])
        self.evt              = array('l',[0])
        self.nPU              = array('l',[0])
        self.nPUEOOT              = array('l',[0])
        self.nPULOOT              = array('l',[0])
        self.nPUtrue              = array('f',[0])
        self.nPV              = array('l',[0])
        self.nPVGood              = array('l',[0])
        self.nOtherPV              = array('l',[0])

        self.OtherPV_z              = array('f',[0]*nMax)
        self.PV_x              = array('f',[0])
        self.PV_y              = array('f',[0])
        self.PV_z              = array('f',[0])

        self.algo              = array('l',[0])
        self.weight           = array('f',[0])
        self.weightPU           = array('f',[0])
        self.weightPUtrue           = array('f',[0])
        self.LHEweight        = array('f',[0])
        self.Generator_weight = array('f',[0])
        self.LHE_Njets        = array('l',[0])
        self.electronTriggerWord  = array('l',[0])
        self.muonTriggerWord  = array('l',[0])
        nwords = 4 #how many dimu trigger words
        self.dimuTriggerWord = array('l',[0]*nwords)
        self.LHEScaleWeights        = array('f',[1]*9)

        self.nGoodElectron    = array('l',[0])
        self.nGoodMuon        = array('l',[0])
        self.nGoodPhoton      = array('l',[0])

        self.L1PreFiringWeight_Nom        = array('f',[0])
        self.L1PreFiringWeight_Up        = array('f',[0])
        self.L1PreFiringWeight_Down        = array('f',[0])

        #print("Boutta create")
        #variables that have a different value for each particle in the event.
        for pType in pTypes:
            for fName in fNames:
                fullname = pType + "_" + fName
                exec("self.%s = array('f',[0]*nMax)"%(fullname))
                exec("self.t.Branch('{0:s}',  self.{0:s},  '{0:s}[{1:d}]/F')".format(fullname, nMax))
            for lName in lNames:
                fullname = pType + "_" + lName
                exec("self.%s = array('l',[0]*nMax)"%(fullname))
                exec("self.t.Branch('{0:s}',  self.{0:s},  '{0:s}[{1:d}]/l')".format(fullname, nMax))

        #self.Muon_pt[0] = 0.
        #self.Muon_pt[1] = 0.
        #print("set muon pt 1.")
        # MET variables
        self.met         = array('f',[0])
        self.metphi      = array('f',[0])
        self.metNoTauES      = array('f',[0])
        self.metphiNoTauES      = array('f',[0])
        self.metNoCor         = array('f',[0])
        self.metphiNoCor      = array('f',[0])
        #self.puppimet    = array('f',[0])
        #self.puppimetphi = array('f',[0])
        self.metcov00    = array('f',[0])
        self.metcov01    = array('f',[0])
        self.metcov10    = array('f',[0])
        self.metcov11    = array('f',[0])

        #systematics

        self.MET_pt_UnclUp = array('f',[0])
        self.MET_phi_UnclUp = array('f',[0])
        self.MET_pt_UnclDown = array('f',[0])
        self.MET_phi_UnclDown = array('f',[0])
        self.met_UnclX = array('f',[0])
        self.met_UnclY = array('f',[0])
        self.MET_T1Smear_pt= array('f',[0])
        self.MET_T1Smear_phi= array('f',[0])
        self.MET_pt_nom= array('f',[0])
        self.MET_pt_nom= array('f',[0])


        # jet variables
        #self.njetsold = array('f',[-1]*8)
        self.njets     = array('f',[0])
        self.nbtag     = array('f',[0])
        self.jflavour  = array('f',[0]*15)
        self.jeta  = array('f',[0]*15)
        self.jpt       = array('f',[0]*15)

        self.t.Branch('run',              self.run,               'run/l' )
        self.t.Branch('nElectron',              self.nElectron,               'nElectron/l' )
        self.t.Branch('nMuon',              self.nMuon,               'nMuon/l' )
        self.t.Branch('nTau',              self.nTau,               'nTau/l' )
        self.t.Branch('nPhoton',              self.nPhoton,               'nPhoton/l' )
        self.t.Branch('lumi',             self.lumi,              'lumi/I' )
        self.t.Branch('evt',              self.evt,               'evt/l' )
        self.t.Branch('nPU',              self.nPU,               'nPU/I' )
        self.t.Branch('nPUEOOT',              self.nPUEOOT,               'nPUEOOT/I' )
        self.t.Branch('nPULOOT',              self.nPULOOT,               'nPULOOT/I' )
        self.t.Branch('nPUtrue',              self.nPUtrue,               'nPUtrue/F' )
        self.t.Branch('nPV',              self.nPV,               'nPV/I' )
        self.t.Branch('nPVGood',              self.nPVGood,               'nPVGood/I' )
        self.t.Branch('PV_x',              self.PV_x,               'PV_x/F' )
        self.t.Branch('PV_y',              self.PV_y,               'PV_y/F' )
        self.t.Branch('PV_z',              self.PV_z,               'PV_z/F' )
        self.t.Branch('algo',              self.algo,               'algo/I' )
        self.t.Branch('weight',           self.weight,            'weight/F' )
        self.t.Branch('weightPU',           self.weightPU,            'weightPU/F' )
        self.t.Branch('weightPUtrue',           self.weightPUtrue,            'weightPUtrue/F' )
        self.t.Branch('LHEweight',        self.LHEweight,         'LHEweight/F' )
        self.t.Branch('LHE_Njets',        self.LHE_Njets,         'LHE_Njets/I' )
        self.t.Branch('LHEScaleWeights',        self.LHEScaleWeights,         'LHEScaleWeights[9]/F' )
        self.t.Branch('Generator_weight', self.Generator_weight,  'Generator_weight/F' )
        self.t.Branch('electronTriggerWord',  self.electronTriggerWord, 'electronTriggerWord/I' )
        self.t.Branch('muonTriggerWord',      self.muonTriggerWord,  'muonTriggerWord/I' )
        self.t.Branch('dimuTriggerWord',      self.dimuTriggerWord,  'dimuTriggerWord[%d]/I'%(nwords) )

        self.t.Branch('nGoodElectron',    self.nGoodElectron,     'nGoodElectron/I' )
        self.t.Branch('nGoodMuon',        self.nGoodMuon,         'nGoodMuon/I' )
        self.t.Branch('nGoodPhoton',        self.nGoodPhoton,         'nGoodPhoton/I' )

        self.t.Branch('L1PreFiringWeight_Nom',        self.L1PreFiringWeight_Nom,        'L1PreFiringWeight_Nom/F')
        self.t.Branch('L1PreFiringWeight_Up',        self.L1PreFiringWeight_Up,        'L1PreFiringWeight_Up/F')
        self.t.Branch('L1PreFiringWeight_Down',        self.L1PreFiringWeight_Down,        'L1PreFiringWeight_Down/F')

        #systematics
        self.t.Branch('MET_pt_UnclUp', self.MET_pt_UnclUp, 'MET_pt_UnclUp/F')
        self.t.Branch('MET_phi_UnclUp', self.MET_phi_UnclUp, 'MET_phi_UnclUp/F')
        self.t.Branch('MET_pt_UnclDown', self.MET_pt_UnclDown, 'MET_pt_UnclDown/F')
        self.t.Branch('MET_phi_UnclDown', self.MET_phi_UnclDown, 'MET_phi_UnclDown/F')
        self.t.Branch('met_UnclX', self.met_UnclX, 'met_UnclX/F')
        self.t.Branch('met_UnclY', self.met_UnclY, 'met_UnclY/F')
        self.t.Branch('MET_T1Smear_pt', self.MET_T1Smear_pt, 'MET_T1Smear_pt/F')
        self.t.Branch('MET_T1Smear_phi', self.MET_T1Smear_phi, 'MET_T1Smear_phi/F')

        # MET variables
        self.t.Branch('met', self.met, 'met/F')
        self.t.Branch('metphi', self.metphi, 'metphi/F')
        self.t.Branch('metNoCor', self.metNoCor, 'metNoCor/F')
        self.t.Branch('metphiNoCor', self.metphiNoCor, 'metphiNoCor/F')
        self.t.Branch('metNoTauES', self.metNoTauES, 'metNoTauES/F')
        self.t.Branch('metphiNoTauES', self.metphiNoTauES, 'metphiNoTauES/F')
        #self.t.Branch('puppimet', self.puppimet, 'puppimet/F')
        #self.t.Branch('puppimetphi', self.puppimetphi, 'puppimetphi/F')
        self.t.Branch('metcov00', self.metcov00, 'metcov00/F')
        self.t.Branch('metcov01', self.metcov01, 'metcov01/F')
        self.t.Branch('metcov10', self.metcov10, 'metcov10/F')
        self.t.Branch('metcov11', self.metcov11, 'metcov11/F')

        # jet variables
        #self.t.Branch('njetsold', self.njetsold, 'njetsold[8]/F')
        #self.t.Branch('nbtagold', self.nbtagold, 'nbtagold[8]/F')
        self.t.Branch('njets', self.njets, 'njets/F')
        self.t.Branch('nbtag', self.nbtag, 'nbtag/F')

        if doSyst :
                #Book the branches and the arrays needed to store variables
                for i, v in enumerate(self.allsystMET):

                    if str(era)=='2017' :
                        v = v.replace('MET','METFixEE2017')
                    iMET= v.replace('METFixEE2017','MET')
                    iiMET=iMET+'_noES'
                    self.t.Branch(iMET, self.list_of_arrays[i], '{0:s}/F'.format(iMET))
                    self.t.Branch(iiMET, self.list_of_arrays_noES[i], '{0:s}/F'.format(iiMET))

                for i, v in enumerate(self.allsystJets):
                    self.t.Branch('njets{0:s}'.format(v), self.list_of_arraysJetsNjets[i], 'njets{0:s}/F'.format(v))
                    self.t.Branch('nbtag{0:s}'.format(v), self.list_of_arraysJetsNbtag[i], 'nbtag{0:s}/F'.format(v))
                    self.t.Branch('jflavour{0:s}'.format(v), self.list_of_arraysJetsFlavour[i], 'jflavour{0:s}[15]/F'.format(v))
                    self.t.Branch('jpt{0:s}'.format(v), self.list_of_arraysJetsPt[i], 'jpt{0:s}[15]/F'.format(v))
                    self.t.Branch('jeta{0:s}'.format(v), self.list_of_arraysJetsEta[i], 'jeta{0:s}[15]/F'.format(v))

        #self.MET_pt_jesEC2Up  = array('f',[0])
        #self.t.Branch('MET_pt_jesEC2Up', self.MET_pt_jesEC2Up, 'MET_pt_jesEC2Up/F' )
        self.tN=[]

        for i, isyst in enumerate(shift) :
            self.tN.append(isyst)

            #if isyst == "Events" : continue
            #else  :
            if i > 0 :
                self.tN[i-1]  = self.t.CloneTree()
                self.tN[i-1].SetName(isyst)

                print '====================>',self.tN[i-1], self.tN[i-1].GetName()

    def get_mt(self,METtype,entry,tau) :
        if METtype == 'MVAMet' :
            # temporary choice
            dphi = tau.Phi() - entry.MET_phi
            return sqrt(2.*tau.Pt()*entry.MET_pt*(1. - cos(dphi)))
        elif METtype == 'PFMet' :
            dphi = tau.Phi() - entry.MET_phi
            return sqrt(2.*tau.Pt()*entry.MET_pt*(1. - cos(dphi)))
        elif METtype == 'PUPPIMet' :
            dphi = tau.Phi() - entry.PuppiMET_phi
            return sqrt(2.*tau.Pt()*entry.PuppiMET_pt*(1. - cos(dphi)))
        else :
            print("Invalid METtype={0:s} in outTuple.get_mt().   Exiting".format(METtype))

    def getPt_tt(self,entry,tau1,tau2) :
        ptMiss = TLorentzVector()
        ptMiss.SetPtEtaPhiM(entry.MET_pt,0.,entry.MET_phi,0.)
        return (tau1+tau2+ptMiss).Pt()

    def getMt_tot(self,entry,tau1,tau2) :
        pt1, pt2, met = tau1.Pt(), tau2.Pt(), entry.MET_pt
        phi1, phi2, metphi = tau1.Phi(), tau2.Phi(), entry.MET_phi
        arg = 2.*(pt1*met*(1. - cos(phi1-metphi)) + pt2*met*(1. - cos(phi2-metphi)) + pt1*pt2*(1. - cos(phi2-phi1)))
        return sqrt(arg)

    def getDR(self,entry, v1,v2) :

        dPhi = min(abs(v2.Phi()-v1.Phi()),2.*pi-abs(v2.Phi()-v1.Phi()))
        DR = sqrt(dPhi**2 + (v2.Eta()-v1.Eta())**2)
        return DR

    def getDRnV(self,entry, eta1,phi1, eta2,phi2) :

        dPhi = min(abs(phi2-phi1),2.*pi-abs(phi2-phi1))
        DR = sqrt(dPhi**2 + (eta2-eta1)**2)
        return DR

    def getdPhi(self, entry, v1,v2) :
        dPhi = min(abs(v2.Phi()-v1.Phi()),2.*pi-abs(v2.Phi()-v1.Phi()))
        return dPhi

    def getM_vis(self,entry,tau1,tau2) :
        return (tau1+tau2).M()

    def getJets(self,entry,tau1,tau2,era) :
        nJet30, jetList, bJetList, bJetListFlav = 0, [], [], []
        phi2_1, eta2_1 = tau1.Phi(), tau1.Eta()
        phi2_2, eta2_2 = tau2.Phi(), tau2.Eta()
        bjet_discr = 0.6321
        bjet_discrFlav = 0.0614
        if str(era) == '2017' : bjet_discr = 0.4941
        if str(era) == '2018' : bjet_discr = 0.4184

        for j in range(entry.nJet) :
            if entry.Jet_jetId[j]  < 2  : continue  #require tight jets
            if entry.Jet_pt[j]>20 and entry.Jet_pt[j] < 50 and entry.Jet_puId[j]  < 4  : continue #loose jetPU_iD
            if str(era) == '2017'  and entry.Jet_pt[j] > 20 and entry.Jet_pt[j] < 50 and abs(entry.Jet_eta[j]) > 2.65 and abs(entry.Jet_eta[j]) < 3.139 : continue  #remove noisy jets
            if entry.Jet_pt[j] < 20. : continue
            if abs(entry.Jet_eta[j]) > 4.7 : continue
            phi1, eta1 = entry.Jet_phi[j], entry.Jet_eta[j]
            dPhi = min(abs(phi2_1-phi1),2.*pi-abs(phi2_1-phi1))
            DR = sqrt(dPhi**2 + (eta2_1-eta1)**2)
            dPhi = min(abs(phi2_2-phi1),2.*pi-abs(phi2_2-phi1))
            DR = min(DR,sqrt(dPhi**2 + (eta2_2-eta1)**2))
            if DR < 0.5 : continue
            if entry.Jet_pt[j] > 30 :
                if abs(entry.Jet_eta[j]) < 2.4 and entry.Jet_btagDeepB[j] > bjet_discr : bJetList.append(j)
                if abs(entry.Jet_eta[j]) < 2.4 and entry.Jet_btagDeepFlavB[j] > bjet_discrFlav : bJetListFlav.append(j)
                jetList.append(j)

        return jetList, bJetList,bJetListFlav



    def getJetsJMEMV(self,entry,LepList,era, syst) :
        jetList, jetListFlav, jetListEta, jetListPt, bJetList, bJetListT, bJetListFlav = [], [], [], [], [], [], []
        #print 'will try', len(LepList)
        bjet_discr = 0.6321
        bjet_discrT = 0.8953
        bjet_discrFlav = 0.0614

        if str(era) == '2017' :
            bjet_discr = 0.4941
            bjet_discrT = 0.8001
        if str(era) == '2018' :
            bjet_discr = 0.4184
            bjet_discrT = 0.7527

        failJets=[]
        goodJets=[]
        bJetList=[]
        #if syst !='' : syst="_"+syst

        if 'nom' in syst : syst='_nom'

        for j in range(entry.nJet) :

            try :
                jpt = getattr(entry, "Jet_pt{0:s}".format(str(syst)), None)
                #if syst=='_nom' : print jpt[j],  entry.Jet_pt[j],  syst

                if entry.Jet_jetId[j]  < 2  : continue  #require tight jets
                if jpt[j] > 30 and jpt[j] < 50 and entry.Jet_puId[j]  < 4  : continue #loose jetPU_iD
                if str(era) == '2017'  and jpt[j] > 20 and jpt[j] < 50 and abs(entry.Jet_eta[j]) > 2.65 and abs(entry.Jet_eta[j]) < 3.139 : continue  #remove noisy jets
                if jpt[j] < 25. : continue
                if abs(entry.Jet_eta[j]) > 4.7 : continue

                #for iv, lepv in enumerate(LepList) :
                for iv, lv  in  enumerate(LepList) :
                    dr = self.getDRnV(entry, entry.Jet_eta[j], entry.Jet_phi[j], LepList[iv].Eta(), LepList[iv].Phi())
                    if float(dr) > 0.5 :
                        #print 'seems goodfor iv--->', iv, 'jet', j, entry.nJet, 'dr--', dr , LepList[iv].Eta(), LepList[iv].Phi(), LepList[iv].Pt()
                        if j not in goodJets : goodJets.append(j)
                    if float(dr) < 0.5 :
                        #print ' failed for lepton--->', iv, 'jet', j, 'njets', entry.nJet, 'dr--', dr , LepList[iv].Eta(), LepList[iv].Phi(), LepList[iv].Pt()
                        if j not in failJets : failJets.append(j)
                        #continue
            except : continue

        for j in failJets :
            if j in goodJets : goodJets.remove(j)


        for jj in goodJets :
            #if isMC :
            try :
                jetListFlav.append(entry.Jet_partonFlavour[jj])
            except AttributeError  : jetListFlav.append(0)
            jetListEta.append(entry.Jet_eta[jj])
            jpt = getattr(entry, "Jet_pt{0:s}".format(str(syst)), None)
            jetListPt.append(jpt[jj])


            if jpt[jj] > 25 :

                if abs(entry.Jet_eta[jj]) < 2.4 :
                    if entry.Jet_btagDeepB[jj] > bjet_discr : bJetList.append(jj)
                    if entry.Jet_btagDeepB[jj] > bjet_discrT : bJetListT.append(jj)
                    if entry.Jet_btagDeepFlavB[jj] > bjet_discrFlav : bJetListFlav.append(jj)
            if jpt[jj] > 30 :
                jetList.append(jj)

        return jetList, jetListFlav, jetListEta,  jetListPt, bJetList,bJetListT,bJetListFlav

    def Fill(self, entry, goodMuonList, goodPhotonList, goodElectronList, isMC, era, doUncertainties=False, met_pt=-99, met_phi=-99, systIndex=0):

        SystIndex = int(systIndex)


        #if SystIndex >0 : doUncertainties=False

        if SystIndex ==0 :

            is_trig_1, is_trig_2, is_Dtrig_1, is_Ttrig_1 = 0., 0., 0.,0.
            TrigListLep = []
            TrigListTau = []
            hltListLep  = []
            hltListLepT  = []
            hltListLepSubL  = []
            hltListLepSubSubL  = []

            self.entries += 1

            self.run[0]  = entry.run
            self.nElectron[0]  = entry.nElectron
            self.nMuon[0]  = entry.nMuon
            self.nTau[0]  = entry.nTau
            self.nPhoton[0]  = entry.nPhoton
            self.lumi[0] = entry.luminosityBlock
            self.evt[0]  = entry.event

            #dictionary relating the new names we'll use to the old ones used in nAOD.
            vnames = {}
            for fName in fNames:
                vnames[fName] = fName
            for lName in lNames:
                vnames[lName] = lName
            #only a few are different.
            vnames["idDTve"] = "idDeepTau2017v2p1VSe"
            vnames["idDTvm"] = "idDeepTau2017v2p1VSm"
            vnames["idDTvj"] = "idDeepTau2017v2p1VSjet"
            vnames["idDMNewDMs"] = "idDecayModeNewDMs"
            vnames["idMVANewDMs"] = "idMVAnewDM2017v2"
            vnames["rawMVANewDMs"] = "rawMVAnewDM2017v2"
            vnames["eMVA"] = "mvaFall17V2noIso_WP90"
            vnames["iso"] = "pfRelIso04_all" #this is for muons; change 4->3 for electrons!!

           # print("boutta initiate to -99")
            #particle-dependent variables
            for pType in pTypes:
                for vname in vnames.keys():
                    fullname = pType + "_" + vname
                    for i in range(nMax):
                        exec("self.%s[i] = -99"%(fullname))

            try:
                self.L1PreFiringWeight_Nom[0] = entry.L1PreFiringWeight_Nom
                self.L1PreFiringWeight_Up[0] = entry.L1PreFiringWeight_Up
                self.L1PreFiringWeight_Down[0] = entry.L1PreFiringWeight_Down
            except AttributeError :
                self.L1PreFiringWeight_Nom[0] = 1
                self.L1PreFiringWeight_Up[0] = 1
                self.L1PreFiringWeight_Down[0] = 1


            #separate out the LHE vs pileup info, because some files have one but not the other!
            #pileup
            try :
                self.weight[0]           = entry.genWeight
                self.Generator_weight[0] = entry.Generator_weight

                self.nPU[0]  = entry.Pileup_nPU
                self.nPUEOOT[0]  = entry.Pileup_sumEOOT
                self.nPULOOT[0]  = entry.Pileup_sumLOOT
                self.nPUtrue[0]  = entry.Pileup_nTrueInt
                self.nPV[0]  = entry.PV_npvs
                self.nPVGood[0]  = entry.PV_npvsGood

            except AttributeError:
                self.weight[0]           = 1.
                self.weightPU[0]         = -1
                self.weightPUtrue[0]     = -1
                self.Generator_weight[0] = 1.
                self.nPU[0]  = -1
                self.nPUEOOT[0]  = -1
                self.nPULOOT[0]  = -1
                self.nPUtrue[0]  = -1
                self.nPV[0]  = -1
                self.nPVGood[0]  = -1

            try:
                self.PV_x[0] = entry.PV_x
                self.PV_y[0] = entry.PV_y
                self.PV_z[0] = entry.PV_z 
                self.nOtherPV[0] = entry.nOtherPV
                for k in range(entry.nOtherPV):
                    self.OtherPV_z[k] = entry.OtherPV_z[k]
                for k in range(entry.nOtherPV, nMax):
                    self.OtherPV_z[k] = -9999.
            except AttributeError:
                self.PV_x[0] = -1.
                self.PV_x[0] = -1.
                self.PV_x[0] = -1.
                self.nOtherPV[0] = -1
                for k in range(nMax):
                    self.OtherPV_z = -9999.

            #LHE
            try:
                self.LHEweight[0]        = entry.LHEWeight_originalXWGTUP
                self.LHE_Njets[0]        = ord(entry.LHE_Njets)
                if SystIndex == 0 :
#                    print("nLHEScaleWeight: {}".format(int(entry.nLHEScaleWeight)))
                    for i in range(0, min(9, int(entry.nLHEScaleWeight))) :
#                        print("i={}, scaleWeight={}".format(i, entry.LHEScaleWeight[i]))
                        self.LHEScaleWeights[i] = entry.LHEScaleWeight[i]

            except AttributeError :
                self.LHEweight[0]        = 1.
                self.LHE_Njets[0] = -1

        e = entry

        '''
        List from Cecile
        single ele 2016: HLT Ele25 eta2p1 WPTight Gsf v and cut pt(ele)>26, eta(ele)<2.1
        single ele 2017: HLT Ele27 WPTight Gsf v, HLT Ele32 WPTight Gsf v, HLT Ele35 WPTight Gsf v and cut pt(ele)>28, eta(ele)<2.1
        single ele 2018: HLT Ele32 WPTight Gsf v, HLT Ele35 WPTight Gsf v and cut pt(ele)>33, eta(ele)<2.1
        '''

        #maximum number of bits for a single trigger word
        bitsPerWord = 14

        if int(SystIndex) ==0 :
            electronTrigList = ["Ele25_eta2p1_WPTight_Gsf", "Ele27_WPTight_Gsf", "Ele32_WPTight_Gsf", "Ele35_WPTight_Gsf", 
                         "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]
            '''
            List from Cecile
            single mu 2016: HLT IsoMu22 v, HLT IsoMu22 eta2p1 v, HLT IsoTkMu22 v, HLT IsoTkMu22 eta2p1 v and cut pt(mu)>23, eta(mu)<2.1
            single mu 2017: HLT IsoMu24 v, HLT IsoMu27 v and cut pt(mu)>25, eta(mu)<2.4
            single mu 2018: HLT IsoMu24 v, HLT IsoMu27 v and cut pt(mu)>25, eta(mu)<2.4
            '''
            '''
            In order to find the right bit when selecting later ... use bitwise And & along with the bit-word ie ... 2^{bit placement} ex: if third 2^3 = 8
            '''
            muonTrigList = ["IsoMu22", "IsoMu22_eta2p1", "IsoTkMu22", "IsoTkMu22_eta2p1", "IsoMu24", "IsoMu27", "TripleMu_12_10_5",
                          "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ", "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8", "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
                          "Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", "Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_Mass8"]

        #    dimuTrigList = ["Dimuon0_Jpsi", "Dimuon0_Jpsi3p5_Muon2", "Dimuon0_LowMass", "DoubleMu2_Jpsi_DoubleTrk1_Phi1p05",
        #                    "Trimuon5_3p5_2_Upsilon_Muon", "TrimuonOpen_5_3p5_2_Upsilon_Muon", "TripleMu_10_5_5_DZ",
        #                    "TripleMu_12_10_5", "TripleMu_5_3_3_Mass3p8_DCA", "TripleMu_5_3_3_Mass3p8_DZ" ]
            dimuTrigList = muFun.doubleMuonTriggers(str(era))

            #now make the 3 different triggerWord numbers
            # trigger words are stored as an int where each bit is a different HLT bit
            for trigN in ["electron", "muon", "dimu"]:
                exec("trigList = %sTrigList"%(trigN))
                bits=[]
                #which number word are we on (don't want too many bits in one word)
                wordn = 0
                error = AttributeError
                for k,tname in enumerate(trigList):
                    #bstat = e.GetBranchStatus("HLT_%s"%tname)
                    #print("branch status for %s: %s"%(tname, str(bstat)))
                    #e.SetBranchStatus("HLT_%s"%tname, True)
                    #print("new branch status for %s: %s"%(tname, str(bstat)))
                    #if tname == "DoubleL2Mu50": error = KeyError
                    try:
                        exec("bits.append(bool(e.HLT_%s))"%(tname))
                        #print("HLT_%s found!"%(tname))
                    except error:
                        #print("HLT_%s not found."%(tname))
                        bits.append(False)

                    if k % bitsPerWord == (bitsPerWord-1) or k == (len(trigList)-1):
                        #first fill in the remaining bits with False (if needed)
                        for k in range (len(trigList), (wordn+1)*bitsPerWord):
                            bits.append(False)
                        #print("final bits for " + trigN + " word " + str(wordn) + ": " + str(bits))
                        triggerWord = 0
                        for i, bit in enumerate(bits) :
                            if bit : triggerWord += 2**i
                        #print("final triggerWord for " + trigN + " word " + str(wordn) + ": " + str(triggerWord))
                        exec("self.%sTriggerWord[%d] = triggerWord"%(trigN, wordn))
                        wordn += 1
                        bits = []
 
        #print("boutta fill fr")
        #now go through the particle lists (of good particles) and fill in the particle-dependent info.
        for pType in pTypes:
            exec("goodList = good%sList"%(pType))
            ngood = len(goodList)
            if ngood > nMax:
                print("Error: nMax is only %d but we have %d good %s!"%(nMax, ngood, pType))
                sys.exit()
            exec("self.nGood%s[0] = ngood"%(pType))
            for vname in vnames.keys():
                fullname = pType + "_" + vname   
                #name in the nanoAOD
                nanoname = pType + "_" + vnames[vname]
                for j in range(ngood):
                    #this doesn't work for some variables/particles; just skip those
                    #print("var: {} nanovar: {} j: {} goodList: {}".format(fullname, nanoname, j, str(goodList)))
                    try:
                        exec("self.%s[j] = e.%s[goodList[j]]"%(fullname, nanoname))
                    except AttributeError:
                        break
                
            # Fill genMatch variables
            if isMC:
                for j in range(ngood):
                    exec("idx_gen = entry.%s_genPartIdx[j]"%(pType))

                    # if idx_genMu = -1, no match was found
                    if idx_gen >= 0:
                        idx_gen_mom      = entry.GenPart_genPartIdxMother[idx_gen]
                        exec("self.%s_pt_tr[j]     = entry.GenPart_pt[idx_gen]"%(pType))  
                        exec("self.%s_phi_tr[j]    = entry.GenPart_phi[idx_gen]"%(pType)) 
                        exec("self.%s_eta_tr[j]    = entry.GenPart_eta[idx_gen]"%(pType)) 
                        exec("self.%s_GenPart_statusFlags[j]    = entry.GenPart_statusFlags[idx_gen]"%(pType))
                        exec("self.%s_GenPart_status[j]    = entry.GenPart_status[idx_gen]"%(pType))

                    try: exec("self.{0:s}_gen_match[j] = ord(entry.{0:s}_genPartFlav[jt1])".format(pType))
                    except AttributeError: exec("self.%s_gen_match[j] = -1"%(pType))

        if str(era) != '2017' :
            self.metNoCor[0]= entry.MET_pt
            self.metphiNoCor[0]= entry.MET_phi
        if str(era) == '2017' :
            #self.metNoCor[0]= entry.METFixEE2017_pt
            #self.metphiNoCor[0]= entry.METFixEE2017_phi
            self.metNoCor[0]= entry.MET_pt
            self.metphiNoCor[0]= entry.MET_phi

        #print 'inside', met_pt, entry.MET_pt, entry.MET_T1_pt, entry.event, entry.luminosityBlock, entry.run

        if met_pt != -99 :
            self.met[0]         = met_pt
            self.metphi[0]      = met_phi

        else :
            if not doUncertainties :
                if str(era) != '2017' :
                    self.met[0]= met_pt # entry.met_pt
                    self.metphi[0]= met_phi #entry.met_phi
                if str(era) == '2017' :
                    #self.met[0]= entry.METFixEE2017_pt
                    #self.metphi[0]= entry.METFixEE2017_phi
                    self.met[0]= met_pt #entry.met_pt
                    self.metphi[0]= met_phi #entry.met_phi
            if  doUncertainties :

                if str(era) != '2017' :
                    try :
                        self.met[0]= entry.MET_T1_pt
                        self.metphi[0]= entry.MET_T1_phi
                    except AttributeError :
                        self.met[0]= entry.MET_pt
                        self.metphi[0]= entry.MET_phi

                if str(era) == '2017' :
                    try :
                        self.met[0]= entry.METFixEE2017_T1_pt
                        self.metphi[0]= entry.METFixEE2017_T1_phi
                    except AttributeError :
                        self.met[0]= entry.MET_pt
                        self.metphi[0]= entry.MET_phi
                        #self.met[0]= entry.METFixEE2017_pt
                        #self.metphi[0]= entry.METFixEE2017_phi

        #metNoTauES holds the uncorrected TauES MET - if not doUncerta -> holds the default ucorrected MET, if doUncert the T1_corrected

        if str(era) != '2017' :
            self.metNoTauES[0]         = entry.MET_pt
            self.metphiNoTauES[0]         = entry.MET_phi

            if doUncertainties :
                try :
                    self.metNoTauES[0]         = entry.MET_T1_pt
                    self.metphiNoTauES[0]         = entry.MET_T1_phi
                except AttributeError :
                    self.metNoTauES[0]         = entry.MET_pt
                    self.metphiNoTauES[0]         = entry.MET_phi

                if isMC :
                    try :
                        self.MET_T1Smear_pt[0]         = entry.MET_T1Smear_pt
                        self.MET_T1Smear_phi[0]         = entry.MET_T1Smear_phi
                    except AttributeError :
                        self.MET_T1Smear_pt[0]         = -99
                        self.MET_T1Smear_phi[0]         = -99

        if str(era) == '2017' :
            #self.metNoTauES[0]         = entry.METFixEE2017_pt
            #self.metphiNoTauES[0]         = entry.METFixEE2017_phi
            self.metNoTauES[0]         = entry.MET_pt
            self.metphiNoTauES[0]         = entry.MET_phi

            if doUncertainties :
                try :
                    self.metNoTauES[0]         = entry.METFixEE2017_T1_pt
                    self.metphiNoTauES[0]         = entry.METFixEE2017_T1_phi
                except AttributeError :
                    self.metNoTauES[0]         = entry.METFixEE2017_pt_nom
                    self.metphiNoTauES[0]         = entry.METFixEE2017_phi_nom
                if isMC :
                    try :
                        self.MET_T1Smear_pt[0]         = entry.METFixEE2017_T1Smear_pt
                        self.MET_T1Smear_phi[0]         = entry.METFixEE2017_T1Smear_phi
                    except AttributeError :
                        self.MET_T1Smear_pt[0]         = -1
                        self.MET_T1Smear_phi[0]         = -1


        #print 'in NTUPLE ============================== met_pt', met_pt, 'met', self.met[0], 'metnoTauES', self.metNoTauES[0], 'met_T1', entry.MET_T1_pt, 'met_T1Smear', entry.MET_T1Smear_pt, 'doUncert ?', doUncertainties

        if str(era) != '2017' :

            self.metcov00[0] = entry.MET_covXX
            self.metcov01[0] = entry.MET_covXY
            self.metcov10[0] = entry.MET_covXY
            self.metcov11[0] = entry.MET_covYY
            self.met_UnclX = entry.MET_MetUnclustEnUpDeltaX
            self.met_UnclY = entry.MET_MetUnclustEnUpDeltaY

            if doUncertainties :
                if isMC :
                    self.MET_pt_UnclUp[0] = entry.MET_pt_unclustEnUp
                    self.MET_phi_UnclUp[0] = entry.MET_phi_unclustEnUp
                    self.MET_pt_UnclDown[0] = entry.MET_pt_unclustEnDown
                    self.MET_phi_UnclDown[0] = entry.MET_phi_unclustEnDown
        else :
            self.metcov00[0] = entry.METFixEE2017_covXX
            self.metcov01[0] = entry.METFixEE2017_covXY
            self.metcov10[0] = entry.METFixEE2017_covXY
            self.metcov11[0] = entry.METFixEE2017_covYY
            self.met_UnclX = entry.METFixEE2017_MetUnclustEnUpDeltaX
            self.met_UnclY = entry.METFixEE2017_MetUnclustEnUpDeltaY

            if doUncertainties :
                if isMC :
                    self.MET_pt_UnclUp[0] = entry.METFixEE2017_pt_unclustEnUp
                    self.MET_phi_UnclUp[0] = entry.METFixEE2017_phi_unclustEnUp
                    self.MET_pt_UnclDown[0] = entry.METFixEE2017_pt_unclustEnDown
                    self.MET_phi_UnclDown[0] = entry.METFixEE2017_phi_unclustEnDown

        #leplist is need for the systematics stuff below.
        # using all 'good' muons--is this right???
        #  (bc 'good' is very very loose at this point.)
        leplist=[]
        #print("nGoodMuon: " + str(self.nGoodMuon))
        for j in goodMuonList:
            fourvec = muFun.get4vec('m', e, j)    
            leplist.append(fourvec)

        if doUncertainties:
                ## this is not done from within ZH and the correctallMET function
                for i, v in enumerate(self.allsystMET) :

                    if str(era)=='2017' :
                        #i_ should be the righ-hand of the branch and should retain the METFixEE2017 if y=2017
                        #iMET should appear always at the branch name...
                        v = v.replace('MET','METFixEE2017')
                    iMET= v.replace('METFixEE2017','MET')

                    try : j = getattr(entry, "{0:s}".format(str(v)))
                    except AttributeError : j = -9.99
                    self.list_of_arrays_noES[i][0] = j
                    #if '_pt_jerUp' in v  : print '=====================================while filling-----------------',j, self.list_of_arrays[i][0], i, v, entry.event

                for i, v in enumerate(self.allsystJets) :
                #njets_sys, nbtag_sys
                    jetList, jetListFlav, jetListEta, jetListPt,bJetList, bJetListT, bJetListFlav = self.getJetsJMEMV(entry,leplist,era,v)

                    self.list_of_arraysJetsNjets[i][0] = len(jetList)
                    self.list_of_arraysJetsNbtag[i][0] = len(bJetList)
                    for ifl in range(len(jetList)) :
                        self.list_of_arraysJetsPt[i][ifl] = jetListPt[ifl]
                        self.list_of_arraysJetsEta[i][ifl] = jetListEta[ifl]
                        self.list_of_arraysJetsFlavour[i][ifl] = jetListFlav[ifl]


        #fill the un-corrected or just in the case you dont care to doUncertainties
        nom_=''
        jetList, jetListFlav, jetListEta, jetListPt,bJetList, bJetListT, bJetListFlav = self.getJetsJMEMV(entry,leplist,era,'')
        self.njets[0] = len(jetList)
        self.nbtag[0] = len(bJetList)
        #bpg added min to avoid oob error
        for ifl in range(min(15, len(jetListPt))) :
            self.jflavour[ifl]  = jetListFlav[ifl]
            self.jeta[ifl]  = jetListEta[ifl]
            self.jpt[ifl]  = jetListPt[ifl]

        #if  self.nbtag[0] == 0 :
        if SystIndex == 0 :
            self.t.Fill()
        else :
            self.tN[SystIndex-1].Fill()

        return

    def setWeight(self,weight) :
        self.weight[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return
    def setWeightPU(self,weight) :
        self.weightPU[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return
    def setWeightPUtrue(self,weight) :
        self.weightPUtrue[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return

    def FillTree(self) :
        self.t.Fill()

    def writeTree(self) :
        print("In outTuple.writeTree() entries={0:d}".format(self.entries))
        self.f.Write()
        self.f.Close()
        return
