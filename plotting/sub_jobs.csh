#!/bin/tcsh
source /cvmfs/cms.cern.ch/cmsset_default.csh
setenv SCRAM_ARCH slc6_amd64_gcc700
scramv1 project CMSSW CMSSW_10_2_16_patch1
cd CMSSW_10_2_16_patch1/src
eval `scramv1 runtime -csh`
git clone https://github.com/cms-tau-pog/TauIDSFs TauPOG/TauIDSFs
cd ${_CONDOR_SCRATCH_DIR}/CMSSW_10_2_16_patch1/src/
cp ${_CONDOR_SCRATCH_DIR}/* .
scram b -j 4
eval `scramv1 runtime -csh`
echo "Starting year $2."
#xrdfs cms-xrd-global.cern.ch locate /store/user/asahasra/DoubleElectron_Pt-1To300-gun/ScoutingSkim220329_DoubleElectronGunRun3Summer21_asahasra/220330_092202/0000/outputScoutingPF_$num.root
#python plotDistributions.py -c data_$2.csv -y $2 -con -nn condortest -n 10000
#use below if you want to start from not 0 with the csv files
#@ x = ($3 + 2)
#use below for normal usage
@ x = ($3)
#echo $x
#echo data_$2_$x.csv
python plotDistributions.py -c data_$2_$3.csv -y $2 -con 
echo "Done with year $2."
