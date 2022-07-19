#get the data from infile, fit to const bkg + gaussian.
#from ROOT import TFile, TF1, TH1F, TCanvas, RooRealVar, RooDataHist, RooFit
import ROOT
import sys
#sys.path.append("../../tm_analysis/analysis/python/utils")
sys.path.append("../../tm_analysis/analysis/python")
#import fitter
import utils.fitter as fitter

#infile = "hipTpair/data_DoubleMuon_Run2_skimmed.root"
#infile = "multiquad/data_DoubleMuon_Run2_skimmed.root"
#infile = "multimmg/data_DoubleMuon_Run2_skimmed.root"
infile = "oppocharge/data_DoubleMuon_Run2_skimmed.root"
distname = "Mmmee"
#distname = "Mmmg"
#accidentally used the wrong name!
#distname = "Ptmmee"
compare_MC = True

f = ROOT.TFile.Open(infile)
f.Print()

t = f.Get("Events") 
t.Print()

nbins = 40 #30 #25 
xmin = .25 #.4 #.8
xmax = .9 #1.2

#initiate histogram
h = ROOT.TH1F("h", "mu mu e e", nbins, xmin, xmax)
#fill histogram fast
t.Draw(distname + ">>h")

c = ROOT.TCanvas("cnew","cnew")
c.cd()
#cgfit = TF1("cgfit", "([0] + [4]*x + gaus(1))", xmin, xmax);
#cgfit = TF1("cgfit", "([0] + [6]*x + [7]*x*x + crystalball(1))", xmin, xmax);
#cgfit = TF1("cgfit", "([0] + gaus(1))", xmin, xmax);
#cgfit.Print()


#signal shape is best described by a crystalBall.
rrv = ROOT.RooRealVar("m_{2#mu2e}","m_{2#mu2e} [GeV]",xmin,xmax)
#rrv = ROOT.RooRealVar("m_{2#mu2e}","m_{2#mu2e} [GeV]",0.5,0.9)
#rrv.setRange("peak", 0.53, 0.57)
rrv.setRange("peak", 0.51, 0.63)
rrv.setRange("full", xmin, xmax)
#rrv.setRange("peak", .9, 1.)
#rrv.setRange("full", .8, 1.2)
myfitter = fitter.fitter_4mu(mass=rrv)
#try a different bkg model!!
myfitter = fitter.fitter_4mu(mass=rrv, bkg_model='Threshold')
#myfitter = fitter.fitter_4mu(mass=.957)
print("created myfitter!!")
#now set the parameters appropriately.
#from collections import namedtuple
#import fit_function_library as library
import utils.fit_function_library as library
#try to do like this: 'Param', ['val', 'min', 'max']
#myfitter.set_sig_params(mcb=library.Param(.957, .9, 1.0), acb=library.Param(-4.5, -6, -0.5), ncb=library.Param(21, 20, 22), scb=library.Param(.0195, .01, .02))
#myfitter.set_bkg_params( a1=library.Param(.987, -1, 1), a2=library.Param(.145, -1, 1) )
#trying different bkg model!! (Threshold)
myfitter.set_bkg_params( alpha=library.Param(1, 0.5, 5), x0=library.ConstParam(.2122) )
myfitter.set_sig_params( mcb=library.Param(.549, .5, .6), acb=library.Param(-4.5, -6, -0.5), ncb=library.Param(21, 15, 25), scb=library.Param(.0195, .01, .02) )
#myfitter.set_bkg_params()
print("set new signal params!!!")

data = ROOT.RooDataHist("data", "data", rrv, ROOT.RooFit.Import(h))

#do the fit
myfitter.model.fitTo(data)

#plot the fit
frame = rrv.frame()
#data.plotOn(frame, Name="Data", DrawOption="PEZ")
data.plotOn(frame, ROOT.RooFit.Name("Data"), ROOT.RooFit.DrawOption("PEZ"))


