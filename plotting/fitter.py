import ROOT as rt
from abc import ABC, abstractmethod

# Declare base fitter class with interface
class fitter(ABC):
    def __init__(self):
        self.make_signal_pdf()
        self.make_bkg_pdf()
        self.make_model()

    @abstractmethod
    def make_signal_pdf(self):
        pass

    @abstractmethod
    def make_bkg_pdf(self):
        pass

    @abstractmethod
    def make_model(self):
        pass

# Derived class for fitting of the 4-mu mass spectrum
class fitter_4mu(fitter):
    def __init__(self, mass):
        self.mass = mass
        super().__init__()
    
    def make_signal_pdf(self):
        # Construct CB signal
        #self.mcb = rt.RooRealVar("mcb", "mcb", 0.549, 0.5, 0.6)
        #self.mcb = rt.RooRealVar("mcb", "mcb", 0.957, 0.9, 1.0)
        self.mcb = rt.RooRealVar("mcb", "mcb", self.mass, self.mass-.05, self.mass+.05)
        #self.acb = rt.RooRealVar("acb", "acb", -0.9, -1, -0.5)
        self.acb = rt.RooRealVar("acb", "acb", -4.5, -6, -0.5)
        #self.ncb = rt.RooRealVar("ncb", "ncb", 21, 15, 25)
        self.ncb = rt.RooRealVar("ncb", "ncb", 21, 20, 22)
        #self.scb = rt.RooRealVar("scb", "scb", 0.00575468)
        self.scb = rt.RooRealVar("scb", "scb", 0.0195, .01, .02)
        # Best-fit from MC:
        # self.mcb = rt.RooRealVar("mcb", "mcb", 0.5498)
        # self.acb = rt.RooRealVar("acb", "acb", -0.947)
        # self.ncb = rt.RooRealVar("ncb", "ncb", 21.04)
        # self.scb = rt.RooRealVar("scb", "scb", 0.0057, 0.005, 0.006)
        self.sig = rt.RooCBShape("CB", "CB", self.mass, self.mcb, self.scb, self.acb, self.ncb)
    
    def make_bkg_pdf(self):
        # Construct Chebychev polynomial bkg
        #self.a0 = rt.RooRealVar("a0", "a0", 0.987, -10, 10)
        #self.a1 = rt.RooRealVar("a1", "a1", 0.145, -10, 10)
        self.a0 = rt.RooRealVar("a0", "a0", 0.987, -1, 1)
        self.a1 = rt.RooRealVar("a1", "a1", 0.145, -1, 1)
        self.bkg = rt.RooChebychev("bkg", "bkg", self.mass, rt.RooArgList(self.a0, self.a1))
        #self.bkg = rt.RooChebychev("bkg", "bkg", self.mass, rt.RooArgList(self.a0))
        # params for old polynomial fit pol2(0) + gaus(3) + gaus(6):
        # 36.2, -148.5, 156.1, 23.2, 0.55, 0.0046, 10, 0.56, 0.001
    
    def make_model(self):
        # Construct fit
        #self.sig_frac = rt.RooRealVar("sig_frac", "sig_frac", 0.1, 0, 1)
        #self.nsig = rt.RooRealVar("nsig", "nsig", 50, 0, 100)
        self.sig_frac = rt.RooRealVar("sig_frac", "sig_frac", 0.001, 0, 1)
        self.nsig = rt.RooRealVar("nsig", "nsig", 50, 0, 1000)
        #self.nbkg = rt.RooRealVar("nbkg", "nbkg", 1000, 0, 10000)
        self.nbkg = rt.RooRealVar("nbkg", "nbkg", 1, 0, 1000000)
        self.ebkg = rt.RooExtendPdf("ebkg", "extended bkg pdf", self.bkg, self.nbkg)
        self.esig = rt.RooExtendPdf("esig", "extended sig pdf", self.sig, self.nsig)
        self.model = rt.RooAddPdf("CBplusCheb2", "CB plus Cheb2", rt.RooArgList(self.esig, self.ebkg))
        # = rt.RooAddPdf("CBplusPol", "CB plus pol2", rt.RooArgList(cb, pol2), rt.RooArgList(sig_frac))

