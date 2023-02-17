import ROOT

mode = "trig"
#reco or trigger eff
reco = mode == "both" or mode == "reco" #True
trig = mode == "both" or mode == "trig" #True

#need xsec to get overall weighted eff
f_xsec = ROOT.TFile.Open("/uscms_data/d3/bgreenbe/CMSSW_10_2_9/src/tm_analysis/analysis/data_out/xsecs.root")
h_xsec = f_xsec.Get("corr_xsec")
#counting the weights
all_weight = 0.
passed_weight = 0.

#just counting the unweighted events
nall = 0
npassed = 0

#make histogram for pT of all Events
h_all = ROOT.TH1F("hall", "hall", 65, 0.0, 65.0)
h_passed = ROOT.TH1F("hpassed", "hpassed", 65, 0.0, 65.0)
h_passed.Sumw2()

import glob
#for g in glob.glob("EtaToMuMuGamma*.root"):
for g in glob.glob("/eos/uscms/store/user/bgreenbe/EtaToMuMuGamma/NANOAOD_Signal_Samples/EtaToMuMuGamma*.root"):
    print("Working on file %s"%(g)) 

    f = ROOT.TFile(g, "read")

    t = f.Get("Events") 
    
    #if t is empty (eg, file doesn't exist), continue
    if not t: 
        continue

    for i,e in enumerate(t):
        if i%10000 == 0: print("event %d"%i) 
        etavec = ROOT.TLorentzVector()
        tlv = [ROOT.TLorentzVector() for j in range(3)] 
        for j in range(3):
            #if abs(e.GenPart_pdgId[j]) == 11:
            #    mass = .00511
            if e.GenPart_pdgId[j] == 221:
                mass = 0
            elif abs(e.GenPart_pdgId[j]) == 13:
                mass = .105
            else:
                print("Error!!! Unrecognized pdgId: %d"%e.GenPart_pdgId[j]) 
                exit()
            tlv[j].SetPtEtaPhiM( e.GenPart_pt[j], e.GenPart_eta[j], e.GenPart_phi[j], mass )
        etavec = tlv[0] + tlv[1] + tlv[2]
        h_all.Fill(etavec.Pt()) 

        xsec = h_xsec.GetBinContent( h_xsec.FindBin( etavec.Pt() ) )
        all_weight += xsec
        nall += 1

        passed_reco = False
        if reco:
            if e.nMuon > 1 and e.nElectron > 1:
                if mode == "reco":
                    h_passed.Fill( etavec.Pt() ) 
                    passed_weight += xsec
                    npassed += 1
                passed_reco = True
        #else:
        if trig:
            #trigger eff instead of reco
            doubleMubits = ['HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL', 'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon', 'HLT_Mu27_Ele37_CaloIdL_MW', 'HLT_Mu37_Ele27_CaloIdL_MW', 'HLT_Mu37_TkMu27', 'HLT_DoubleMu4_3_Bs', 'HLT_DoubleMu4_3_Jpsi', 'HLT_DoubleMu4_JpsiTrk_Displaced', 'HLT_DoubleMu4_LowMassNonResonantTrk_Displaced', 'HLT_DoubleMu3_Trk_Tau3mu', 'HLT_DoubleMu3_TkMu_DsTau3Mu', 'HLT_DoubleMu4_PsiPrimeTrk_Displaced', 'HLT_DoubleMu4_Mass3p8_DZ_PFHT350', 'HLT_Mu3_PFJet40', 'HLT_Mu7p5_L2Mu2_Jpsi', 'HLT_Mu7p5_L2Mu2_Upsilon', 'HLT_Mu7p5_Track2_Jpsi', 'HLT_Mu7p5_Track3p5_Jpsi', 'HLT_Mu7p5_Track7_Jpsi', 'HLT_Mu7p5_Track2_Upsilon', 'HLT_Mu7p5_Track3p5_Upsilon', 'HLT_Mu7p5_Track7_Upsilon', 'HLT_Mu3_L1SingleMu5orSingleMu7', 'HLT_L2Mu10', 'HLT_L2Mu10_NoVertex_NoBPTX3BX', 'HLT_L2Mu10_NoVertex_NoBPTX', 'HLT_L2Mu45_NoVertex_3Sta_NoBPTX3BX', 'HLT_L2Mu40_NoVertex_3Sta_NoBPTX3BX', 'HLT_L2Mu50', 'HLT_L2Mu23NoVtx_2Cha', 'HLT_L2Mu23NoVtx_2Cha_CosmicSeed', 'HLT_DoubleL2Mu30NoVtx_2Cha_CosmicSeed_Eta2p4', 'HLT_DoubleL2Mu30NoVtx_2Cha_Eta2p4', 'HLT_DoubleL2Mu50', 'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed', 'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched', 'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed', 'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched', 'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4', 'HLT_DoubleL2Mu23NoVtx_2Cha', 'HLT_DoubleL2Mu23NoVtx_2Cha_NoL2Matched', 'HLT_DoubleL2Mu25NoVtx_2Cha', 'HLT_DoubleL2Mu25NoVtx_2Cha_NoL2Matched', 'HLT_DoubleL2Mu25NoVtx_2Cha_Eta2p4', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL', 'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8', 'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8', 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8', 'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8', 'HLT_Mu25_TkMu0_Onia', 'HLT_Mu30_TkMu0_Psi', 'HLT_Mu30_TkMu0_Upsilon', 'HLT_Mu20_TkMu0_Phi', 'HLT_Mu25_TkMu0_Phi', 'HLT_Mu12', 'HLT_Mu15', 'HLT_Mu20', 'HLT_Mu27', 'HLT_Mu50', 'HLT_Mu55', 'HLT_Mu12_DoublePFJets40_CaloBTagDeepCSV_p71', 'HLT_Mu12_DoublePFJets100_CaloBTagDeepCSV_p71', 'HLT_Mu12_DoublePFJets200_CaloBTagDeepCSV_p71', 'HLT_Mu12_DoublePFJets350_CaloBTagDeepCSV_p71', 'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagDeepCSV_p71', 'HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagDeepCSV_p71', 'HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagDeepCSV_p71', 'HLT_Mu8_TrkIsoVVL', 'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ', 'HLT_Mu8_DiEle12_CaloIdL_TrackIdL', 'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ', 'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_CaloDiJet30', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepCSV_1p5', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_CaloDiJet30_CaloBtagDeepCSV_1p5', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu17_TrkIsoVVL', 'HLT_Mu19_TrkIsoVVL', 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Mu12_DoublePhoton20', 'HLT_TripleMu_5_3_3_Mass3p8_DZ', 'HLT_TripleMu_10_5_5_DZ', 'HLT_TripleMu_12_10_5', 'HLT_DoubleMu3_DZ_PFMET50_PFMHT60', 'HLT_DoubleMu3_DZ_PFMET70_PFMHT70', 'HLT_DoubleMu3_DZ_PFMET90_PFMHT90', 'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass', 'HLT_DoubleMu4_Jpsi_Displaced', 'HLT_DoubleMu4_Jpsi_NoVertexing', 'HLT_DoubleMu4_JpsiTrkTrk_Displaced', 'HLT_DoubleMu43NoFiltersNoVtx', 'HLT_DoubleMu48NoFiltersNoVtx', 'HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL', 'HLT_Mu48NoFiltersNoVtx_Photon48_CaloIdL', 'HLT_Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL', 'HLT_Mu43NoFiltersNoVtxDisplaced_Photon43_CaloIdL', 'HLT_DoubleMu33NoFiltersNoVtxDisplaced', 'HLT_DoubleMu40NoFiltersNoVtxDisplaced', 'HLT_DoubleMu20_7_Mass0to30_L1_DM4', 'HLT_DoubleMu20_7_Mass0to30_L1_DM4EG', 'HLT_DoubleMu20_7_Mass0to30_Photon23', 'HLT_Mu4_TrkIsoVVL_DiPFJet90_40_DEta3p5_MJJ750_HTT300_PFMETNoMu60', 'HLT_Mu8_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT300_PFMETNoMu60', 'HLT_Mu10_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT350_PFMETNoMu60', 'HLT_Mu15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5', 'HLT_Mu15_IsoVVVL_PFHT450_PFMET50', 'HLT_Mu15_IsoVVVL_PFHT450', 'HLT_Mu50_IsoVVVL_PFHT450', 'HLT_Mu15_IsoVVVL_PFHT600', 'HLT_Mu3er1p5_PFJet100er2p5_PFMET70_PFMHT70_IDTight', 'HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight', 'HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight', 'HLT_Mu3er1p5_PFJet100er2p5_PFMET100_PFMHT100_IDTight', 'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu70_PFMHTNoMu70_IDTight', 'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu80_PFMHTNoMu80_IDTight', 'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu90_PFMHTNoMu90_IDTight', 'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu100_PFMHTNoMu100_IDTight', 'HLT_TrkMu12_DoubleTrkMu5NoFiltersNoVtx', 'HLT_TrkMu16_DoubleTrkMu6NoFiltersNoVtx', 'HLT_TrkMu17_DoubleTrkMu8NoFiltersNoVtx', 'HLT_Mu8', 'HLT_Mu17', 'HLT_Mu19', 'HLT_Mu17_Photon30_IsoCaloId', 'HLT_Mu18_Mu9_SameSign', 'HLT_Mu18_Mu9_SameSign_DZ', 'HLT_Mu18_Mu9', 'HLT_Mu18_Mu9_DZ', 'HLT_Mu20_Mu10_SameSign', 'HLT_Mu20_Mu10_SameSign_DZ', 'HLT_Mu20_Mu10', 'HLT_Mu20_Mu10_DZ', 'HLT_Mu23_Mu12_SameSign', 'HLT_Mu23_Mu12_SameSign_DZ', 'HLT_Mu23_Mu12', 'HLT_Mu23_Mu12_DZ', 'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05', 'HLT_DoubleMu2_Jpsi_DoubleTkMu0_Phi', 'HLT_DoubleMu3_DCA_PFMET50_PFMHT60', 'HLT_TripleMu_5_3_3_Mass3p8_DCA', 'HLT_Mu12_IP6_part0', 'HLT_Mu12_IP6_part1', 'HLT_Mu12_IP6_part2', 'HLT_Mu12_IP6_part3', 'HLT_Mu12_IP6_part4', 'HLT_Mu9_IP5_part0', 'HLT_Mu9_IP5_part1', 'HLT_Mu9_IP5_part2', 'HLT_Mu9_IP5_part3', 'HLT_Mu9_IP5_part4', 'HLT_Mu7_IP4_part0', 'HLT_Mu7_IP4_part1', 'HLT_Mu7_IP4_part2', 'HLT_Mu7_IP4_part3', 'HLT_Mu7_IP4_part4', 'HLT_Mu9_IP4_part0', 'HLT_Mu9_IP4_part1', 'HLT_Mu9_IP4_part2', 'HLT_Mu9_IP4_part3', 'HLT_Mu9_IP4_part4', 'HLT_Mu8_IP5_part0', 'HLT_Mu8_IP5_part1', 'HLT_Mu8_IP5_part2', 'HLT_Mu8_IP5_part3', 'HLT_Mu8_IP5_part4', 'HLT_Mu8_IP6_part0', 'HLT_Mu8_IP6_part1', 'HLT_Mu8_IP6_part2', 'HLT_Mu8_IP6_part3', 'HLT_Mu8_IP6_part4', 'HLT_Mu9_IP6_part0', 'HLT_Mu9_IP6_part1', 'HLT_Mu9_IP6_part2', 'HLT_Mu9_IP6_part3', 'HLT_Mu9_IP6_part4', 'HLT_Mu8_IP3_part0', 'HLT_Mu8_IP3_part1', 'HLT_Mu8_IP3_part2', 'HLT_Mu8_IP3_part3', 'HLT_Mu8_IP3_part4', 'HLT_TrkMu6NoFiltersNoVtx', 'HLT_TrkMu16NoFiltersNoVtx', 'HLT_DoubleMu33NoFiltersNoVtx', 'HLT_DoubleMu38NoFiltersNoVtx', 'HLT_DoubleMu23NoFiltersNoVtxDisplaced', 'HLT_DoubleMu28NoFiltersNoVtxDisplaced', 'HLT_DoubleMu4_3_Jpsi_Displaced', 'HLT_Mu16_eta2p1_MET30', 'HLT_L2DoubleMu23_NoVertex', 'HLT_L2DoubleMu28_NoVertex_2Cha_Angle2p5_Mass10', 'HLT_L2DoubleMu38_NoVertex_2Cha_Angle2p5_Mass10', 'HLT_L2Mu35_NoVertex_3Sta_NoBPTX3BX', 'HLT_Mu17_Mu8', 'HLT_Mu17_Mu8_DZ', 'HLT_Mu17_Mu8_SameSign_DZ', 'HLT_Mu17_TkMu8_DZ', 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL', 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ', 'HLT_Mu25_TkMu0_dEta18_Onia', 'HLT_Mu27_TkMu8', 'HLT_Mu30_TkMu11', 'HLT_Mu30_eta2p1_PFJet150_PFJet50', 'HLT_Mu40_TkMu11', 'HLT_Mu40_eta2p1_PFJet200_PFJet50', 'HLT_Mu24_eta2p1', 'HLT_Mu45_eta2p1', 'HLT_Mu38NoFiltersNoVtx_Photon38_CaloIdL', 'HLT_Mu42NoFiltersNoVtx_Photon42_CaloIdL', 'HLT_Mu28NoFiltersNoVtxDisplaced_Photon28_CaloIdL', 'HLT_Mu33NoFiltersNoVtxDisplaced_Photon33_CaloIdL', 'HLT_Mu23NoFiltersNoVtx_Photon23_CaloIdL', 'HLT_DoubleMu18NoFiltersNoVtx', 'HLT_Mu33NoFiltersNoVtxDisplaced_DisplacedJet50_Tight', 'HLT_Mu33NoFiltersNoVtxDisplaced_DisplacedJet50_Loose', 'HLT_Mu28NoFiltersNoVtx_DisplacedJet40_Loose', 'HLT_Mu38NoFiltersNoVtxDisplaced_DisplacedJet60_Tight', 'HLT_Mu38NoFiltersNoVtxDisplaced_DisplacedJet60_Loose', 'HLT_Mu38NoFiltersNoVtx_DisplacedJet60_Loose', 'HLT_Mu28NoFiltersNoVtx_CentralCaloJet40', 'HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL', 'HLT_Mu37_Ele27_CaloIdL_GsfTrkIdVL', 'HLT_Mu27_Ele37_CaloIdL_GsfTrkIdVL', 'HLT_Mu12_Photon25_CaloIdL', 'HLT_Mu12_Photon25_CaloIdL_L1ISO', 'HLT_Mu12_Photon25_CaloIdL_L1OR', 'HLT_Mu17_Photon22_CaloIdL_L1ISO', 'HLT_Mu17_Photon30_CaloIdL_L1ISO', 'HLT_Mu17_Photon35_CaloIdL_L1ISO', 'HLT_Mu3er_PFHT140_PFMET125', 'HLT_Mu6_PFHT200_PFMET80_BTagCSV_p067', 'HLT_Mu6_PFHT200_PFMET100', 'HLT_Mu14er_PFMET100', 'HLT_DoubleMu8_Mass8_PFHT250', 'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT250', 'HLT_DoubleMu8_Mass8_PFHT300', 'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT300', 'HLT_Mu10_CentralPFJet30_BTagCSV_p13', 'HLT_Mu15_IsoVVVL_BTagCSV_p067_PFHT400', 'HLT_Mu15_IsoVVVL_PFHT350_PFMET50', 'HLT_Mu15_IsoVVVL_PFHT350', 'HLT_Mu16_TkMu0_dEta18_Onia', 'HLT_Mu16_TkMu0_dEta18_Phi', 'HLT_TrkMu15_DoubleTrkMu5NoFiltersNoVtx', 'HLT_Mu300', 'HLT_Mu350', 'HLT_Mu17_Mu8_SameSign', 'HLT_TripleMu_5_3_3', 'HLT_DoubleMu3_PFMET50', 'HLT_Mu15_IsoVVVL_PFHT400_PFMET50', 'HLT_Mu15_IsoVVVL_PFHT400', 'HLT_Mu50_IsoVVVL_PFHT400', 'HLT_Mu30_TkMu0_Onia', 'HLT_DoubleMu4_Mass8_DZ_PFHT350', 'HLT_DoubleMu8_Mass8_PFHT350', 'HLT_Mu12_DoublePFJets40_CaloBTagCSV_p79', 'HLT_Mu12_DoublePFJets100_CaloBTagCSV_p79', 'HLT_Mu12_DoublePFJets200_CaloBTagCSV_p79', 'HLT_Mu12_DoublePFJets350_CaloBTagCSV_p79', 'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagCSV_p79', 'HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagCSV_p79', 'HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagCSV_p79', 'HLT_TripleMu_5_3_3_Mass3p8to60_DZ', 'HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5', 'HLT_TripleMu_5_3_3_Mass3p8to60_DCA', 'HLT_Mu8p5_IP3p5_part0', 'HLT_Mu8p5_IP3p5_part1', 'HLT_Mu8p5_IP3p5_part2', 'HLT_Mu8p5_IP3p5_part3', 'HLT_Mu8p5_IP3p5_part4', 'HLT_Mu8p5_IP3p5_part5', 'HLT_Mu10p5_IP3p5_part0', 'HLT_Mu10p5_IP3p5_part1', 'HLT_Mu10p5_IP3p5_part2', 'HLT_Mu10p5_IP3p5_part3', 'HLT_Mu10p5_IP3p5_part4', 'HLT_Mu10p5_IP3p5_part5', 'HLT_Mu9_IP6_part5', 'HLT_Mu8_IP3_part5']
            passed_trig = False
            for dmb in doubleMubits:
                try:
                    exec("p = e.%s"%(dmb))
                except AttributeError:
                    continue
                if p > 0:
                    passed_trig = True
                    break
            if passed_trig:
                if mode == "trig" or passed_reco:
                    h_passed.Fill( etavec.Pt() ) 
                    passed_weight += xsec
                    npassed += 1
        
#write hists to file so can plot again later
outname = "%sEffBkg.root"%("combined" if mode == "both" else mode)
outf = ROOT.TFile.Open(outname, "recreate")
h_passed.Write()
h_all.Write()
    
if reco:
    h_passed.Rebin(5)
    h_all.Rebin(5)
h_passed.Divide(h_all)

modename = "Combined" if mode == "both" else mode
h_passed.SetTitle("%s efficiency vs. pT"%modename) 
#if reco:
#    h_passed.SetTitle("Reco efficiency vs. pT") 
#else:
#    h_passed.SetTitle("Trigger efficiency vs. pT") 
h_passed.GetXaxis().SetTitle("eta Gen pT (GeV)") 
h_passed.Draw()
tot_eff = passed_weight / all_weight
print("Total Bkg %s efficiency: %f"%(modename, tot_eff)) 
unw8deff = 1.0*npassed / nall
print("UNWEIGHTED Bkg %s eff: %f"%(modename, unw8deff)) 
raw_input("press enter to exit. regards.") 