myfitter.model.plotOn(frame, ROOT.RooFit.Name("Bkg"), ROOT.RooFit.Components('bkg'), ROOT.RooFit.LineWidth(5), ROOT.RooFit.LineStyle(2), ROOT.RooFit.LineColor(ROOT.kGreen-1))
myfitter.model.plotOn(frame, ROOT.RooFit.Name("Sig"), ROOT.RooFit.Components('CB'), ROOT.RooFit.LineWidth(5), ROOT.RooFit.LineStyle(4), ROOT.RooFit.LineColor(ROOT.kRed+1))
#myfitter.model.plotOn(frame, ROOT.RooFit.Name("Tot"), ROOT.RooFit.LineWidth(5), ROOT.RooFit.LineColor(ROOT.kBlue))
myfitter.model.plotOn(frame, ROOT.RooFit.Name("Tot"), ROOT.RooFit.LineWidth(4), ROOT.RooFit.LineColor(ROOT.kBlue))
#myfitter.model.plotOn(frame, ROOT.RooFit.Name("Bkg"), ROOT.RooFit.Components({myfitter.bkg}), ROOT.RooFit.LineWidth(5), ROOT.RooFit.LineStyle('--'), ROOT.RooFit.LineColor(ROOT.kGreen-1))
#myfitter.model.plotOn(frame, ROOT.RooFit.Name("Sig"), ROOT.RooFit.Components({myfitter.sig}), ROOT.RooFit.LineWidth(5), ROOT.RooFit.LineStyle('-.'), ROOT.RooFit.LineColor(ROOT.kRed+1))
frame.Print()
frame.Draw("AC")
c.Modified()
c.Update()

ndata = h.Integral(h.FindBin(0.51), h.FindBin(0.63))
#ndata = h.Integral(h.FindBin(0.90), h.FindBin(1.0))
argset = ROOT.RooArgSet(rrv)
sig_int = myfitter.sig.func.createIntegral(argset, ROOT.RooFit.NormSet(argset), ROOT.RooFit.Range("peak"))
bkg_int = myfitter.bkg.func.createIntegral(argset, ROOT.RooFit.NormSet(argset), ROOT.RooFit.Range("peak"))
tot_int = myfitter.model.createIntegral(argset, ROOT.RooFit.NormSet(argset), ROOT.RooFit.Range("peak"))
print("sigvals: %f, %f; bkgvals: %f, %f"%(sig_int.getVal(), myfitter.nsig.getVal(), bkg_int.getVal(), myfitter.nbkg.getVal())) 
nsig = sig_int.getVal() * myfitter.nsig.getVal()
nbkg = bkg_int.getVal() * myfitter.nbkg.getVal()
ntot = tot_int.getVal() * (myfitter.nsig.getVal() + myfitter.nbkg.getVal())

bkghi = bkg_int.getVal() * myfitter.nbkg.getAsymErrorHi() 
bkglo = bkg_int.getVal() * myfitter.nbkg.getAsymErrorLo() 

print("bkg errors: %f, %f "%(bkghi, bkglo)) 

#leg = ROOT.TLegend(0.4, 0.65, 0.8, 0.85)
leg = ROOT.TLegend(0.15, 0.65, 0.45, 0.85)
leg.SetHeader("N: m_{2#mu2e} #in [0.51, 0.63] GeV")
#leg.SetHeader("N: m_{2#mu2e} #in [0.9, 1.0] GeV")
leg.SetLineWidth(0)
leg.AddEntry("Sig", f"Signal (CB): N = {nsig:.1f}", "l")
leg.AddEntry("Bkg", f"Background: N = {nbkg:.1f}", "l")
leg.AddEntry("Tot", f"Sum: N = {ntot:.1f}", "l")
leg.AddEntry("Data", f"Data, N = {ndata:n}", "lep")
leg.Draw()
####################################
###CrystalBall starting params####
#cgfit.SetParameter(0, 0.3) #const
#cgfit.SetParameter(1, 8)  #norm
#cgfit.SetParameter(2, 0.548) #mean
##fix eta mass or nah??
##cgfit.FixParameter(2, .5479)
#cgfit.SetParameter(3, 0.018) #sigma
#
#cgfit.SetParameter(4, -2) #alph
#cgfit.SetParameter(5, 2) #n
#cgfit.SetParameter(6, .01) #slope
#cgfit.SetParameter(7, .01) #quadratic coef

