#get the data from infile, fit to const bkg + gaussian.
from ROOT import TFile, TF1, TH1F

infile = "hipTpair/data_DoubleMuon_Run2_skimmed.root"
distname = "Mmmee"

f = TFile.Open(infile)
f.Print()

t = f.Get("Events") 
t.Print()

cgfit = TF1("cgfit", "([0] + gaus(1))", 0.4, 0.7);
cgfit.Print()

cgfit.SetParameters(0, 1, 2, 3);

#cgfit.SetRange(0.4,0.7);

#initiate histogram
nbins = 20
xmin = .4
xmax = .7
h = TH1F("h", "mu mu e e", nbins, xmin, xmax)

xax = h.GetXaxis()
xax.Print()
xax.SetTitle("4-lepton invariant mass (GeV)")
yax = h.GetYaxis()
binsize = (xmax - xmin) / nbins
yax.SetTitle("Events / %f GeV"%binsize)

#fill histogram fast
t.Draw("Mmmee>>h")

#xax = cgfit.GetXaxis()
#xax.Print()
#cgfit.SetTitle("mu mu e e")
#xax.SetTitle("4-muon invariant mass (GeV)")
#yax = cgfit.GetYaxis()
#yax.SetTitle("Events / .015 GeV")
draw = False
if draw:
    h.Draw("hist")

#L for log likelihood fit instead of chi-squares
#V for verbose
#S for save fit
fitresult = h.Fit("cgfit", "LS")

if draw:
    cgfit.Draw("same")
#xax.Paint("same") 
#fitresult.Draw("same")

params = fitresult.GetParams()
const = params[0]
mean = params[2]
sigma = params[3]

errors = fitresult.GetErrors()
sigmaB = errors[0]
print("mean: %f, sigma: %f, const: %f"%(mean, sigma, const))
#find how many signal and background events under the peak
bkgInt = const*6*sigma / binsize

sigInt = cgfit.Integral(mean-3*sigma, mean+3*sigma) / binsize - bkgInt

print("About %f signal events and %f background events under the peak."%(sigInt, bkgInt))

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

print("Expected significance is about %f sigmas."%(significance))
raw_input("h")
