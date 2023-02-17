import ROOT

#script to plot MC comparison plots

issig = False
#names of the input files
n0 = "eMVA0/EtaTo2Mu2E_2018_0_ntuple_skimmedsignalMC.root"
nL = "EtaTo2Mu2E_2018_0_ntuple_skimmedsignalMC.root"
if not issig:
    n0 = "eMVA0/EtaToMuMuGamma_2018_0_ntuple_skimmedBkgMC.root"
    nL = "EtaToMuMuGamma_2018_0_ntuple_skimmedBkgMC.root"

f0 = ROOT.TFile(n0)
fL = ROOT.TFile(nL)

t0 = f0.Get("Events")
tL = fL.Get("Events")

xmax = .9
xmin = .25
nbins = 40
h0 = ROOT.TH1F("h0", "h0", nbins, xmin, xmax)
hL = ROOT.TH1F("hL", "hL", nbins, xmin, xmax)

t0.Draw("Mmmee>>h0", "Weight*(Mmmee>-99)") 
tL.Draw("Mmmee>>hL", "Weight*(Mmmee>-99)") 

c1 = ROOT.TCanvas()
c1.cd()

h0.SetLineColor(ROOT.kBlue)
hL.SetLineColor(ROOT.kRed)

h0.SetLineWidth(2)
hL.SetLineWidth(2)

h0.Draw("hist")
hL.Draw("hist same")

binwidth = (xmax - xmin)/nbins
h0.GetXaxis().SetTitle("M_{#mu#mu ee} (GeV)")
h0.GetYaxis().SetTitle("Events / %.5f GeV"%(binwidth))
if issig:
    h0.SetTitle("Signal MC electron MVA Comparison")
else:
    h0.SetTitle("Bkg MC electron MVA Comparison")

leg = ROOT.TLegend(.15, .7, .4, .85)
leg.AddEntry(h0, "No e^{-} MVA cut")
leg.AddEntry(hL, "Loose e^{-} MVA cut")
leg.Draw("same")

c1.Update()
input("exit?...") 
