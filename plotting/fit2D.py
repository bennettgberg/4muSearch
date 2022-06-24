import ROOT
import sys
sys.path.append("../../tm_analysis/analysis/python/utils")
import fitter

#name of the input file
infile = "data_DoubleMuon_Run2_skimmed.root"

subtract = True

#name of the invariant mass distribution of interest
invMname = "Mmmg"

#name of the pt distribution of interest
pTname = "Ptmmg"

#open the input file
f = ROOT.TFile.Open("oppotight/" + infile)
f.Print()

#get the events tree
t = f.Get("Events")
#t.Print()

#initiate the 2D histogram
#how many bins on the pT axis
nptbins = 10 # 100
#min, max pt values for the hist
ptmin = 12 
ptmax = 212 
#how many bins on the invariant mass axis
nimbins = 20
#min, max invariant mass values for the hist
immin = .8
immax = 1.2 

#min, max cutoffs for the signal peak
#trying some whack cutoffs just to see what happens
pkmin = .9
pkmax = 1.0

h2d = ROOT.TH2F("h2d", "h2d", nptbins, ptmin, ptmax, nimbins, immin, immax)

#Fill the histogram
c = ROOT.TCanvas("c2d","c2d")
c.cd()
t.Draw(invMname + ":" + pTname + ">>h2d", "", "colz") 
print("Og h2d has " + str(h2d.GetEntries()) + " entries.")
c.SaveAs(invMname + "_vs_" + pTname + ".png")
if subtract:
    infile2 = "sametight/%s"%(infile)
    f2 = ROOT.TFile.Open(infile2)
    t2 = f2.Get("Events")
    h2d_same = ROOT.TH2F("h2dsame", "h2dsame", nptbins, ptmin, ptmax, nimbins, immin, immax)
    c = ROOT.TCanvas("c2dsame","c2dsame")
    c.cd()
    t2.Draw(invMname + ":" + pTname + ">>h2dsame", "", "colz") 
    print("h2dsame has " + str(h2d_same.GetEntries()) + " total entries.")
    c.SaveAs(invMname + "_vs_" + pTname + "_samesign.png")
    h2d.Add(h2d_same, -1)
    print("h2d after subtraction has " + str(h2d.GetEntries()) + " entries total.")
    c = ROOT.TCanvas("c2dsub", "c2dsub")
    c.cd()
    h2d.Draw("colz")
    c.SaveAs(invMname + "_vs_" + pTname + "_subtracted.png")
#input("h")

