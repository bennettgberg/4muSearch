import ROOT, sys, time
sys.path.insert(1,'../code/')
import muFun
from array import array

#this script will make 'ultra-skimmed' ntuples out of the ntuples I already have.
# Will save only important things that can be easily plotted, such as M4L of the 4 best
#  muons; weights for each event; etc.


#fileName = #"data_DoubleMuonB_skimmed_2017.root"
#name = sys.argv[1].split(".")[0]
def makeskim(filename, yr, path, nevent, nickname, debug=False):
    if yr not in [2016, 2017, 2018]:
        print("Error: only Run2 (2016,2017,2018) allowed for now.")
        sys.exit()
    name = filename.split(".")[0]
    fileName = name + "_skimmed" + nickname + ".root"
    hname = 'h' + name

    outF = ROOT.TFile( fileName, 'recreate' )
    #have to create this before opening the file fsr??
    newT = ROOT.TTree( 'Events', 'Output tree' )

    #max number of dimu pairs to keep
    # (keep nMax^2 4-lepton pairpairs)
    nMax = 10
    m2l = array('f', [0]*nMax)
    m2e = array('f', [0]*nMax)
#    m4l = array('f', [0]*nMax)
    #4mu mass
    mmmmm = array('f', [0]*nMax*nMax)
    #invariant mass of the mmee system
    mmmee = array('f', [0]*nMax*nMax)
    pt2l = array('f', [0]*nMax)
    pt2e = array('f', [0]*nMax)
    #pt4l = array('f', [0]*nMax)
    ptmmmm = array('f', [0]*nMax*nMax)
    ptmmee = array('f', [0]*nMax*nMax)
    event = array('l', [0])
    run = array('l', [0])
    Nmmmm = array('l', [0])
    Nmmee = array('l', [0])
    nwords = 4
    triggerWord = array('l', [0]*nwords)
    newT.Branch("M2l", m2l, "M2l[%d]/F"%(nMax))
    newT.Branch("M2e", m2e, "M2e[%d]/F"%(nMax))
    newT.Branch("Mmmmm", mmmmm, "Mmmmm/F")
    newT.Branch("Mmmee", mmmee, "Mmmee/F")
    newT.Branch("Pt2l", pt2l, "Pt2l[%d]/F"%(nMax))
    newT.Branch("Pt2e", pt2e, "Pt2e[%d]/F"%(nMax))
    newT.Branch("Ptmmmm", ptmmmm, "Ptmmmm[%d]/F"%(nMax*nMax))
    newT.Branch("Ptmmee", ptmmee, "Ptmmee[%d]/F"%(nMax*nMax))
    newT.Branch("event", event, "event/l")
    newT.Branch("run", run, "run/l")
    newT.Branch("Nmmmm", Nmmmm, "Nmmmm/l")
    newT.Branch("Nmmee", Nmmee, "Nmmee/l")
    newT.Branch("triggerWord", triggerWord, "triggerWord[%d]/l"%(nwords))
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
    print("got Events tree.")
    nevents = t.GetEntries()
    ncut = 0
    import generalFunctions as GF
    print("got generalFunctions.")
    cutCounter = GF.cutCounter()
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
    #keep trying until it works (at most 5 times)
    #succeeded?
    succ = False
    for trynum in range(10):
        try:
            print("about to start loop.")
            for i,e in enumerate(t):
                if nevent > -1 and i > nevent: break
                if i % 10000 == 0:
                    print("Now processing event %d out of %d for %s_%d"%(i, nevents, fl, yr))
                dbg = False
                #if e.run == dbg_run and e.evt in dbg_evts:
                #    dbg = True
                #    print("***Run=%d, event=%d***"%(dbg_run, e.evt))
                #    #print event arguments: entry, isMC, isntuple
                #    GF.printEvent(e, False, True)
                cutCounter.count('All')
                #first make the stricter selections
                #make sure at least one of the dimu triggers was passed
                passed_trig = False
                for j in range(nwords):
                    if e.dimuTriggerWord[j] > 0:
                        passed_trig = True
                        break
                if not passed_trig:
               #     ncut += 1
                    if dbg:
                        print("failed trigger.")
               #     continue
                cutCounter.count('Passed trigger')
                # (getGoodLists will return array of 4 identical lists (bc all particles are muons))
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
                #sometimes all leptons are too close to each other or something
                if len(pairList) < 1:
                    ncut += 1
                    if dbg:
                        print("failed good muon pair.")
                    continue
                cutCounter.count('1 good muon pair')
                
                if len(pairList) > nMax: 
                    #print("Error: pairList length is %d but nMax is only %d."%(len(pairList), nMax))
                    #print("pairList: " + str(pairList))
                    #sys.exit()
                    #break
                    pass
                #get the nMax pairs with lowest invariant mass.
                invmasses = [0. for j in range(len(pairList))]
                pTs = [0. for j in range(len(pairList))]
                #first get all the invmasses, pTs
                for j in range(len(pairList)):
                    #get the 4-vectors
                    leps = [] #lorentz vectors
                    for k in range(2):
                        leps.append( muFun.get4vec('m', e, pairList[j][k]) )
                    #get the invariant mass of the pair 
                    v2l = (leps[0] + leps[1])
                    M = v2l.M()
                    pt = v2l.Pt()
                    invmasses[j] = M
                    pTs[j] = pt
                #now get the nMax with lowest invmass.
                for j in range(nMax):
                    if len(invmasses) > 0:
                        mmin = min(invmasses)
                        m2l[j] = mmin
                        #k is the index of the min invariant mass.
                        k = invmasses.index(mmin)
                        pt2l[j] = pTs[k]
                        #remove these values from the lists so they won't be found again next iteration.
                        del invmasses[k]
                        del pTs[k]
                    else:
                        m2l[j] = -99
                        pt2l[j] = -99
                
                for cat in ['mmmm', 'mmee']:
                    #some events will have 2 good muon pairs, some won't.
                    pairlist2 = pairList
                    if 'e' in cat: pairlist2 = epairList
                    allpair2s = muFun.getAllPair2s(cat, e, pairList, pairlist2)
                    for j in range(nMax*nMax):
                        exec("pt%s[j] = -99"%(cat))
                        exec("m%s[j] = -99"%(cat))
                    exec("N%s[0] = len(allpair2s)"%(cat))
                    if len(allpair2s) < 1 or len(allpair2s[0]) < 1:
                            if dbg:
                                print("failed 2 good muon pairs.")
                            #continue
                    else:
                        #we want to keep ALL pair2s, not just the 'best' one.
                        #print("allpair2s: " + str(allpair2s))
                        #if len(allpair2s) > nMax*nMax:
                        #    #nMax^2 items are allowed for the 4-lepton variables
                        #    print("Error! %d pair2s but nMax is only %d for cat %s."%(len(allpair2s), nMax, cat))
                        #    sys.exit()
                        #find the nMax^2 lowest invmasses, save only those.
                        invmasses = [0. for j in allpair2s]
                        pTs = [0. for j in allpair2s]
                        for j in range(len(allpair2s)):
                            fveclist, lepList, bestPair = muFun.getBestPairs(cat, e, [allpair2s[j]])
                            eta4vec = fveclist[0] + fveclist[1] + fveclist[2] + fveclist[3]
                            M = eta4vec.M()
                            pt = eta4vec.Pt()
                            invmasses[j] = M
                            pTs[j] = pt
                        for j in range(nMax**2):
                            if len(invmasses) > 0:
                                mmin = min(invmasses)
                                k = invmasses.index(mmin)
                                exec("pt%s[j] = mmin"%(cat))
                                exec("m%s[j] = pTs[k]"%(cat))
                                del invmasses[k]
                                del pTs[k]
                            else:
                                #already set everything to -99 above.
                                break
                cutCounter.count('2 good muon pairs')

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

                event[0] = e.evt
                run[0] = e.run
                #write output root file.
                #print("newT: " + str(newT))
                #newT.Print()
                newT.Fill()
        except RuntimeError:
            print("I/O error for %s_%d. Retrying (try #%d)."%(fl, yr, trynum))
            inF.Close()
            time.sleep(120)
            inF = ROOT.TFile(full_path)
            t = inF.Get("Events")
            continue

        print("%s_%d succeeded on try number %d"%(fl, yr, trynum))
        succ = True
        break

    if not succ:
        print("Error: I/O error for %s_%d!"%(fl, yr))
        raise RuntimeError
    outF.Write()
    inF.Close()
    cutCounter.printSummary()
    print("Cut %d events out of %d total ( %f %% ) for %s_%d."%(ncut, nevents, (100.0*ncut/nevents), fl, yr))

