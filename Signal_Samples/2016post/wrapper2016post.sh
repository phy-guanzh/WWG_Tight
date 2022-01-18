exit_on_error() {
    result=$1
    code=$2
    message=$3

    if [ $1 != 0 ]; then
        echo $3
        exit $2
    fi
}

#### FRAMEWORK SANDBOX SETUP ####
# Load cmssw_setup function
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/wwg/pyfile/cmssw_setup.sh . || exit_on_error $? 150 "Could not download sandbox1."
#cp /etc/ciconnect/templates/cmssw_setup.sh .
source cmssw_setup.sh

# Setup CMSSW Base
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700

xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/SMP-RunIISummer20UL16wmLHEGEN-00255_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/SMP-RunIISummer20UL16SIM-00092_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/SMP-RunIISummer20UL16DIGIPremix-00089_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/SMP-RunIISummer20UL16HLT-00092_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/SMP-RunIISummer20UL16RECO-00092_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/SMP-RunIISummer20UL16MiniAODv2-00092_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/SMP-RunIISummer20UL16NanoAODv9-00092_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
#cmsrel CMSSW_10_2_18
#cd CMSSW_10_2_18/src
#cmsenv
#cd -
# Download sandbox, replace it when you have different sandbox_name
sandbox_name1="sandbox-CMSSW_10_6_22-a9ec907.tar.bz2"  #LHEGen
sandbox_name2="sandbox-CMSSW_10_6_17_patch1-2be13ee.tar.bz2" #SIM
sandbox_name3="sandbox-CMSSW_10_6_17_patch1-2be13ee.tar.bz2" #DIGI
sandbox_name4="sandbox-CMSSW_8_0_33_UL-5f0516c.tar.bz2" #HLT
sandbox_name5="sandbox-CMSSW_10_6_17_patch1-2be13ee.tar.bz2" #RECO
sandbox_name6="sandbox-CMSSW_10_6_25-38d2c87.tar.bz2" #MINIAOD2
sandbox_name7="sandbox-CMSSW_10_6_26-552d939.tar.bz2" #NANO
# Change to your own http
#wget --no-check-certificate --progress=bar "http://stash.osgconnect.net/+zguan/Wjets/condor/${sandbox_name1}"  || exit_on_error $? 150 "Could not download sandbox1."
#wget --no-check-certificate --progress=bar "http://stash.osgconnect.net/+zguan/Wjets/condor/${sandbox_name2}"  || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/${sandbox_name1} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/${sandbox_name2} . || exit_on_error $? 150 "Could not download sandbox1."
#xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/${sandbox_name3} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/${sandbox_name4} . || exit_on_error $? 150 "Could not download sandbox1."
#xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/${sandbox_name5} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/${sandbox_name6} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/pyfile2016post/${sandbox_name7} . || exit_on_error $? 150 "Could not download sandbox1."

pushd .
# Setup framework from sandbox
#cmsrel CMSSW_10_6_14
#cd CMSSW_10_6_14/src
#eval `scramv1 runtime -sh`
#cmsenv
#git cms-init
#git cms-merge-topic kdlong:CMSSW_10_6_14_NanoGenWeights
#scramv1 b
#eval `scramv1 runtime -sh`
#tar -xf $sandbox_name4 || exit_on_error $? 151 "Could not unpack sandbox"
#cmssw_setup $sandbox_name4 || exit_on_error $? 151 "Could not unpack sandbox"
#tar -vxf ${sandbox_name4} || exit_on_error $? 151 "Could not unpack sandbox"
#cd CMSSW_10_6_14/src
#scramv1 b
#eval `scramv1 runtime -sh`
#cmsenv
#eval `scramv1 runtime -sh`
popd
sandbox_name="WWAToEMuA_4f_NLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/emuchannel/newmaster/${sandbox_name} . || exit_on_error $? 150 "Could not download sandbox1."
sed -i "s/^.*tarball.tar.xz.*$/     args = cms.vstring(\'..\/$sandbox_name\'),/" -i SMP-RunIISummer20UL16wmLHEGEN-00255_1_cfg.py
#seed_time=$(($(date +%s) % 100 + 1))
seed_time=$(($RANDOM %10000 +1))
sed -i "s/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int(43)/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int($seed_time)/g" -i SMP-RunIISummer20UL16wmLHEGEN-00255_1_cfg.py
rm -rf *.root
cmssw_setup $sandbox_name1 || exit_on_error $? 151 "Could not unpack sandbox1"
cmsRun SMP-RunIISummer20UL16wmLHEGEN-00255_1_cfg.py || exit_on_error $? 151 "ERROR GS"

cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox2"
cmsRun SMP-RunIISummer20UL16SIM-00092_1_cfg.py
#rm SMP-RunIIFall18wmLHEGS-00059_inLHE.root SMP-RunIIFall18wmLHEGS-00059.root
cmssw_setup $sandbox_name3 || exit_on_error $? 151 "Could not unpack sandbox3"
cmsRun SMP-RunIISummer20UL16DIGIPremix-00089_1_cfg.py
export SCRAM_ARCH=slc7_amd64_gcc530
cmssw_setup $sandbox_name4 || exit_on_error $? 151 "Could not unpack sandbox4"
cmsRun SMP-RunIISummer20UL16HLT-00092_1_cfg.py
export SCRAM_ARCH=slc7_amd64_gcc700
cmssw_setup $sandbox_name5 || exit_on_error $? 151 "Could not unpack sandbox5"
cmsRun SMP-RunIISummer20UL16RECO-00092_1_cfg.py
cmssw_setup $sandbox_name6 || exit_on_error $? 151 "Could not unpack sandbox6"
cmsRun SMP-RunIISummer20UL16MiniAODv2-00092_1_cfg.py
cmssw_setup $sandbox_name7 || exit_on_error $? 151 "Could not unpack sandbox7"
cmsRun SMP-RunIISummer20UL16NanoAODv9-00092_1_cfg.py
#rm -rf cmssw-tmp
# Setup framework from sandbox
#pushd .
#cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
#popd

#rm $sandbox_name
#cmsRun SMP-RunIIAutumn18DRPremix-00048_1_cfg.py
#rm SMP-RunIIFall18wmLHEGS-00059_inLHE.root SMP-RunIIFall18wmLHEGS-00059.root
#cmsRun SMP-RunIIAutumn18DRPremix-00048_2_cfg.py
#rm SMP-RunIIAutumn18DRPremix-00048_step1.root
#cmsRun SMP-RunIIAutumn18MiniAOD-00048_1_cfg.py
#rm SMP-RunIIAutumn18DRPremix-00048.root
rm -rf cmssw-tmp
# Setup framework from sandbox
#pushd .
#cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
#popd
#cmsRun SMP-RunIIAutumn18NanoAODv6-00019_1_cfg.py
#rm SMP-RunIIAutumn18MiniAOD-00048.root
# clean
#rm -rf cmssw-tmp
rm *py
rm *pyc
rm $sandbox_name4
#rm $sandbox_name2
