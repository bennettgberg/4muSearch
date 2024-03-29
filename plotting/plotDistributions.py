import ROOT, sys, time
sys.path.insert(1,'../code/')
import muFun
import argparse, os
from array import array

#this script will make 'ultra-skimmed' ntuples out of the ntuples I already have.
# Will save only important things that can be easily plotted, such as M4L of the 4 best
#  muons; weights for each MC event; etc.

#allow multiple mmee quadruplets per event or nah??
multiquad = False

#highest, lowest invariant Mass to keep
#maxM = 99999999.0 # 2.0
maxM = 2.0
minM = 0.0

#blinded = False

#fileName = #"data_DoubleMuonB_skimmed_2017.root"
#name = sys.argv[1].split(".")[0]
def makeskim(filename, yr, path, nevent, nickname, debug=False, condor=False, isMC=False, blinded=False):
    if yr not in [2016, 2017, 2018]:
        print("Error: only Run2 (2016,2017,2018) allowed for now.")
        sys.exit()
    name = filename.split(".")[0]
    fileName = name + "_skimmed" + nickname + ".root"
    hname = 'h' + name

    outF = ROOT.TFile( fileName, 'recreate' )
    #have to create this before opening the file fsr??
    newT = ROOT.TTree( 'Events', 'Output tree' )

    #need the passed_trig, passed_reco hists for making the trig, reco eff's
    hpassedReco = ROOT.TH1F( 'passedReco', 'passedReco', 65, 0.0, 65.0 ) 
    hpassedTrig = ROOT.TH1F( 'passedTrig', 'passedTrig', 65, 0.0, 65.0 ) 
    hwpt2 = ROOT.TH1F("hWeightPt", "hWeightPt", 65, 0.0, 65.0)
    hwpt2.Write()

    #max number of dimu pairs to keep
    # (keep nMax^2 4-lepton pairpairs)
    nMax = 12 #2
    #how many quadruplets to keep
    nquad = 1
    #cat 0: mmmm
    #cat 1: mmee
    if multiquad: nquad = nMax**2
    #m2l = array('f', [0]*nMax)
    #m2e = array('f', [0]*nMax)