#initiate histogram
#h = TH1F("h", "mu mu gamma", nbins, xmin, xmax)

#xax = h.GetXaxis()
#xax.Print()
#xax.SetTitle("4-lepton invariant mass (GeV)")
##xax.SetTitle("dimu-gamma invariant mass (GeV)")
#yax = h.GetYaxis()
#binsize = (xmax - xmin) / nbins
#yax.SetTitle("Events / %f GeV"%binsize)
#
#
#draw = True # False
#fitresult = h.Fit("cgfit", "LSB")
#
#c = TCanvas("c", "c")
#c.cd()
#h.Draw()
#
#params = fitresult.GetParams()
#const = params[0]
#slope = params[6]
##slope = 0
#mean = params[2]
#sigma = params[3]
#
##area under the bkg only
#hi = .63 # mean+3*sigma
#lo = .51 #mean-3*sigma
#bkgInt = (0.5*slope*(hi**2 - lo**2) + const*(hi - lo) + 1.0/3 * params[7]*(hi**3 - lo**3) ) / binsize
#
#sigInt = cgfit.Integral(lo, hi) / binsize - bkgInt
#
#print("About %f signal events and %f +/- %f background events under the peak."%(sigInt, bkgInt, sigmaB))
#
from math import log
##l = log(1 + sigInt/bkgInt) 
##print("l: " + str(l))
##l2 = l*(sigInt + bkgInt)
##l3 = l2 - sigInt
##print("l3: " + str(l3)) 
#
##approximate significance (neglecting sigmaB)
##significance = (2*((sigInt + bkgInt)*log(1 + sigInt/bkgInt) - sigInt))**0.5
#
##significance taking sigmaB into account
sigInt = nsig
bkgInt = nbkg
sigmaB = max(bkglo, bkghi)
significance = (2*((sigInt + bkgInt)*log((sigInt+bkgInt)*(bkgInt+sigmaB**2)/(bkgInt**2 + (sigInt+bkgInt)*sigmaB**2)) - bkgInt**2/sigmaB**2 *log(1 + sigmaB**2*sigInt/(bkgInt*(bkgInt+sigmaB**2)))))**0.5 
#
print("Significance is about %f sigmas."%(significance))

#draw MC first (if drawing it)
if compare_MC:
    fMC = ROOT.TFile.Open("EtaTo2Mu2E_2018_0_skimmedMCtest.root")
    tMC = fMC.Get("Events")

    #MC_scales = [3.0, 2.0, 1.0, 0.5]
    MC_scales = [2.0]
    hMC = [None for mcs in MC_scales]
    #draw the blinded MC scaled by a few different values
    for i,scale in enumerate(MC_scales):
        hMC[i] = ROOT.TH1F("hMC"+str(i), "#mu#muee", nbins, xmin, xmax)
        hMC[i].SetLineWidth(2)
        color = 7+i
        #10 is just white \throwingUpEmoji
        if color >= 9: color += 2
        #hMC[i].SetLineColor(color)
        hMC[i].SetLineColor(ROOT.kOrange)
        #switch to a temporary canvas so don't draw bs on the good canvas??
        #ctemp = TCanvas("ctemp", "ctemp")
        #ctemp.cd()
        drawopt = "hist same"
        #if i > 0: drawopt += " same"
        tMC.Draw(distname + ">>hMC"+str(i), str(scale)+"*Weight*(Weight>0)", drawopt)
        #c.cd()
        #hMC.Draw("hist same")
#if compare_MC:
#    for i,scale in enumerate(MC_scales):
        leg.AddEntry(hMC[i],"(signal MC)*"+str(scale)+"*(blinding factor)", "l")
    c.Update()

#use official CMS Style.
import utils.CMSStyle as cmsstyle
#cmsstyle.setCMSLumiStyle(c, 99999999999)
c.Update()
input("h")