#helper function used only for multiprocessing
def makeskimstar(ploads):
    #print("arguments for makeskim: " + str(*ploads))
    return makeskim(*ploads)    

def main():
    #parse input arguments
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--nevents",default=-1,type=int,help="Number of events to process in each file (-1 default to do all events)")
    parser.add_argument("-d","--debug",default=False,action='store_true',help="run in debug mode (no multiprocessing) or nah")
    parser.add_argument("-nn","--nickname",default="",type=str,help="nickname for output file (to distinguish it).")
    parser.add_argument("-y","--year",default=2016,type=int,help="year (2016, 2017, or 2018).")                     
    parser.add_argument("-c","--incsv",default="bpgSamples.csv",type=str,help="name of input csv file with all the file names in it.")                     
    parser.add_argument("-t","--testname",default="",type=str,help="name appended to all for the ntuple files that we're going to read. eg noee for all_noee")
    args = parser.parse_args()

    #get the list of processes from the csv.
    incsv = args.incsv
    incsf = open(incsv, "r")
    filelist = []
    for lin in incsf:
        samp = lin.split(',')[0]
        filelist.append(samp)

    nevent = args.nevents
    year = args.year
    #path to ntuple files
    path = "/eos/uscms/store/user/bgreenbe/eta_{}/all{}/".format(year, "_"+args.testname if args.testname != "" else "")

    print("filelist: " + str(filelist))
    #if debug mode requested do not try to multi-thread.
    if args.debug:
            for fn in filelist:
                num = 0
                fullfile = fn + "_" + str(year) + "_" + str(num) + ".root"
                print("file path: " + path + fullfile)
                while os.path.exists(path + fullfile):
                    makeskim(fullfile, year, path, nevent, args.nickname, args.debug)    
                    num += 1
                    fullfile = fn + "_" + str(year) + "_" + str(num) + ".root"
                if num == 0:
                    print("Error: path to file(s) not found.")
    else:
        #how many cores to try to use
        ncores = 8 
        payloads = []
        for fn in filelist:
            num = 0
            fullfile = fn + "_" + str(year) + "_" + str(num) + ".root"
            while os.path.exists(path + fullfile):
                payloads.append((fullfile, year, path, nevent, args.nickname))
                num += 1
                fullfile = fn + "_" + str(year) + "_" + str(num) + ".root"
                
        import multiprocessing as mp
        pool  = mp.Pool(ncores)
        pool.map(makeskimstar, payloads)#this works for root output!
        pool.close()
        pool.join()

if __name__ == "__main__":
    main()
