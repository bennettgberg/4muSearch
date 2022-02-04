
import os, sys

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    defDS = '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM '
    parser.add_argument("--dataSet",default=defDS,help="Data set name.") 
    parser.add_argument("-d","--dataType",default="MC",help="Data type, string: 'Data' or 'MC' (default MC).") 
    parser.add_argument("--nickName",default='MCpileup',help="Data set nick name.") 
    parser.add_argument("-m","--mode",default='anaXRD',help="Mode (script to run).")
    parser.add_argument("-y","--year",default=2017,type=str,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("--csv",default="MCsamples_2016.csv",help="CSV file for samples")
    parser.add_argument("--pileup",default="MC_2016_nAODv7.root",help="CSV file for samples")
    parser.add_argument("-c","--concatenate",default=5,type=int,help="On how many files to run on each job")
    parser.add_argument("-s","--selection",default='4mu',type=str,help="select ZH,AZH,HAA")
    parser.add_argument("-g","--genmatch",default=0,type=int,help="genmatch")
    parser.add_argument("-p","--proxypath",default="/afs/cern.ch/user/s/shigginb/private/x509up",type=str,help="Full path to proxy certificate file (for condor)")
    parser.add_argument("-l","--language",default="bash",type=str,help="Language for scripts to run (only bash or tcsh is supported for now.)")
    parser.add_argument("-myeos","--my_eos",default=0,type=int,help="input files will exist in my personal eos space (1) or won't (0)")
    parser.add_argument("-j","--doSystematics",default="false",type=str,help="doSystematics (true) or nah (false)")
    return parser.parse_args()

def beginBatchScriptTcsh(baseFileName) :
    outLines = ['#!/bin/tcsh\n']
    outLines.append("source /cvmfs/cms.cern.ch/cmsset_default.csh\n")
    #outLines.append("setenv SCRAM_ARCH slc6_amd64_gcc700\n")
    outLines.append("setenv SCRAM_ARCH slc6_amd64_gcc700\n")
#    outLines.append("eval scramv1 project CMSSW CMSSW_10_2_9\n")
    #outLines.append("cd CMSSW_10_2_16_patch1/src\n")
#    outLines.append("cd CMSSW_10_2_9/src\n")
#    outLines.append("setenv SCRAM_ARCH slc6_amd64_gcc700\n")
#    outLines.append("eval `scramv1 project CMSSW CMSSW_10_2_16_patch1`\n")
#    outLines.append("cd CMSSW_10_2_16_patch1/src\n")
    outLines.append("scramv1 project CMSSW CMSSW_10_2_16_patch1\n")
    outLines.append("cd CMSSW_10_2_16_patch1/src\n")
    outLines.append("eval `scramv1 runtime -csh`\n")
    outLines.append("git clone https://github.com/cms-tau-pog/TauIDSFs TauPOG/TauIDSFs\n")
    outLines.append("cd ${_CONDOR_SCRATCH_DIR}/CMSSW_10_2_16_patch1/src/\n")
    outLines.append("cp ${_CONDOR_SCRATCH_DIR}/* .\n")
    outLines.append("scram b -j 4\n")
    outLines.append("eval `scramv1 runtime -csh`\n")
#    outLines.append("echo ${_CONDOR_SCRATCH_DIR}\n")
#    outLines.append("cd ${_CONDOR_SCRATCH_DIR}\n")
    return outLines

def beginBatchScript(baseFileName) :
    outLines = ['#!/bin/bash\n']
#    outLines.append("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
#    outLines.append("export SCRAM_ARCH=slc6_amd64_gcc700\n")
#    outLines.append("eval scramv1 project CMSSW CMSSW_10_2_16_patch1\n")
#    outLines.append("cd CMSSW_10_2_16_patch1/src\n")
#    outLines.append("eval scramv1 runtime -sh\n")
#    outLines.append("export X509_USER_PROXY=$1\n")
#    outLines.append("voms-proxy-info -all\n")
#    outLines.append("voms-proxy-info -all -file $1\n")
#    outLines.append("echo ${_CONDOR_SCRATCH_DIR}\n")
#    outLines.append("cd ${_CONDOR_SCRATCH_DIR}\n")
    outLines.append("cd ${_CONDOR_SCRATCH_DIR}\n")
    outLines.append("export X509_USER_PROXY=$1\n")
    outLines.append("voms-proxy-info -all\n")
    outLines.append("voms-proxy-info -all -file $1\n")
    outLines.append("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
    outLines.append("export SCRAM_ARCH=slc6_amd64_gcc700\n")
    outLines.append("eval `scramv1 project CMSSW CMSSW_10_2_16_patch1`\n")
    outLines.append("cd CMSSW_10_2_16_patch1/src\n")
    outLines.append("eval `scramv1 runtime -sh`\n")
    outLines.append("git clone https://github.com/cms-tau-pog/TauIDSFs TauPOG/TauIDSFs\n")
    outLines.append("cd ${_CONDOR_SCRATCH_DIR}/CMSSW_10_2_16_patch1/src/\n")
    outLines.append("cp ${_CONDOR_SCRATCH_DIR}/* .\n")
    outLines.append("scram b -j 4\n")
    outLines.append("eval `scramv1 runtime -sh`\n")
    outLines.append("ls -altrh\n")
    return outLines

def getFileName(line) :
    tmp = line.split()[0].strip(',')
    fileName = tmp.strip()
    return fileName


args = getArgs()
era = str(args.year)
isMC = True
if args.dataType == "Data": isMC = False
# sample query 
# dasgoclient --query="file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8*/*/NANOAOD*" --limit=0   

#string to be added in some cases is 4tau is specified.
ttttstr = ""
# sample query
# dasgoclient --query="file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8*/*/NANOAOD*" --limit=0

query = '"file dataset={0:s}"'.format(args.dataSet)

if "USER" in str(args.dataSet) : query = '"file dataset={0:s}"'.format(args.dataSet+" instance=prod/phys03")

command = "dasgoclient --query={0:s} --limit=0  > fileList.txt".format(query)
print("Running in {0:s} mode.  Command={1:s}".format(args.mode,command))
os.system(command)

files = open('fileList.txt','r').readlines()
if len(files) < 1 :
    print("***In makeCondor.py: Empty fileList.txt")
    print("copying fileList from M-20.")
    os.system("cp /uscms/homes/b/bgreenbe/work/CMSSW_10_2_9/src/ZH_Run2/MC/condor/bpgtest/fileList.txt .")
    files = open("fileList.txt").readlines()
   # exit()

scriptList = []
file=[]
dataset=[]

mjobs=args.concatenate


for nFiles, file in enumerate(files) :
    fileName=getFileName(file)
    dataset.append(fileName)


counter=0

for nFile in range(0, len(dataset),mjobs) :
    #print("nFile={0:d} file[:80]={1:s}".format(nFile,file[:80]))

    #scriptName = "{0:s}_{1:03d}.csh".format(args.nickName,nFile+1)
    scriptName = "{0:s}_{1:03d}.{2:s}sh".format(args.nickName,nFile+1, "c" if not args.language == "bash" else "")
    print("scriptName={0:s}".format(scriptName))
    if args.language == "bash":
        outLines = beginBatchScript(scriptName)
    else:
        outLines = beginBatchScriptTcsh(scriptName)

    #outLines.append("tar -zxvf SFs.tar.gz\n")
    outLines.append("cp MCsamples_*csv MCsamples.csv\n")
    outLines.append("cp cuts_{0:s}.yaml cuts.yaml\n".format(args.selection))

    fileName = getFileName(file)
    maxx = mjobs
    if counter+mjobs > len(dataset) :
        #print 'should include', nFile, -nFile-mjobs + len(dataset)+1, 'from ', len(dataset), counter
        maxx = len(dataset)-counter
        #for j in range(0,mjobs) :
    for j in range(0,maxx) :
        #print 'shoud see', nFile+maxx, maxx, len(dataset)
    #bpg: changes for my_eos are somewheres around here boi
        fileloop=dataset[nFile:nFile+maxx][j]
        if not args.my_eos:
            #outLines.append("xrdcp root://cms-xrd-global.cern.ch/{0:s} inFile.root\n".format(fileloop)) 
            outLines.append("xrdcp root://cmsxrootd.fnal.gov/{0:s} inFile.root\n".format(fileloop)) #does this work?
        else:
            print("error: signal samples for 4mu not yet available.")
            sys.exit(1)
            #need to extract the filename and copy it from eos.
            #words = fileloop.split("/")
            #fname = words[len(words)-1]
            ##for now this is always signal
            #aMassString = args.nickName.split('_')[-1]
            #outLines.append("xrdcp root://cmseos.fnal.gov//store/user/bgreenbe/haa_4tau_{}/signal_{}/{} inFile.root\n".format(era, aMassString, fname))
        outFileName = "{0:s}_{1:03d}.root".format(args.nickName,nFile+j)
        #print("python HAA{}.py -f inFile.root -o {} --nickName {} --csv {} -y {} -s {} -w 1 -g {}\n".format(ttttstr, outFileName,args.nickName, args.csv, args.year, args.selection, args.genmatch))
        outLines.append("python ntupler_4mu.py -f inFile.root -o {0:s} --nickName {1:s} --csv {2:s} -y {3:s} -w 1 -g {5:d} -d {6:s} -j {7:s}\n".format(outFileName,args.nickName, args.csv, args.year, args.selection, args.genmatch, "MC" if isMC else "Data", args.doSystematics))
        #copy the file to eos.
#        outLines.append("xrdcp {0:s} root://cmseos.fnal.gov//store/user/bgreenbe/haa_4tau/{1:s}/{0:s}\n".format(outFileName, args.nickName))
        outLines.append("rm inFile.root\n")


    allname = "all_{0:s}_{1:03d}.root".format(args.nickName, nFile+1) #can use below instead of rewriting twice.
    outLines.append("hadd -f -k all_{0:s}_{1:03d}.root *ntup *weights\n".format(args.nickName,nFile+1))
    outLines.append("xrdcp -f all_{0:s}_{1:03d}.root root://cmseos.fnal.gov//store/user/bgreenbe/4mu_{2:s}/{0:s}\n".format(args.nickName, nFile+1, era))
    outLines.append("rm *.pyc\nrm *.so\nrm *.pcm\nrm *cc.d\n")
    outLines.append("rm *.ntup *.weights *.so\nrm *.pcm\nrm *cc.d\n")
#        fileloop=dataset[nFile:nFile+maxx][j]
#        outLines.append("xrdcp root://cms-xrd-global.cern.ch/{0:s} inFile.root\n".format(fileloop))
#        outFileName = "{0:s}_{1:03d}.root".format(args.nickName,nFile+j)
#        outLines.append("python HAA.py -f inFile.root -o {0:s} --nickName {1:s} -y {2:s} -j false -w 1\n".format(outFileName,args.nickName, args.year))
#        outLines.append("rm inFile.root\n")
#
#
#    outLines.append("hadd -f -k all_{0:s}_{1:03d}.root *ntup *weights\n".format(args.nickName,nFile+1))
#    outLines.append("rm *.pyc\nrm *.so\nrm *.pcm\nrm *cc.d\n")
#    outLines.append("rm *.ntup *.weights *.so\nrm *.pcm\nrm *cc.d\n")
#    outLines.append("cp  all*root ${_CONDOR_SCRATCH_DIR}/.\n")
#    outLines.append("cp  *weights* ${_CONDOR_SCRATCH_DIR}/.\n")
    print("Writing out file = {0:s}".format(scriptName))
    open(scriptName,'w').writelines(outLines)
    scriptList.append(scriptName)
    counter += mjobs

# now that .csh files have been generated make a list of corresponding .jdl files


#dir = os.getenv("CMSSW_BASE")+"/src/ZH_Run2/MC/"
thisdir = os.getenv("CMSSW_BASE")+"/src/4mu/"
SVFitDir = os.getenv("CMSSW_BASE")+"/src/ZH_Run2/SVFit/"


#dir = os.getcwd()+"/../../../../MC/"
#SVFitDir = os.getcwd()+"/../../../../SVFit/"


print("thisdir={0:s}".format(thisdir))

for file in scriptList :
    #base = file[:-4] 
    base = file[:-3] 
    if args.language != "bash":
        base = base[:-1]
    #print base,"     OR     ",file[:-3]
    outLines = ['universe = vanilla\n']
    outLines.append('Executable = {0:s}\n'.format(file))
    outLines.append('Output = {0:s}.out\n'.format(base))
    outLines.append('Error = {0:s}.err\n'.format(base))
    outLines.append('Log = {0:s}.log\n'.format(base))
#    outLines.append('Proxy_filename = x509up\n')
    #outLines.append('Proxy_path = /afs/cern.ch/user/s/shigginb/private/$(Proxy_filename)\n')
    outLines.append('Proxy_path = {}\n'.format(args.proxypath))
    print("thisdir={0:s}".format(thisdir))
    #outLines.append('transfer_input_files = {0:s}ZH.py, {0:s}MC_{1:s}.root, {0:s}data_pileup_{1:s}.root, {0:s}MCsamples_{1:s}.csv, {0:s}ScaleFactor.py, {0:s}SFs.tar.gz, {0:s}cuts_{2:s}.yaml, '.format(dir,args.year, args.selection))
    #outLines.append('transfer_input_files = {0:s}ZH.py, {0:s}MC_{1:s}.root, {0:s}data_pileup_{1:s}.root, {0:s}MCsamples_{1:s}.csv, {0:s}cuts_{2:s}.yaml, '.format(dir,args.year, args.selection))
    json_path = thisdir + "/ref/"
    if args.year == "2017":
        json_path += "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
    else:
    #put in other json paths.
        pass
    outLines.append('transfer_input_files = {0:s}code/ntupler_4mu{4:s}.py, {0:s}ref/MC_{1:s}_nAODv7.root, {0:s}ref/data_pileup_{1:s}.root, {0:s}ref/MCsamples_{1:s}_v7.csv, {0:s}code/cuts_4mu.yaml, {0:s}{3:s}, {5:s},'.format(thisdir,args.year, args.selection, args.csv, ttttstr, json_path))
    outLines.append('{0:s}code/tauFun2{1:s}.py, {0:s}code/Weights.py, {0:s}code/generalFunctions.py, {0:s}code/outTuple{1:s}.py\n'.format(thisdir, ttttstr))
#    outLines.append('Proxy_filename = x509up\n')
#    outLines.append('Proxy_path = /afs/cern.ch/user/s/shigginb/private/$(Proxy_filename)\n')
    outLines.append('should_transfer_files = YES\n')
    outLines.append('when_to_transfer_output = ON_EXIT\n')
    outLines.append('arguments = $(Proxy_path)\n')
    #outLines.append('x509userproxy = $ENV(X509_USER_PROXY)\n')
    outLines.append('request_cpus = 2\n')
    outLines.append('+JobFlavour  = "tomorrow"\n')
    outLines.append('Queue 1\n')
    open('{0:s}.jdl'.format(base),'w').writelines(outLines)
