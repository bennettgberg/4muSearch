import ROOT

def subtract(draw=False):
    #infileoppo = "oppocharge/data_DoubleMuon_Run2_skimmed.root"
    infileoppo = "data_DoubleMuon_Run2_skimmed.root"
    distname = "Mmmg"
    foppo = ROOT.TFile.Open(infileoppo)

    #infilesame = "data_DoubleMuon_Run2_skimmed.root"
    infilesame = "sametight/data_DoubleMuon_Run2_skimmed.root"
    fsame = ROOT.TFile.Open(infilesame)

    eventsoppo = foppo.Get("Events")

    eventssame = fsame.Get("Events")

    nbins = 30 #20 #30 #30 #20 #10 # 20
    xmin = .6 #.4 #.5 #.4
    xmax = 1.2 #.8 #.9 #.7
    #h = ROOT.TH1F("h", "mu mu gamma, Nmmg==1", nbins, xmin, xmax)
    h = ROOT.TH1F("h", "mu mu gamma", nbins, xmin, xmax)
    xax = h.GetXaxis()
    xax.Print()
    #xax.SetTitle("4-lepton invariant mass (GeV)")
    xax.SetTitle("dimu-gamma invariant mass (GeV)")
    yax = h.GetYaxis()
    binsize = (xmax - xmin) / nbins
    yax.SetTitle("Events / %f GeV"%binsize)

    #fill histogram slow
    mindR = 99999
    for i,e in enumerate(eventsoppo):
        if i%10000 == 0: print("Event %d / %d. Last mindR: %f"%(i, eventsoppo.GetEntries(), mindR)) 
        mindR = 99999
        minidx = -1
        for j in range(e.Nmmg):
            if e.PhodR[j] < mindR:
                minidx = j
                mindR = e.PhodR[j]
        if minidx > -1:
            h.Fill(e.Mmmg[minidx])
    c0 = ROOT.TCanvas("c0","c0")
    c0.cd()
    h.Draw("hist")
    #fill histogram fast
    #eventsoppo.Draw(distname + ">>h", "Nmmg==1")
    #eventsoppo.Draw(distname + ">>h")
    raw_input("continue?")

    c1 = ROOT.TCanvas("c1","c1")
    c1.cd()
    h2 = ROOT.TH1F("h2", "mu mu gamma", nbins, xmin, xmax)
    for i,e in enumerate(eventssame):
        if i%10000 == 0: print("Event %d / %d"%(i, eventssame.GetEntries())) 
        mindR = 99999
        minidx = -1
        for j in range(e.Nmmg):
            if e.PhodR[j] < mindR:
                minidx = j
                mindR = e.PhodR[j]
        if minidx > -1:
            h2.Fill(e.Mmmg[minidx])
    h2.Draw()
    #eventssame.Draw(distname + ">>h2", "Nmmg==1")
    #eventssame.Draw(distname + ">>h2")
    #raw_input("continue?")
    h.Add(h2, -1)
    if draw:
        c2 = ROOT.TCanvas("c2","c2")
        c2.cd()
        h.Draw()

        raw_input("h")

    return h

if __name__=="__main__":
    subtract(True)