# Derived class for fitting of the 2-mu mass spectrum by pT slice
class fitter_2mu(fitter):
    def __init__(self, mass, model='low-pt'):
        self.mass = mass
        self.model = model
        super().__init__()
    
    def make_bkg_pdf(self):
        if self.model == 'low-pt':
            return self.make_bkgLow_pdf()
        elif self.model == 'high-pt':
            return self.make_bkgHigh_pdf()
        else:
            raise NameError('Background model not known!')
    
    def make_signal_pdf(self):
        # Create two Gaussian PDFs g1(x,mean1,sigma) anf g2(x,mean2,sigma)
        self.mean = rt.RooRealVar("mean", "mean of gaussians", 0.5478)
        self.sigma1 = rt.RooRealVar("sigma1", "width of gaussians", 0.01)
        self.sigma2 = rt.RooRealVar("sigma2", "width of gaussians", 0.005)
        self.sig1 = rt.RooGaussian("sig1", "Signal component 1", self.mass, self.mean, self.sigma1)
        self.sig2 = rt.RooGaussian("sig2", "Signal component 2", self.mass, self.mean, self.sigma2)
        # Sum the signal components into a composite signal pdf
        self.sig1frac = rt.RooRealVar("sig1frac", "fraction of component 1 in signal", 0.8, 0., 1.)
        self.sig = rt.RooAddPdf("sig", "Signal", rt.RooArgList(self.sig1, self.sig2), self.sig1frac)
        # Several old attempts below:
        # nsig1 = rt.RooRealVar("nsig1", "number of component 1 in signal", 1000, 0., 10000.)
        # nsig2 = rt.RooRealVar("nsig2", "number of component 2 in signal", 1000, 0., 10000.)
        # sig = rt.RooAddPdf("sig", "Signal", rt.RooArgList(sig1, sig2), rt.RooArgList(nsig1, nsig2))
        # alpha = rt.RooRealVar("alpha", "alpha", 1, 0.5, 10)
        # n = rt.RooRealVar("n", "n", 1, 0.5, 10)
        # sig = rt.RooCBShape("sig", "Cystal Ball Function", mass, mean, sigma1, alpha, n)
        # gamma = rt.RooRealVar("gamma", "gamma", 2, -5, 5)
        # delta = rt.RooRealVar("delta", "delta", 2, -5, 5)
        # sig = rt.RooJohnson("sig", "Johnson distribution", mass, mean, sigma1, gamma, delta)
    
    def make_bkgLow_pdf(self):
        # Build Chebychev pdf for lower pT
        self.a0 = rt.RooRealVar("a0", "a0", 0.5, 0., 1.)
        self.a1 = rt.RooRealVar("a1", "a1", 0.2, 0., 1.)
        self.bkg = rt.RooChebychev("bkgLow", "Background for low-pT", self.mass, rt.RooArgSet(self.a0, self.a1))
    
    def make_bkgHigh_pdf(self):
        # Build polynomial pdf for higher pT
        self.p0 = rt.RooRealVar("p0", "p0", 5500, 1e3, 1e7)
        self.p1 = rt.RooRealVar("p1", "p1", -1000., -1e4, 0.0)
        self.bkg = rt.RooPolynomial("bkgHigh", "Background for high-pT", self.mass, rt.RooArgSet(self.p0, self.p1))
    
    def make_model(self):
        # Sum the composite signal and background into an extended pdf nsig*sig+nbkg*bkg
        self.nsig = rt.RooRealVar("nsig", "number of signal events", 1e5, 0., 1e9)
        self.nbkg = rt.RooRealVar("nbkg", "number of background events", 1e7, 0, 1e9)
        self.model = rt.RooAddPdf("model", "(g1+g2)+a", rt.RooArgList(self.bkg, self.sig), rt.RooArgList(self.nbkg, self.nsig))