myfitter = [0 for ipt in range(nptbins)] 
rrv = [0 for ipt in range(nptbins)] 
#Now in each pT bin, fit a bkg+gaussian to the invM
for ipt in range(nptbins):
    print("************Starting pT bin " + str(ipt) + "***************")
    #signal shape is best described by a crystalBall.
    rrv[ipt] = ROOT.RooRealVar("m_{#mu#mu#gamma}" + str(ipt),"m_{#mu#mu#gamma} [GeV]",immin,immax)
    rrv[ipt].setRange("peak", pkmin, pkmax)
    rrv[ipt].setRange("full", immin, immax)
    myfitter[ipt] = fitter.fitter_4mu(mass=rrv[ipt])

    #now get the data from this pt bin of the 2d histogram
    h = h2d.ProjectionY("h", ipt+1, ipt+1)
    print("h" + str(ipt) + ":") 
    h.Print()
    bincenter = h.GetBinCenter(ipt)
    c = ROOT.TCanvas("hhh"+str(ipt), "h_pt" + str(bincenter))
    c.cd()
    #print("first few bins: " + str(h.GetBinContent(1)) + ", " + str(h.GetBinContent(2)) + ", " + str(h.GetBinContent(3))) 
    h.Draw("hist")
    c.Update()
    #input("here is the projection of h2d for bin" + str(ipt) + ". It has " + str(h.GetEntries()) + " entries.")
    c = ROOT.TCanvas("cnew"+str(ipt),"cnew"+str(ipt))
    c.cd()
    data = ROOT.RooDataHist("data"+str(ipt), "data"+str(ipt), rrv[ipt], ROOT.RooFit.Import(h))

    #do the fit
    myfitter[ipt].model.fitTo(data)

    #plot the fit
    frame = rrv[ipt].frame()
    #data.plotOn(frame, Name="Data", DrawOption="PEZ")
    data.plotOn(frame, ROOT.RooFit.Name("Data"), ROOT.RooFit.DrawOption("PEZ"))
    myfitter[ipt].model.plotOn(frame, ROOT.RooFit.Name("Bkg"), ROOT.RooFit.Components('bkg'), ROOT.RooFit.LineWidth(5), ROOT.RooFit.LineStyle(2), ROOT.RooFit.LineColor(ROOT.kGreen-1))
    myfitter[ipt].model.plotOn(frame, ROOT.RooFit.Name("Sig"), ROOT.RooFit.Components('CB'), ROOT.RooFit.LineWidth(5), ROOT.RooFit.LineStyle(4), ROOT.RooFit.LineColor(ROOT.kRed+1))
    myfitter[ipt].model.plotOn(frame, ROOT.RooFit.Name("Tot"), ROOT.RooFit.LineWidth(5), ROOT.RooFit.LineColor(ROOT.kBlue))
    frame.Print()
    frame.Draw("AC")
    c.Modified()
    c.Update()

    ndata = h.Integral(h.FindBin(pkmin), h.FindBin(pkmax))
    argset = ROOT.RooArgSet(rrv[ipt])
    sig_int = myfitter[ipt].sig.createIntegral(argset, ROOT.RooFit.NormSet(argset), ROOT.RooFit.Range("peak"))
    bkg_int = myfitter[ipt].bkg.createIntegral(argset, ROOT.RooFit.NormSet(argset), ROOT.RooFit.Range("peak"))
    tot_int = myfitter[ipt].model.createIntegral(argset, ROOT.RooFit.NormSet(argset), ROOT.RooFit.Range("peak"))
    print("sigvals: %f, %f; bkgvals: %f, %f"%(sig_int.getVal(), myfitter[ipt].nsig.getVal(), bkg_int.getVal(), myfitter[ipt].nbkg.getVal())) 
    nsig = sig_int.getVal() * myfitter[ipt].nsig.getVal()
    nbkg = bkg_int.getVal() * myfitter[ipt].nbkg.getVal()
    ntot = tot_int.getVal() * (myfitter[ipt].nsig.getVal() + myfitter[ipt].nbkg.getVal())

    bkghi = bkg_int.getVal() * myfitter[ipt].nbkg.getAsymErrorHi() 
    bkglo = bkg_int.getVal() * myfitter[ipt].nbkg.getAsymErrorLo() 

    print("bkg errors: %f, %f "%(bkghi, bkglo)) 

    #TLegend constructor: x1, y1, x2, y2
    leg = ROOT.TLegend(0.6, 0.2, 0.95, 0.5)
    leg.SetHeader("N: m_{2#mu2e} #in [0.9, 1.0] GeV")
    leg.SetLineWidth(0)
    leg.AddEntry("Sig", f"Signal (CB): N = {nsig:.1f}", "l")
    leg.AddEntry("Bkg", f"Background: N = {nbkg:.1f}", "l")
    leg.AddEntry("Tot", f"Sum: N = {ntot:.1f}", "l")
    leg.AddEntry("Data", f"Data, N = {ndata:n}", "lep")
    leg.Draw()
    from math import log
    ##significance taking sigmaB into account
    sigInt = nsig
    if sigInt < 0:
        print("Warning: sigInt = %f; setting to 0."%(sigInt)) 
        sigInt = 0
    bkgInt = nbkg
    sigmaB = max(bkglo, bkghi)
    significance = (2*((sigInt + bkgInt)*log((sigInt+bkgInt)*(bkgInt+sigmaB**2)/(bkgInt**2 + (sigInt+bkgInt)*sigmaB**2)) - bkgInt**2/sigmaB**2 *log(1 + sigmaB**2*sigInt/(bkgInt*(bkgInt+sigmaB**2)))))**0.5 
    print("sigInt: %f, bkgInt: %f (+%f/-%f), sigmaB: %f"%(sigInt, bkgInt, bkghi, bkglo, sigmaB))
    try:
        print("Significance is about %f sigmas."%(significance))
    except TypeError:
        print("Significance is 0.")
    c.Update()
    #input("h")
    plotname = invMname + "_pTbin" + str(ipt) + ".png"
    c.SaveAs(plotname)
