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

#xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc_nlo/hgc_LO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/righthg/${1}_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz . || exit_on_error $? 150 "Could not download sandbox1."
tar -avxf ${1}_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz
 
seed_time=$(($RANDOM %10000 +1))
./runcmsgrid.sh 100 $seed_time 4 


xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/JHUGen_test_slc7_amd64_gcc820_CMSSW_10_6_20.tgz . || exit_on_error $? 150 "Could not download sandbox1."
tar -vxf JHUGen_test_slc7_amd64_gcc820_CMSSW_10_6_20.tgz

sed -i 's?.\/cmsgrid_final.lhe?'`pwd`\/cmsgrid_final.lhe'?' -i JHUGen.input   || exit_on_error $? 150 "failed fix path"

sandbox_name1="sandbox-CMSSW_10_2_16_UL-405b47c.tar.bz2"
sandbox_name2="sandbox-CMSSW_10_6_17_patch1-5f57a9b.tar.bz2"
sandbox_name3="sandbox-CMSSW_10_6_20-c207373.tar.bz2"
sandbox_name4="sandbox-CMSSW_10_6_22-5fda411.tar.bz2"
sandbox_name5="sandbox-CMSSW_10_6_26-8539d32.tar.bz2"


xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/${sandbox_name1} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/${sandbox_name2} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/${sandbox_name3} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/${sandbox_name4} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/${sandbox_name5} . || exit_on_error $? 150 "Could not download sandbox1."

xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/MCDBtoEDM_NONE.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/SMP-RunIISummer20UL18wmLHEGEN-00236_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/SMP-RunIISummer20UL18SIM-00091_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/SMP-RunIISummer20UL18DIGIPremix-00091_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/SMP-RunIISummer20UL18HLT-00091_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/SMP-RunIISummer20UL18RECO-00091_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/SMP-RunIISummer20UL18MiniAODv2-00093_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/SMP-RunIISummer20UL18NanoAODv9-00092_1_cfg.py . || exit_on_error $? 150 "Could not download sandbox1."

cmssw_setup $sandbox_name3 || exit_on_error $? 151 "Could not unpack sandbox"
seed_time=$(($RANDOM %10000 +1))
./runcmsgrid.sh 100 $seed_time 4 



#cmsrel CMSSW_10_2_18
#cd CMSSW_10_2_18/src
#cmsenv
#cd -
#pushd .
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
#popd
#sandbox_name="WWAToLNuLNuA_4f_NLO_2_slc6_amd64_gcc700_CMSSW_10_2_24_patch1_tarball.tar.xz"
#xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/emuchannel/${sandbox_name} . || exit_on_error $? 150 "Could not download sandbox1."
#sed -i "s/^.*tarball.tar.xz.*$/     args = cms.vstring(\'..\/$sandbox_name\'),/" -i SMP-RunIISummer20UL18wmLHEGEN-00236_1_cfg.py
#seed_time=$(($(date +%s) % 100 + 1))
#sed -i "s/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int(43)/process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int($seed_time)/g" -i SMP-RunIISummer20UL18wmLHEGEN-00236_1_cfg.py
#rm -rf *.root
cmssw_setup $sandbox_name4 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun MCDBtoEDM_NONE.py || exit_on_error $? 151 "ERROR EDM"
cmssw_setup $sandbox_name4 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL18wmLHEGEN-00236_1_cfg.py || exit_on_error $? 151 "ERROR GS"

cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL18SIM-00091_1_cfg.py
#rm SMP-RunIIFall18wmLHEGS-00059_inLHE.root SMP-RunIIFall18wmLHEGS-00059.root
cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL18DIGIPremix-00091_1_cfg.py
cmssw_setup $sandbox_name1 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL18HLT-00091_1_cfg.py
cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL18RECO-00091_1_cfg.py
cmssw_setup $sandbox_name3 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL18MiniAODv2-00093_1_cfg.py
cmssw_setup $sandbox_name5 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL18NanoAODv9-00092_1_cfg.py
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
