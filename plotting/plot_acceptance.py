import ROOT

#mode is sig or bkg
mode = "sig"

if mode == "sig":
    trig_path = "/eos/uscms/store/user/bgreenbe/EtaTo2Mu2E/NANOAOD_Signal_Samples/trigEff.root"
    reco_path = "/eos/uscms/store/user/bgreenbe/EtaTo2Mu2E/NANOAOD_Signal_Samples/recoEff.root"
    comb_path = "/eos/uscms/store/user/bgreenbe/EtaTo2Mu2E/NANOAOD_Signal_Samples/combinedEff.root"
else:
    trig_path = "../trigEffBkg.root"
    reco_path = "../recoEffBkg.root"
    comb_path = "../combinedEffBkg.root"

paths = [   
    trig_path,
    reco_path,
    comb_path  ]

c = ROOT.TCanvas("c", "c")
#c.cd()
leg = ROOT.TLegend(.6, .3, .9, .5)
hpassed = [None for path in paths]
f = [None for path in paths]
for i,path in enumerate(paths):
    print("Opening %s"%(path)) 
    f[i] = ROOT.TFile.Open(path)

    hpname = "hpassed"
    hpassed[i] = f[i].Get(hpname)
    hpassed[i].SetName(hpname + str(i)) 
    hpassed[i].SetTitle(hpname + str(i)) 
    print("Got object %s."%(hpassed[i].GetName())) 
    
    haname = "hall"
    hall = f[i].Get(haname)

    hpassed[i].Rebin(5)
    hall.Rebin(5)

    hpassed[i].Divide(hall)

    color = i+2
    hpassed[i].SetMarkerColor(color)
    hpassed[i].SetLineColor(color)
    hpassed[i].SetLineWidth(2)
    
    #name for the legend
    legName = "Signal" if mode == "sig" else "Background"
    if i == 0:
        legName += " trigger efficiency"
    elif i == 1:
        legName += " reco efficiency"
    elif i == 2:
        legName += " acceptance"
    leg.AddEntry(hpassed[i], legName)

    print("Drawing hpassed from %s"%(path)) 
    #c.cd()
    if i == 0:
        hpassed[i].Draw()
    else:
        hpassed[i].Draw("same")
    #input("<ENTR> to continue. regards") 

#c.cd()
hpassed[0].GetXaxis().SetTitle("gen pT (GeV)")
hpassed[0].GetYaxis().SetTitle("Efficiency") 
hpassed[0].SetTitle("%s Efficiencies and Acceptance"%("Signal" if mode == "sig" else "Background"))
hpassed[0].SetStats(0)
#hpassed[0].SetMinimum(0.0001)
hpassed[0].SetMinimum(0.00001)
leg.Draw("same")
c.SetLogy()
c.Update()
input("<ENTR> to exit. regards") 
