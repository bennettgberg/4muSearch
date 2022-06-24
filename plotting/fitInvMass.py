#get the data from infile, fit to const bkg + gaussian.
from ROOT import TFile, TF1, TH1F, TCanvas

#infile = "hipTpair/data_DoubleMuon_Run2_skimmed.root"
#infile = "multiquad/data_DoubleMuon_Run2_skimmed.root"
#infile = "multimmg/data_DoubleMuon_Run2_skimmed.root"
infile = "oppocharge/data_DoubleMuon_Run2_skimmed.root"
distname = "Mmmee"
#distname = "Mmmg"
#accidentally used the wrong name!
#distname = "Ptmmee"

f = TFile.Open(infile)
f.Print()

t = f.Get("Events") 
t.Print()

nbins = 25 #30 #20 #10 # 20
xmin = .4 #.3 #.4 #.5 #.4
xmax = .9 #.7 #.9 #.8 #.9 #.7
#cgfit = TF1("cgfit", "([0] + [4]*x + gaus(1))", xmin, xmax);
cgfit = TF1("cgfit", "([0] + [6]*x + [7]*x*x + crystalball(1))", xmin, xmax);
#cgfit = TF1("cgfit", "([0] + gaus(1))", xmin, xmax);
cgfit.Print()

#cgfit.SetParameters(0, 1, 2, 3);
#cgfit.SetParameter(0, 2.1)
#cgfit.SetParameter(1, 6.5)
#cgfit.SetParameter(2, .546)
#cgfit.SetParameter(3, 0.018)
#cgfit.SetParameter(4, .01)

###gaussian starting params######
#cgfit.SetParameter(0, 0.5) #const
#cgfit.SetParameter(1, 5.0) #norm
##cgfit.SetParameter(1, 5000)
#cgfit.SetParameter(2, .548) #mean
##fix eta mass or nah??
##cgfit.FixParameter(2, .5479)
#cgfit.SetParameter(3, 0.018) #sigma
#
##slope of line for linear fit
#cgfit.SetParameter(4, .1)
####################################
###CrystalBall starting params####
cgfit.SetParameter(0, 0.3) #const
cgfit.SetParameter(1, 8)  #norm
cgfit.SetParameter(2, 0.548) #mean
#fix eta mass or nah??
#cgfit.FixParameter(2, .5479)
cgfit.SetParameter(3, 0.018) #sigma

cgfit.SetParameter(4, -2) #alph
cgfit.SetParameter(5, 2) #n
cgfit.SetParameter(6, .01) #slope
cgfit.SetParameter(7, .01) #quadratic coef

#initiate histogram
h = TH1F("h", "mu mu e e", nbins, xmin, xmax)
#h = TH1F("h", "mu mu gamma", nbins, xmin, xmax)

xax = h.GetXaxis()
xax.Print()
xax.SetTitle("4-lepton invariant mass (GeV)")
#xax.SetTitle("dimu-gamma invariant mass (GeV)")
yax = h.GetYaxis()
binsize = (xmax - xmin) / nbins
yax.SetTitle("Events / %f GeV"%binsize)

#fill histogram fast
t.Draw(distname + ">>h")

#raw_input("continue?")
#xax = cgfit.GetXaxis()
#xax.Print()
#cgfit.SetTitle("mu mu e e")
#xax.SetTitle("4-muon invariant mass (GeV)")
#yax = cgfit.GetYaxis()
#yax.SetTitle("Events / .015 GeV")
draw = True # False
#if draw:
#    h.Draw("hist")
#L for log likelihood fit instead of chi-squares
#V for verbose
#S for save fit
#B for some of the parameters are fixed
#fitresult = h.Fit("cgfit", "LS")
fitresult = h.Fit("cgfit", "LSB")

c = TCanvas("c", "c")
c.cd()
h.Draw()
#cgfit.SetLineColor(2)
#cgfit.Draw("same")
#h.Draw("same")
#cgfit.Draw("same")
#if draw:
#xax.Paint("same") 
#fitresult.Draw("same")

params = fitresult.GetParams()
const = params[0]
slope = params[6]
#slope = 0
mean = params[2]
sigma = params[3]

errors = fitresult.GetErrors()
#sigmaB = errors[0] * 6 * sigma / binsize
print("mean: %f, sigma: %f, const: %f"%(mean, sigma, const))
#find how many signal and background events under the peak
#bkgInt = const*6*sigma / binsize
#area under the bkg only
hi = .63 # mean+3*sigma
lo = .51 #mean-3*sigma
bkgInt = (0.5*slope*(hi**2 - lo**2) + const*(hi - lo) + 1.0/3 * params[7]*(hi**3 - lo**3) ) / binsize
quad_err = 1.0/3 * errors[7]*(hi**3 - lo**3) / binsize
print("quad_err: " + str(quad_err)) 
slope_err = (0.5*errors[6]*(hi**2 - lo**2)) / binsize
print("slope_err: " + str(slope_err)) 
const_err = (errors[0]*(hi - lo)) / binsize
print("const_err: " + str(const_err)) 
sigmaB = bkgInt**0.5 #((slope_err**2 + const_err**2 + quad_err**2 )**0.5)
#bkgInt = 2*3*sigma*const / binsize
#sigmaB = 2*3*sigma*errors[0] / binsize

sigInt = cgfit.Integral(lo, hi) / binsize - bkgInt

print("About %f signal events and %f +/- %f background events under the peak."%(sigInt, bkgInt, sigmaB))

from math import log
#l = log(1 + sigInt/bkgInt) 
#print("l: " + str(l))
#l2 = l*(sigInt + bkgInt)
#l3 = l2 - sigInt
#print("l3: " + str(l3)) 

#approximate significance (neglecting sigmaB)
#significance = (2*((sigInt + bkgInt)*log(1 + sigInt/bkgInt) - sigInt))**0.5

#significance taking sigmaB into account
significance = (2*((sigInt + bkgInt)*log((sigInt+bkgInt)*(bkgInt+sigmaB**2)/(bkgInt**2 + (sigInt+bkgInt)*sigmaB**2)) - bkgInt**2/sigmaB**2 *log(1 + sigmaB**2*sigInt/(bkgInt*(bkgInt+sigmaB**2)))))**0.5 

print("Significance is about %f sigmas."%(significance))
raw_input("h")
