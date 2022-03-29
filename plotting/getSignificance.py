import ROOT

#root file with all of the data from Run2
infile = "data_DoubleMuon_Run2_skimmed.root"

#get the file
f = ROOT.TFile(infile)

#name of the distribution we're interested in
distname = "Mmmee"

#get the distribution
#tree = f.Get("Events")
dist = f.Get("Events")
#dist = tree.GetBranch(distname)
dist.Print()

#now construct the model that we will fit
#constant background
const = ROOT.RooRealVar("const", "constant background", 0.5, 0.01, 5.0)

#low cutoff for signal mass
locut = .4

#high cutoff for signal mass
hicut = .7

#make variable for eta mass (which we'll be fitting).
meta = ROOT.RooRealVar("Mmmee", "m_{#mu #mu ee}", locut, hicut)

#now make the constant model object thing.
bkg = ROOT.RooBernstein("bkg", "bkg", meta, ROOT.RooArgList(const))
print("bkg: ")
bkg.Print()

meanvar = ROOT.RooRealVar("mean", "mean", .547, .547, .547)
sigmavar = ROOT.RooRealVar("sigma", "sigma", .02, 0.001, 0.2)
print("meanvar: ")
meanvar.Print()
print("sigmavar: ")
sigmavar.Print()
#gaussian signal, between .4 and .7 GeV, mean .547
sig = ROOT.RooGaussian("sigGauss", "gaussian signal", meta, meanvar, sigmavar)
print("sig: ")
sig.Print()

#variable for normalizing bt gaussian and const background
norm = ROOT.RooRealVar("norm", "normalization", 1.5, 0.01, 50.)
print("norm: ")
norm.Print()

#add bkg + sig for the full model
fitmodel = ROOT.RooAddPdf("fit","full fit", sig, bkg, norm) 
#fitmodel = sig #bkg
print("fitmodel: ")
fitmodel.Print()

#make 'dataset' out of the data.
#Mmmee = ROOT.RooRealVar("Mmmee", "m_{#mu #mu e e}", locut, hicut)
datargset = ROOT.RooArgSet(meta)
print("datargset: ")
datargset.Print()
#rooimp = ROOT.RooFit.Import(dist)
#print("rooimp: ")
#rooimp.Print()
cut = "Mmmee>%f&&Mmmee<%f"%(locut, hicut)
print("cut: " + cut)
#dataset = ROOT.RooDataSet("Mmmee","data", datargset, ROOT.RooFit.Import(dist), cut)
#deactivate all the unused branches to save memory.
dist.SetBranchStatus("*", 0)
dist.SetBranchStatus(distname, 1)
#dataset = ROOT.RooDataSet("etadata","etadata", dist, datargset) #, cut)
#dataset = ROOT.RooDataSet("eta","eta ", datargset, ROOT.RooFit.Import(dist))
#print("dataset: ")
#dataset.Print()
#dataset.Draw()
#try binning it
#binnedData = dataset.createHistogram(15) #dataset.binnedClone()
#binnedData.Print()
#binnedData.Draw("a hist")
#h = raw_input("h.")
#make the dataset only between the specified bounds
#dataset.reduce()
#dataset = ROOT.RooDataSet(dist)

#c = ROOT.TCanvas("c", "", 600, 600) 
#c.cd()
#ROOT.gStyle.SetOptStat(1)
#ROOT.gStyle.SetOptFit(1)
#overmass = ROOT.RooRealVar("Mmmee", "m_{#mu #mu e e}", locut, hicut)
#massFrame = overmass.frame()
#massFrame.Draw("hist")
#massFrame = overmass.frame()
#binnedData.plotOn(massFrame)
#
##now do the fit.
#fitresult = fitmodel.fitTo(binnedData, ROOT.RooFit.Range(locut, hicut), ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Save()) 
##print the fit result
#fitresult.Print()
#fitmodel.paramOn(massFrame)
#fitmodel.plotOn(massFrame, ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.LineStyle(ROOT.kDashed))
#massFrame.Draw()
#
#c.SaveAs("Mmmeefit.png")
#h = raw_input("h.")
ngood = 0
for i,e in enumerate(dist):
    if e.Mmmee < .4 or e.Mmmee > .7:
        continue
    print(e.Mmmee)
    ngood += 1

print("\n\n %d values printed.")
f.Close()
