#!/usr/bin/evn python 

#########################
#Author: Sam Higginbotham
'''

* File Name : addPUhisto.py

* Purpose :

* Creation Date : 17-04-2020

* Last Modified :

'''
#########################
import ROOT
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f","--inFileName",default='MC_2016.root',help="File to be analyzed.")
parser.add_argument("-ch","--histo",default='ZHToTauTau',help="histo to be copied.")
parser.add_argument("-n","--new",nargs='+',help="all new histograms to be added")
args=parser.parse_args()

infile = ROOT.TFile.Open(args.inFileName,"UPDATE")
infile.cd()
old = infile.Get("hW_"+args.histo)
oldmc = infile.Get("hMC_"+args.histo)

newhistolist = args.new

for newhisto in newhistolist: 
    tmp = old.Clone()
    tmp.SetName("hW_"+newhisto)
    print "new histo entries ",tmp.GetEntries()
    tmp.Write(tmp.GetName(),ROOT.TObject.kOverwrite)
    tmp2 = oldmc.Clone()
    tmp2.SetName("hMC_"+newhisto)
    tmp2.Write(tmp2.GetName(),ROOT.TObject.kOverwrite)