#    m4l = array('f', [0]*nMax)

    #weight for MC
    mcweight = array('f', [0])

    #4mu mass
    mmmmm = array('f', [0])
    #invariant mass of the mmee system
    mmmee = array('f', [0])
    mmmg = array('f', [0]*nMax)
    ptmmg = array('f', [0]*nMax)
    #sum of the 2 photon dR distances (b/t each of the muons)
    PhodR = array('f', [0]*nMax)
    Qmmg = array('f', [0]*nMax)
    #pt2l = array('f', [0]*nMax)
    #pt2e = array('f', [0]*nMax)
    #pt4l = array('f', [0]*nMax)
    ptmmmm = array('f', [0])
    etammmm = array('f', [0])
    phimmmm = array('f', [0])
    ptmmee = array('f', [0])
    etammee = array('f', [0])
    phimmee = array('f', [0])
    Qmmee = array('f', [0])
    Qmmmm = array('f', [0])
    event = array('l', [0])
    run = array('l', [0])
    Nmmmm = array('l', [0])
    Nmmee = array('l', [0])
    #mu mu gamma
    Nmmg = array('l', [0])
    #new: info for the mumu pair of the mmg.
    ptmm = array('f', [0])
    ptee = array('f', [0])
    ptm = array('f', [0]*2)
    pte = array('f', [0]*2)
    ip3dm = array('f', [0]*2)
    dxym = array('f', [0]*2)
    dzm = array('f', [0]*2)
    ip3de = array('f', [0]*2)
    dxye = array('f', [0]*2)
    dze = array('f', [0]*2)
    mmm = array('f', [0])
    mee = array('f', [0])
    #DeltaR for each dimuon pair (relevant for mmg)
    drmm = array('f', [0])
    #difference in 3-d impact parameter for each dimuon pair
    dipmm = array('f', [0])
    #tightId of the 2 muons, stored as a binary number
    tightmm = array('l', [0]) 
    #total number of mmg trios that could have been made
    NAllmmg = array('l', [0])
    #number of trigger words (integers for storing trigger passing info)
    nwords = 4
    triggerWord = array('l', [0]*nwords)
    #newT.Branch("M2l", m2l, "M2l[%d]/F"%(nMax))
    #newT.Branch("M2e", m2e, "M2e[%d]/F"%(nMax))
    #newT.Branch("Mmmmm", mmmmm, "Mmmmm[%d]/F"%(nquad))
    #newT.Branch("Mmmee", mmmee, "Mmmee[%d/F"%(nquad))
    newT.Branch("Mmmmm", mmmmm, "Mmmmm/F")
    newT.Branch("Mmmee", mmmee, "Mmmee/F")
   # newT.Branch("Pt2l", pt2l, "Pt2l[%d]/F"%(nquad))
   # newT.Branch("Pt2e", pt2e, "Pt2e[%d]/F"%(nquad))
    genetapt = array('f', [0]) 
    newT.Branch("GenEtaPt", genetapt, "GenEtaPt/F")
    newT.Branch("Ptmmmm", ptmmmm, "Ptmmmm/F")
    newT.Branch("Etammmm", etammmm, "Etammmm/F")
    newT.Branch("Phimmmm", phimmmm, "Phimmmm/F")
    newT.Branch("Ptmmee", ptmmee, "Ptmmee/F")
    #eta coordinate of the mmee
    newT.Branch("Etammee", etammee, "Etammee/F")
    newT.Branch("Phimmee", phimmee, "Phimmee/F")
    newT.Branch("event", event, "event/l")
    newT.Branch("run", run, "run/l")
    newT.Branch("Nmmmm", Nmmmm, "Nmmmm/l")
    newT.Branch("Nmmee", Nmmee, "Nmmee/l")
    newT.Branch("triggerWord", triggerWord, "triggerWord[%d]/l"%(nwords))
    newT.Branch("Nmmg", Nmmg, "Nmmg/l")
    newT.Branch("NAllmmg", NAllmmg, "NAllmmg/l")
    newT.Branch("Mmmg", mmmg, "Mmmg[%d]/F"%(nMax))
    newT.Branch("Ptmmg", ptmmg, "Ptmmg[%d]/F"%(nMax))
    newT.Branch("PhodR", PhodR, "PhodR[%d]/F"%(nMax))

    newT.Branch("Ptmm", ptmm, "Ptmm/F")
    newT.Branch("Mmm", mmm, "Mmm/F")
    newT.Branch("Ptee", ptee, "Ptee/F")
    newT.Branch("Mee", mee, "Mee/F")

    newT.Branch("Ptm", ptm, "Ptm[2]/F")
    newT.Branch("Pte", pte, "Pte[2]/F")
    #3d impact parameter for the muons
    newT.Branch("IP3dm", ip3dm, "IP3dm[2]/F")
    newT.Branch("Dxym", dxym, "Dxym[2]/F")
    newT.Branch("Dzm", dzm, "Dzm[2]/F")
    #3d impact parameter for the electrons
    newT.Branch("IP3de", ip3de, "IP3de[2]/F")
    newT.Branch("Dxye", dxye, "Dxye[2]/F")
    newT.Branch("Dze", dze, "Dze[2]/F")

    newT.Branch("dRmm", drmm, "dRmm/F")
    newT.Branch("dIPmm", dipmm, "dIPmm/F") 
    newT.Branch("tightmm", tightmm, "tightmm/l") 

    newT.Branch("Qmmmm", Qmmmm, "Qmmmm/F")
    newT.Branch("Qmmg", Qmmg, "Qmmg[%d]/F"%(nMax))
    newT.Branch("Qmmee", Qmmmm, "Qmmee/F")
    if isMC:
        newT.Branch("Weight", mcweight, "Weight/F")
        #os.environ['ANALYSIS_BASE_DIR'] = "/uscms_data/d3/bgreenbe/CMSSW_10_2_9/src/tm_analysis/analysis"
        #try:
        #if 2+2 == 5:
        #    import utils.configuration as configuration
        ##except ImportError:
        #else:
        #    print("Error: you must source env.sh before running in MC mode:")
        #    print("     /uscms_data/d3/bgreenbe/CMSSW_10_2_9/src/tm_analysis/analysis/env.sh")
        #    sys.exit()
        #cfg = configuration.Configuration()
        #f_xsec = ROOT.TFile.Open(cfg.fns['xsecs'])
        if not condor:
            f_xsec = ROOT.TFile.Open("../../tm_analysis/analysis/data_out/xsecs.root")
        else:
            f_xsec = ROOT.TFile.Open("xsecs.root")

        #just treating all years together
        lumi = 146.91 #integrated luminosity for all Run2
       # if yr == 2018:
       #     lumi = 63.7 #integrated luminosity for 2018
       # elif yr == 2017:
       #     lumi = 45.0
       # elif yr == 2016:
       #     lumi = 38.3
       # else:
       #     print("year %d not recognized. Error!"%yr)
       #     sys.exit()
        if not condor:
            sys.path.insert(1, "../../tm_analysis/analysis/python/utils")
        #using a fake branching ratio to stay blind until the very end of the analysis!
        #import utils.blinding as blinding
        if blinded:
            import blinding
            bratio = blinding.get_blinded_BR_EtaTo2Mu2E()
            print("blinded ratio obtained!")
        else:
            #only bkg for now is eta->mu mu gamma, with BR 3.1e-4  !!
            bratio = 3.1e-4
        #this is the histogram that will let us find the proper (approximate) cross section for each event
        h_xsec = f_xsec.Get("corr_xsec")
        
        
    print("newT: " + str(newT))
    #newT.Print()
    print("done printing newT.")
    #debug = True
    fl = filename
    #full_path = path + fl + "_" + str(yr) + ".root"
    full_path = path + fl
    print("trying to open %s"%(full_path))
    inF = ROOT.TFile(full_path)
    print("opened tfile %s"%(full_path))
    t = inF.Get("Events")
    if isMC:
        hwpt = inF.Get("hWeightsPt")
    print("got Events tree.")
    nevents = t.GetEntries()
    ncut = 0
    if nevents == 0:
        print("Error: 0 events found in file %s."%(full_path)) 
        raise ZeroDivisionError
    import generalFunctions as GF
    print("got generalFunctions.")
    cutCounter = GF.cutCounter()

    #get sum of weights for MC
    if isMC:
        hw = inF.Get("hWeights")
        sow = hw.GetSumOfWeights()
        if sow == 0:
            print("Error: MC mode but no hWeights!!!!!!!!!!")
            sys.exit()

    #events to debug
    #dbg_run = 297099
    #dbg_evts = [54984622L, 55514217L, 54419339L, 55831401L, 55836957L, 54527950L, 54817192L, 54298018L, 56092566L, 54583843L]
    #dbg_evts = [54984622L, 55514217L, 54419339L, 55831401L, 55836957L, 54527950L, 54817192L, 54298018L, 56092566L, 54583843L, 55361918L, 54498349L, 
    #            55796979L, 56893379L, 56990258L, 56376426L, 57710998L, 57590198L, 56869021L, 56564361L, 57403428L, 57079882L, 57355872L, 57620090L, 
    #            57541930L, 56713363L, 59405211L, 59532350L, 58484774L, 58507639L, 59553318L, 59574224L, 58276071L, 59643412L, 59854231L, 59478902L, 
    #            60908073L, 61240814L, 61257888L, 61058477L, 61721762L, 61638481L, 61734408L, 61587844L, 61974561L, 61863161L, 61451338L, 61136760L, 
    #            62786808L, 62396189L, 63540103L, 63057025L, 63309137L, 62162238L, 63732599L, 65544515L, 64961168L, 64819352L, 64053239L, 64731567L, 
    #            65243447L, 64119803L, 65296866L, 64502455L, 66140606L, 67537510L, 65994010L, 66970698L, 66014196L, 67556381L, 66908274L, 66099874L, 
    #            67935703L, 66117318L, 69079636L, 69566658L, 69123947L, 68258008L, 68866490L, 68770433L, 69705062L, 70365136L, 71792593L, 70520061L, 
    #            70758832L, 71696172L, 71630913L, 71749534L, 69958400L, 70409287L, 70473471L, 72732323L, 72670672L, 72896965L, 72188323L, 72169673L, 
    #            71929979L, 72283425L, 73720728L, 74573049L, 74730050L, 75306675L, 75393220L, 75325823L, 75341692L, 74292980L, 74885652L, 74084233L, 
    #            75241830L, 75058041L, 75021489L, 76301488L, 77516007L, 77232962L, 76808559L, 76197729L, 76383379L, 75884851L, 76792690L, 76385183L, 
    #            76830538L, 77551126L, 78108644L, 77685585L, 78179629L, 13731255L, 13522531L, 14795757L, 13690254L, 13486418L, 15189026L, 13430256L, 
    #            16752964L, 15552420L, 16707507L, 16262607L, 16951160L, 16915378L, 15497235L, 15331227L, 17907470L, 18066667L, 18207783L, 17854780L, 
    #            17622070L, 17311021L, 17555151L, 17652872L, 17836486L, 18743396L, 18755956L, 18796821L, 19016629L, 20204958L, 20233193L, 20478366L, 
    #            19683746L, 21927771L, 21645600L, 22140359L, 20603006L, 23011613L, 22500863L, 22855427L, 22512251L, 22476327L, 22441217L, 24394104L, 
    #            24416428L, 25321999L, 24836560L, 25095298L, 24949121L, 27049853L, 26991279L, 26732218L, 26896631L, 26243024L, 26303674L, 26278116L, 
    #            25508171L, 26802477L, 26777135L, 26153223L, 27515831L, 28369768L, 27401177L, 28504662L, 28681620L, 28639424L, 41196723L, 40976140L, 
    #            41822338L, 41087497L, 42098488L, 41463382L, 41509424L, 41367520L, 41192486L, 42158166L, 41175590L, 42380410L, 41802532L, 42531734L, 
    #            42582850L, 42483501L, 42246824L, 42457261L, 40939731L, 44585642L, 44125341L, 42854354L, 43014867L, 44281049L, 42877206L, 43937647L, 
    #            44654847L, 42941038L, 43115448L, 43675088L, 43729698L, 43245677L, 45449217L, 44720938L, 44947034L, 45284305L, 45964126L, 44986553L, 
    #            45274536L, 47765575L, 47796275L, 47073153L, 47199487L, 47539280L, 47365922L, 48422911L, 46795061L, 48408112L, 47050062L, 47977690L, 
    #            47135904L, 48482418L, 49855497L, 50030356L, 49519510L, 49116253L, 48992108L, 49852510L, 48818128L, 51240386L, 51445926L, 51124203L, 
    #            52222472L, 51950028L, 51353376L, 52212880L, 51781778L, 50571394L, 51980163L, 51228217L, 52311861L, 50435112L, 50764734L, 51995916L, 
    #            51879078L, 53509541L, 53525850L, 52500789L, 53534283L, 54077409L, 23606466L, 29174372L, 30855785L, 29333847L, 29269770L, 29276234L, 
    #            30009285L, 29343013L, 30164586L, 29582938L, 30563254L, 30252544L, 31061047L, 32569102L, 31692320L, 32634475L, 32616560L, 31415459L, 
    #            33075498L, 33815613L, 33627670L, 33339077L, 33255815L, 33900486L, 33239540L, 34130144L, 33108336L, 34086305L, 34434126L, 36177561L, 
    #            36682435L, 35700371L, 35105210L, 35482472L, 36130579L, 34812985L, 34839823L, 35321613L, 36670356L, 35323275L, 35527978L, 34941833L, 
    #            35754536L, 36417731L, 35651164L, 37962360L, 37135314L, 36856882L, 38189849L, 38643425L, 38356836L, 38451455L, 37878932L, 37535221L, 
    #            37567595L, 40133953L, 39216080L, 40393943L, 40489165L, 39770027L, 40582392L]
    #keep trying until it works (at most 10 times)
    #succeeded?
    succ = False
    for trynum in range(10):
        try:
            #if trynum > 0:
            #    #if restarting need to reset the arrays!!
            #    mmmmm = array('f', [0])
            #    #invariant mass of the mmee system
            #    mmmee = array('f', [0])
            #    #pt2l = array('f', [0]*nMax)
            #    #pt2e = array('f', [0]*nMax)
            #    #pt4l = array('f', [0]*nMax)
            #    ptmmmm = array('f', [0])
            #    ptmmee = array('f', [0])
            #    event = array('l', [0])
            #    run = array('l', [0])
            #    Nmmmm = array('l', [0])
            #    Nmmee = array('l', [0])
            ncut = 0
            print("about to start loop.")
            #debugging
            count429 = 0
            for i,e in enumerate(t):
                #break if past the events we are supposed to analyze
                if nevent > -1 and i > nevent: break
                #print once in a while to make sure program is still running
                #if i % 10000 == 0:
                if i % 100 == 0:
                    print("Now processing event %d out of %d for %s_%d"%(i, nevents, fl, yr))
                #add extra debug print statements or nah
                dbg = False #True #False
                #if e.run == 316239 and e.evt == 296470691:
                #    dbg = True
                #if e.run == dbg_run and e.evt in dbg_evts:
                #    dbg = True
                #    print("***Run=%d, event=%d***"%(dbg_run, e.evt))
                #    #print event arguments: entry, isMC, isntuple
                #    GF.printEvent(e, False, True)
                cutCounter.count('All')
                #first make the stricter selections
                #make sure at least one of the dimu triggers was passed
                passed_trig = False
                #for j in range(nwords):
                #    if e.dimuTriggerWord[j] > 0:
                #        passed_trig = True
                #        break
                if isMC:
                    #get info on the Gen Eta meson; obtain its pT
                    genEta = ROOT.TLorentzVector()
                    lep = [None for j in range(e.nGoodGenPart)] 
                    #gen-level eta meson found?
                    genEtaFound = False
                    for j in range(e.nGoodGenPart):
                        lep[j] = ROOT.TLorentzVector()
                        #photon
                        if e.GenPart_pdgId[j] == 22:
                            mass = 0
                        #muon/antimuon
                        elif abs(e.GenPart_pdgId[j]) == 13:
                            mass = .105
                        #electron/positron
                        elif abs(e.GenPart_pdgId[j]) == 11:
                            mass = .000511
                        #eta meson
                        elif e.GenPart_pdgId[j] == 221:
                            genetapt[0] = e.GenPart_pt[j]
                            genEtaFound = True
                            break
                        else:
                            print("Error!!! Unrecognized pdgId: %d"%e.GenPart_pdgId[j]) 
                            sys.exit()
                        lep[j].SetPtEtaPhiM( e.GenPart_pt[j], e.GenPart_eta[j], e.GenPart_phi[j], mass )
                        
                    if not genEtaFound:
                        if e.nGoodGenPart == 3:
                            genEta = lep[0] + lep[1] + lep[2]
                        elif e.nGoodGenPart == 4:
                            genEta = lep[0] + lep[1] + lep[2] + lep[3]
                        else:
                            print("Error: unrecognized nGoodGenPart: %d"%e.nGoodGenPart)
                            sys.exit()
                        genetapt[0] = genEta.Pt()
                else:
                    genetapt[0] = -99

                if e.doubleMuTrig > 0: passed_trig = True
                if passed_trig:
                    hpassedTrig.Fill(genetapt[0]) 

                #don't continue if failed trigger yet, because still want to fill the reco eff histogram.
                #if not passed_trig:
                #    ncut += 1
                #    if dbg:
                #        print("failed trigger.")
                #    continue
                #cutCounter.count('Passed trigger')

                # (getGoodLists will return array of 4 lists, one for each particle (2 identical mu lists, 2 identical e lists))
                goodlists = muFun.getGoodLists('mmee', e)
                goodMuonList = goodlists[0]
                
                goodElectronList = goodlists[2]
                if len(goodMuonList) < 2:
                    ncut += 1
                    if dbg:
                        print("failed 2 good muons.")
                    continue
                cutCounter.count('2 good muons')
                #now get the best mu pairs
                #all_pairs = muFun.getAllPairs('mm', e, goodMuonList, goodMuonList)
                #now get all the possible pairs of mu pairs
                #allpair2s = muFun.getAllPair2s('mmmm', e, all_pairs, all_pairs)
                #now get best amongst them
                #pairList, bestPair = muFun.getBestPair('mm', e, goodMuonList, goodMuonList)
                #actually just get all of them for now.
                pairList = muFun.getAllPairs('mm', e, goodMuonList, goodMuonList)
                epairList = muFun.getAllPairs('ee', e, goodElectronList, goodElectronList)
                if dbg:
                    print("pairList: {}".format(str(pairList)))
                    print("epairList: {}".format(str(epairList)))
                #sometimes all leptons are too close to each other or something
                if len(pairList) < 1:
                    ncut += 1
                    if dbg:
                        print("failed good muon pair.")
                    continue
                cutCounter.count('1 good muon pair')
                
                goodone = False
                M2mugs = [-99 for j in range(nMax)]
                #now look at the photons!
                #first find the best muon pair, then get every combo of photons with it
                #find the best muon pair (min diff in ip3d)
                mindiff = 9999999
                minidx = -1
                for j,pair in enumerate(pairList):
                    diff = abs( e.Muon_ip3d[pair[0]] - e.Muon_ip3d[pair[1]] )
                    if diff < mindiff:
                        mindiff = diff
                        minidx = j
                bestpair = pairList[minidx]
                lep0Vec = ROOT.TLorentzVector()
                lep1Vec = ROOT.TLorentzVector()
                #lep0Vec.SetPtEtaPhiM(e.Muon_pt[pairList[k][0]], e.Muon_eta[pairList[k][0]], e.Muon_phi[pairList[k][0]], .105) 
                #lep1Vec.SetPtEtaPhiM(e.Muon_pt[pairList[k][1]], e.Muon_eta[pairList[k][1]], e.Muon_phi[pairList[k][1]], .105) 
                lep0Vec.SetPtEtaPhiM(e.Muon_pt[bestpair[0]], e.Muon_eta[bestpair[0]], e.Muon_phi[bestpair[0]], .105) 
                lep1Vec.SetPtEtaPhiM(e.Muon_pt[bestpair[1]], e.Muon_eta[bestpair[1]], e.Muon_phi[bestpair[1]], .105) 
                mmm[0] = (lep0Vec + lep1Vec).M()
                ptmm[0] = (lep0Vec + lep1Vec).Pt()
                ptm[0] = e.Muon_pt[bestpair[0]] 
                ptm[1] = e.Muon_pt[bestpair[1]] 
                ip3dm[0] = e.Muon_ip3d[bestpair[0]]
                ip3dm[1] = e.Muon_ip3d[bestpair[1]]
                #dxy, dz of each muon
                dxym[0] = e.Muon_dxy[bestpair[0]]
                dxym[1] = e.Muon_dxy[bestpair[1]]
                dzm[0] = e.Muon_dz[bestpair[0]]
                dzm[1] = e.Muon_dz[bestpair[1]]

                drmm[0] = muFun.pair_dR( e.Muon_eta[bestpair[0]], e.Muon_phi[bestpair[0]], e.Muon_eta[bestpair[1]], e.Muon_phi[bestpair[1]] )
                dipmm[0] = mindiff
                tightstr = ""
                for j in range(2): 
                    if e.Muon_tightId[bestpair[j]] : 
                        tightstr += "1" 
                    else: 
                        tightstr += "0"
                tightmm[0] = int(tightstr, 2)
                #pairList, bestPair = muFun.getBestPair('mm', e, goodMuonList, goodMuonList)
                ngoodtrio = 0 #good photon groupings
                ngoodphoton = e.nGoodPhoton
                for j in range(e.nPhoton):
                    #if not e.Photon_tightId[j] > 0:
                    #    ngoodphoton -= 1
                    #    continue
                    if ngoodtrio > nMax:
                        ngoodphoton = ngoodtrio
                        break
                    #for k in range(len(pairList)):
                    for k in range(1):
                        phoVec = ROOT.TLorentzVector()
                        phoVec.SetPtEtaPhiM(e.Photon_pt[j], e.Photon_eta[j], e.Photon_phi[j], 0) 
                        trioVec = lep0Vec + lep1Vec + phoVec
                        if trioVec.M() > maxM:
                            continue
                        M2mugs[ngoodtrio] = trioVec.M()
                        if ngoodtrio >= nMax:
                            print("Error: nMax is only %d but we have more good trios than that! :/"%(nMax))                
                            ngoodtrio += 1
                            break
                        mmmg[ngoodtrio] = M2mugs[ngoodtrio]
                        ptmmg[ngoodtrio] = trioVec.Pt()
                        PhodR[ngoodtrio] = muFun.pair_dR( e.Muon_eta[bestpair[0]], e.Muon_phi[bestpair[0]], e.Photon_eta[j], e.Photon_phi[j] ) + \
                                            muFun.pair_dR( e.Muon_eta[bestpair[1]], e.Muon_phi[bestpair[1]], e.Photon_eta[j], e.Photon_phi[j] ) 
                        Qmmg[ngoodtrio] = e.Muon_charge[bestpair[0]] + e.Muon_charge[bestpair[1]] 
                        goodone = True
                        ngoodtrio += 1
                    

               # if len(pairList) > nMax: 
               #     #print("Error: pairList length is %d but nMax is only %d."%(len(pairList), nMax))
               #     #print("pairList: " + str(pairList))
               #     #sys.exit()
               #     #break
               #     pass
               # #get the nMax pairs with lowest invariant mass.
               # invmasses = [0. for j in range(len(pairList))]
               # pTs = [0. for j in range(len(pairList))]
               # #first get all the invmasses, pTs
               # for j in range(len(pairList)):
               #     #get the 4-vectors
               #     leps = [] #lorentz vectors
               #     for k in range(2):
               #         leps.append( muFun.get4vec('m', e, pairList[j][k]) )
               #     #get the invariant mass of the pair 
               #     v2l = (leps[0] + leps[1])
               #     M = v2l.M()
               #     pt = v2l.Pt()
               #     invmasses[j] = M
               #     pTs[j] = pt
               # #now get the nMax with lowest invmass.
               # for j in range(nMax):
               #     if len(invmasses) > 0:
               #         mmin = min(invmasses)
               #         m2l[j] = mmin
               #         #k is the index of the min invariant mass.
               #         k = invmasses.index(mmin)
               #         pt2l[j] = pTs[k]
               #         #remove these values from the lists so they won't be found again next iteration.
               #         del invmasses[k]
               #         del pTs[k]
               #     else:
               #         m2l[j] = -99
               #         pt2l[j] = -99
                
                #true if at least one cat had a good quadruplet
                M4m = -99
                M2m2e = -99
                for cat in ['mmmm', 'mmee']:
                #for cat in ['mmee']:
                    #some events will have 2 good muon pairs, some won't.
                    pairlist2 = pairList
                    if 'e' in cat: pairlist2 = epairList
                    #last False is to not allow repeats.
                    allpair2s = muFun.getAllPair2s(cat, e, pairList, pairlist2, False)
                    #now purge any pair2s that are identical to a previous one.
                    sums = []
                    prods = []
                    realpair2s = []
                    for j in range(len(allpair2s)):
                        numsum = allpair2s[j][0][0] + allpair2s[j][0][1] + allpair2s[j][1][0] + allpair2s[j][1][1]
                        numprod= allpair2s[j][0][0] * allpair2s[j][0][1] * allpair2s[j][1][0] * allpair2s[j][1][1]
                        if cat[:2] == cat[2:] and numsum in sums:
                            k = sums.index(numsum)
                            if prods[k] == numprod:
                                #then it's all the same numbers
                                continue
                            #otherwise it's unique.
                        sums.append(numsum)
                        prods.append(numprod)
                        realpair2s.append(allpair2s[j])
                    allpair2s = realpair2s
                    if dbg:
                        print("nentries in newT before: " + str(newT.GetEntries()))
                        print("allpair2s: {}".format(allpair2s))
                    #for j in range(nMax*nMax):
                    #    exec("pt%s[j] = -99"%(cat))
                    #    exec("m%s[j] = -99"%(cat))
                    if len(allpair2s) < 1 or len(allpair2s[0]) < 1:
                        if dbg:
                            print("failed 2 good lepton pairs.")
                        continue
                    #else
                    #we want to keep ALL pair2s, not just the 'best' one.
                    #print("allpair2s: " + str(allpair2s))
                    #if len(allpair2s) > nMax*nMax:
                    #    #nMax^2 items are allowed for the 4-lepton variables
                    #    print("Error! %d pair2s but nMax is only %d for cat %s."%(len(allpair2s), nMax, cat))
                    #    sys.exit()
                    #find the nMax^2 lowest invmasses, save only those.
                    #print("all pair2s: " + str(allpair2s))
                    #invmasses = [0. for j in allpair2s]
                    #pTs = [0. for j in allpair2s]
                    #jj will only increase when there's a quad in the range of interest (minM < M < maxM)
                    jj = 0
                    #for j in range(len(allpair2s)):
                    #if len(allpair2s) == 0 or len(allpair2s[0]) == 0: continue
                    #just get 4vector from this pair2. (will sort them all later).
                    fveclist, lepList, bestPair = muFun.getBestPairs_ip3d(cat, e, allpair2s)
                    eta4vec = fveclist[0] + fveclist[1] + fveclist[2] + fveclist[3]
                    M = eta4vec.M()
                    if cat == 'mmee' and M > .51 and M < .63:
                        hpassedReco.Fill(genetapt[0]) 
                    if dbg:
                        print("fveclist, lepList, bestPair, eta4vec:")
                        print(fveclist)
                        print(lepList)
                        print(bestPair)
                        print(eta4vec)
                    if M < minM or M >= maxM:
                        #make sure Mmmee has a good value, not a repeat
                        if goodone and cat == "mmee":
                            mmmee[0] = -99
                        continue
                    #debug!!
                    if M > 0.40 and M < 0.45: #== 0.4290032:
                        print("M = %f my dude!!!"%(M))
                        print("Mmmee before: %s"%(str(mmmee)))
                        print("input to getBestPairs: " + str(allpair2s)) 
                        eta4vec.Print()
                        GF.printEvent(e,False,True)
                        count429 += 1
                        if count429 == 11: sys.exit()
                        #sys.exit()
                    pt = eta4vec.Pt()
                    if dbg:
                        print("pt: " + str(pt))
                    #invmasses[0] = M
                    #pTs = pt
                    jj += 1
                    if dbg: print("jj: " + str(jj))
                    #if not multiquad: break
                    #for j in range(nquad):
                    #    if len(invmasses) > 0:
                    #        #print("all invmasses: " + str(invmasses))
                    #        mmin = min(invmasses)
                    #        #print("lowest mass: " + str(mmin))
                    #        k = invmasses.index(mmin)
                    if cat == "mmmm":
                        Nmmmm[0] = len(allpair2s)
                        ptmmmm[0] = pt
                        etammmm[0] = eta4vec.Eta()
                        phimmmm[0] = eta4vec.Phi()
                        mmmmm[0] = M
                        M4m = M
                        Qmmmm[0] = e.Muon_charge[lepList[0]] + e.Muon_charge[lepList[1]] + e.Muon_charge[bestPair[0]] + e.Muon_charge[bestPair[1]]
                    elif cat == "mmee":
                        Nmmee[0] = len(allpair2s)
                        ptmmee[0] = pt
                        etammee[0] = eta4vec.Eta()
                        phimmee[0] = eta4vec.Phi()
                        mmmee[0] = M
                        M2m2e = M
                        Qmmee[0] = e.Muon_charge[lepList[0]] + e.Muon_charge[lepList[1]] + e.Electron_charge[bestPair[0]] + e.Electron_charge[bestPair[1]]
                        #fill in ptee, pte now.
                        eevec = fveclist[2] + fveclist[3]
                        ptee[0] = eevec.Pt()
                        mee[0] = eevec.M()
                        pte[0] = e.Electron_pt[bestPair[0]]
                        pte[1] = e.Electron_pt[bestPair[1]]
                        ip3de[0] = e.Electron_ip3d[bestPair[0]] 
                        ip3de[1] = e.Electron_ip3d[bestPair[1]] 
                        dxye[0] = e.Electron_dxy[bestPair[0]] 
                        dxye[1] = e.Electron_dxy[bestPair[1]] 
                        dze[0] = e.Electron_dz[bestPair[0]] 
                        dze[1] = e.Electron_dz[bestPair[1]] 
                   
                    #if M > 0.40 and M < 0.45: #== 0.4290032:
                    #    print("M = %f my bro!!!"%(M))
                    #    print("Mmmee after: %s"%(str(mmmee)))
                    #exec("N%s[0] = len(allpair2s)"%(cat))
                    #exec("pt%s[0] = pt"%(cat))
                    #exec("m%s[0] = M"%(cat))
                    goodone = True
                    #        del invmasses[k]
                    #        del pTs[k]
                    #        #print("new invmasses: " + str(invmasses))
                    #    else:
                    #        break
                        #exec("pt%s[0] = -99"%(cat))
                        #exec("m%s[0] = -99"%(cat))
                    #        ####already set everything to -99 above.
                    #        ##break
                if not goodone:
                    ncut += 1
                    if dbg:
                        print("cut on 2 good lepton pairs.")
                    continue
                cutCounter.count('2 good lepton pairs')
                #make sure Mmmmm has the right value, not a repeat.
                if M4m == -99:
                    mmmmm[0] = -99
                    ptmmmm[0] = -99
                    etammmm[0] = -99
                    phimmmm[0] = -99
                if M2m2e == -99:
                    mmmee[0] = -99
                    ptmmee[0] = -99
                    etammee[0] = -99
                    phimmee[0] = -99
                    mee[0] = -99
                    ptee[0] = -99
                    pte[0] = -99
                    pte[1] = -99
                    ip3de[0] = -99
                    ip3de[1] = -99
                    dxye[0] = -99
                    dxye[1] = -99
                    dze[0] = -99
                    dze[1] = -99
                for j in range(ngoodtrio, nMax):
                    mmmg[j] = -99
                    ptmmg[j] = -99
                    PhodR[j] = -99
                Nmmg[0] = ngoodtrio
                NAllmmg[0] = len(pairList) * ngoodphoton
               # allmmeepairs = muFun.getAllPair2s('mmee', e, pairList, epairList)
               # if len(allmmeepairs) < 1 or len(allmmeepairs[0]) < 1:
               #     ptmmee[0] = -99
               #     mmmee[0] = -99
               #     pt2e[0] = -99
               #     m2e[0] = -99
               # else:
               #     if debug:
               #         print("all pair2s: {}".format(str(allmmeepairs)))
               #     fveclist, lepList, bestPair = muFun.getBestPairs('mmee', e, allmmeepairs)
               #     eta4vec = fveclist[0] + fveclist[1] + fveclist[2] + fveclist[3]
               #     ptmmee[0] = eta4vec.Pt()
               #     mmmee[0] = eta4vec.M()
               #     ee4vec = fveclist[2] + fveclist[3]
               #     #if debug:
               #     #    print("ee4vec:")
               #     #    print(ee4vec)
               #     #    print("lepList: {}, bestPair: {}".format(lepList, bestPair))
               #     #    print("pt: {}, M: {}, eta: {}, phi: {}".format(ee4vec.Pt(), ee4vec.M(), ee4vec.Eta(), ee4vec.Phi()))
               #     #    print("e0: pt: {}, M: {}, eta: {}, phi: {}".format(fveclist[2].Pt(), fveclist[2].M(), fveclist[2].Eta(), fveclist[2].Phi()))
               #     #    print("e1: pt: {}, M: {}, eta: {}, phi: {}".format(fveclist[3].Pt(), fveclist[3].M(), fveclist[3].Eta(), fveclist[3].Phi()))
               #     #    GF.printEvent(e,False,True)
               #     pt2e[0] = ee4vec.Pt()
               #     m2e[0] = ee4vec.M()

                #Now that reco is done, continue if it failed the trigger.
                if not passed_trig:
                    ncut += 1
                    if dbg:
                        print("failed trigger.")
                    continue
                cutCounter.count('Passed trigger')
                if isMC:
                    #set the weight for the mmee event (xsec depends on acceptance(pt)).
                    xsec = h_xsec.GetBinContent( h_xsec.FindBin( ptmmee[0] ) )
                    mcweight[0] = xsec * bratio * lumi / sow
                event[0] = e.evt
                run[0] = e.run
                #write output root file.
                #print("newT: " + str(newT))
                #newT.Print()
                try:
                    newT.Fill()
                except AttributeError:
                    print("Error: newT AttributeError")
                    print("AttributeError occurs in event %d out of %d for %s_%d, try #%d"%(i, nevents, fl, yr, trynum)) 
                    print("nentries in newT: " + str(newT.GetEntries()))
                    print("newT: " + str(newT))
                    raise AttributeError
        except RuntimeError:
            print("I/O error for %s_%d. Retrying (try #%d)."%(fl, yr, trynum))
            inF.Close()
            outF.Close()
            #wait 2 minutes before trying again
            time.sleep(120)
            inF = ROOT.TFile(full_path)
            t = inF.Get("Events")
            outF = ROOT.TFile( fileName, 'recreate' ) 
            newT = ROOT.TTree( 'Events', 'Output tree' )
            newT.Branch("Mmmmm", mmmmm, "Mmmmm/F")
            newT.Branch("Mmmee", mmmee, "Mmmee/F")
           # newT.Branch("Pt2l", pt2l, "Pt2l[%d]/F"%(nquad))
           # newT.Branch("Pt2e", pt2e, "Pt2e[%d]/F"%(nquad))
            newT.Branch("Ptmmmm", ptmmmm, "Ptmmmm/F")
            newT.Branch("Etammmm", etammmm, "Etammmm/F")
            newT.Branch("Phimmmm", phimmmm, "Phimmmm/F")
            newT.Branch("Ptmmee", ptmmee, "Ptmmee/F")
            newT.Branch("Etammee", etammee, "Etammee/F")
            newT.Branch("Phimmee", phimmee, "Phimmee/F")
            newT.Branch("event", event, "event/l")
            newT.Branch("run", run, "run/l")
            newT.Branch("Nmmmm", Nmmmm, "Nmmmm/l")
            newT.Branch("Nmmee", Nmmee, "Nmmee/l")
            newT.Branch("triggerWord", triggerWord, "triggerWord[%d]/l"%(nwords))
            newT.Branch("Nmmg", Nmmg, "Nmmg/l")
            newT.Branch("NAllmmg", NAllmmg, "NAllmmg/l")
            newT.Branch("Mmmg", mmmg, "Mmmg[%d]/F"%(nMax))
            newT.Branch("Ptmmg", ptmmg, "Ptmmg[%d]/F"%(nMax))
            newT.Branch("PhodR", PhodR, "PhodR[%d]/F"%(nMax))
            newT.Branch("Mmm", mmm, "Mmm/F")
            newT.Branch("Ptmm", ptmm, "Ptmm/F")
            newT.Branch("Ptee", ptee, "Ptee/F")
            newT.Branch("Mee", mee, "Mee/F")

            newT.Branch("Ptm", ptm, "Ptm[2]/F")
            newT.Branch("Pte", pte, "Pte[2]/F")
            newT.Branch("IP3dm", ip3dm, "IP3dm[2]/F")
            newT.Branch("Dxym", dxym, "Dxym[2]/F")
            newT.Branch("Dzm", dzm, "Dzm[2]/F")
            newT.Branch("IP3de", ip3de, "IP3de[2]/F")
            newT.Branch("Dxye", dxye, "Dxye[2]/F")
            newT.Branch("Dze", dze, "Dze[2]/F")

            newT.Branch("dRmm", drmm, "dRmm/F")
            newT.Branch("dIPmm", dipmm, "dIPmm/F")
            newT.Branch("tightmm", tightmm, "tightmm/l")
            newT.Branch("Qmmg", Qmmg, "Qmmg[%d]/F"%(nMax))
            newT.Branch("Qmmmm", Qmmmm, "Qmmmm/F")
            newT.Branch("Qmmee", Qmmee, "Qmmee/F")
            if isMC:
                newT.Branch("Weight", mcweight, "Weight/F")
            continue

        print("%s_%d succeeded on try number %d"%(fl, yr, trynum))
        succ = True
        break

    if not succ:
        print("Error: I/O error for %s_%d!"%(fl, yr))
        raise RuntimeError
    if isMC:
        hwpt2 = hwpt.Clone("hWeightPt")
        hwpt2.Print()
        hwpt2.SetDirectory(outF)
    inF.Close()
    #hwpt2.Print()
    status = outF.Write()
    outF.Close()
    cutCounter.printSummary()
    print("Cut %d events out of %d total ( %f %% ) for %s_%d."%(ncut, min(nevent, nevents), (100.0*ncut/min(nevent, nevents)), fl, yr))
    if condor:
        os.system("xrdcp -f %s root://cmseos.fnal.gov//store/user/bgreenbe/eta_skimmed/"%(fileName)) 
        os.system("rm -f {}".format(full_path))

#helper function used only for multiprocessing
def makeskimstar(ploads):
    #print("arguments for makeskim: " + str(*ploads))
    return makeskim(*ploads)    

def main():
    #parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--nevents",default=-1,type=int,help="Number of events to process in each file (-1 default to do all events)")
    parser.add_argument("-db","--debug",default=False,action='store_true',help="run in debug mode (no multiprocessing) or nah")
    parser.add_argument("-mc","--MC",default=False,action='store_true',help="run on MC instead of data.")
    parser.add_argument("-nn","--nickname",default="",type=str,help="nickname for output file (to distinguish it).")
    parser.add_argument("-y","--year",default=2016,type=int,help="year (2016, 2017, or 2018).")                     
    parser.add_argument("-c","--incsv",default="",type=str,help="name of input csv file with all the file names in it.")                     
    parser.add_argument("-t","--testname",default="",type=str,help="name appended to all for the ntuple files that we're going to read. eg noee for all_noee")
    parser.add_argument("-con","--condor",default=False,action='store_true',help="running on condor or nah")
    parser.add_argument("-b","--blind",default=False,action='store_true',help="blind the BR (for signal sample!) or nah?")
    args = parser.parse_args()

    blinded = False
    if args.blind: 
        print("blind!!")
        blinded = True
    else:
        print("not blind!") 
    #get the list of processes from the csv.
    incsv = args.incsv
    filelist = []
    if incsv != "":
        incsf = open(incsv, "r")
        for lin in incsf:
            samp = lin.split(',')[0]
            filelist.append(samp)
    else:
        print("Error: you must specify the csv file with -c/--incsv!!!!!!!!!")
        sys.exit()

    nevent = args.nevents
    year = args.year
    #path to ntuple files
    path = "/eos/uscms/store/user/bgreenbe/eta_{}/all{}/".format(year, "_"+args.testname if args.testname != "" else "")
    #if args.MC: path = "/eos/uscms/store/user/bgreenbe/EtaTo2Mu2E/NANOAODSIM/"

    print("filelist: " + str(filelist))
    #if debug mode requested do not try to multi-thread.
    if args.debug:
            for fn in filelist:
                num = 0
                fullfile = fn + "_" + str(year) + "_" + str(num) + ".root"
                print("file path: " + path + fullfile)
                while os.path.exists(path + fullfile):
            ##########debugging!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1#########################################
                #    if num == 1:
                    makeskim(fullfile, year, path, nevent, args.nickname, args.debug, False, args.MC, blinded)    
            ###################################################################################################
                    num += 1
                    fullfile = fn + "_" + str(year) + "_" + str(num) + ".root"
                if num == 0:
                    print("Error: path to file(s) not found.")
    elif args.condor:
        payloads = []
        ncores = 8
        for fn in filelist:
            num = 0
            done = False
            fullpath = ""
            while not done:
                try:
                    fullfile = "{}_{}_{}.root".format(fn, year, num)
                    #fullpath = "root://cmseos.fnal.gov/" + path
                    fullpath = "root://cmseos.fnal.gov//store/user/bgreenbe/eta_{}/all/{}".format(year, fullfile) 
                   # os.system("xrdfs cmseos.fnal.gov locate %s"%(fullpath))
                    newfilename = "{}_{}_{}_ntuple.root".format(fn, year, num)
                    os.system("xrdcp %s ./%s"%(fullpath, newfilename)) 
                    g = ROOT.TFile(newfilename)
                    #g.Print()
                    evs = g.Get("Events")
                    evs.Print()
                    payloads.append((newfilename, year, "./", nevent, args.nickname, False, True, args.MC, blinded))
                    num += 1
                except ( ReferenceError, OSError ):
                    print("%s_%d not found!"%(fn, num))
                    done = True
            if num == 0:
                print("ERROR: Error no files found.")
                print("{} not found!".format(fullpath))
                sys.exit()
        import multiprocessing as mp
        pool  = mp.Pool(ncores)
        pool.map(makeskimstar, payloads)
        pool.close()
        pool.join()
       # for pl in payloads:
       #     os.system("xrdcp -f ./%s_skimmed%s.root root://cmseos.fnal.gov//store/user/bgreenbe/eta_skimmed/"%(pl[0].split(".")[0], args.nickname)) 
       # for fn in filelist:
       #     os.system("rm ./{}_{}_*_ntuple.root".format(fn, year))
    else:
        #how many cores to try to use
        ncores = 4 
        payloads = []
        for fn in filelist:
            num = 0
            fullfile = fn + "_" + str(year) + "_" + str(num) + ".root"
            while os.path.exists(path + fullfile):
                payloads.append((fullfile, year, path, nevent, args.nickname, False, False, args.MC, blinded))
                num += 1
                fullfile = fn + "_" + str(year) + "_" + str(num) + ".root"
                
            if num == 0:
                print("ERROR: Error no files found.")
        import multiprocessing as mp
        pool  = mp.Pool(ncores)
        pool.map(makeskimstar, payloads)#this works for root output!
        pool.close()
        pool.join()

if __name__ == "__main__":
    main()
