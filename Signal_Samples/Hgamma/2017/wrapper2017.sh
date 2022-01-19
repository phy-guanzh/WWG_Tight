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
export SCRAM_ARCH=slc7_amd64_gcc630
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/righthg/${1}_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz . || exit_on_error $? 150 "Could not download sandbox1."
tar -avxf ${1}_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz
#xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/righthg/hgc_NLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz . || exit_on_error $? 150 "Could not download sandbox1."
#tar -avxf hgc_NLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz
 
seed_time=$(($RANDOM %10000 +1))
./runcmsgrid.sh 100 $seed_time 4 


xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/hgc/JHUGen_test_slc7_amd64_gcc820_CMSSW_10_6_20.tgz . || exit_on_error $? 150 "Could not download sandbox1."
tar -vxf JHUGen_test_slc7_amd64_gcc820_CMSSW_10_6_20.tgz

sed -i 's?.\/cmsgrid_final.lhe?'`pwd`\/cmsgrid_final.lhe'?' -i JHUGen.input   || exit_on_error $? 150 "failed fix path"

sandbox_name1="sandbox-CMSSW_10_6_22-5837070.tar.bz2"
sandbox_name2="sandbox-CMSSW_10_6_17_patch1-3a622d7.tar.bz2"
sandbox_name4="sandbox-CMSSW_10_6_20-d684563.tar.bz2"
sandbox_name5="sandbox-CMSSW_10_6_26-984e384.tar.bz2"
sandbox_name3="sandbox-CMSSW_9_4_14_UL_patch1-f059fdf.tar.bz2"


xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/hgamma/2017pyfile/${sandbox_name1} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/hgamma/2017pyfile/${sandbox_name2} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/hgamma/2017pyfile/${sandbox_name3} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/hgamma/2017pyfile/${sandbox_name4} . || exit_on_error $? 150 "Could not download sandbox1."
xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/hgamma/2017pyfile/${sandbox_name5} . || exit_on_error $? 150 "Could not download sandbox1."

xrdcp root://eosuser.cern.ch//eos/user/z/zguan/www/WWA_gridpack/hgamma/2017pyfile/pyfile.tar.gz . || exit_on_error $? 150 "Could not download sandbox1."
tar -vxf pyfile.tar.gz
mv pyfile/* .
#cmssw_setup $sandbox_name3 || exit_on_error $? 151 "Could not unpack sandbox"
seed_time=$(($RANDOM %10000 +1))
./runcmsgrid.sh 100 $seed_time 4 



#rm -rf *.root
cmssw_setup $sandbox_name1 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun MCDBtoEDM_NONE.py || exit_on_error $? 151 "ERROR EDM"
cmssw_setup $sandbox_name1 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL17wmLHEGEN-00239_1_cfg.py || exit_on_error $? 151 "ERROR GS"

cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL17SIM-00085_1_cfg.py
#rm SMP-RunIIFall18wmLHEGS-00059_inLHE.root SMP-RunIIFall18wmLHEGS-00059.root
cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL17DIGIPremix-00085_1_cfg.py
cmssw_setup $sandbox_name3 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL17HLT-00085_1_cfg.py
cmssw_setup $sandbox_name2 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL17RECO-00085_1_cfg.py
cmssw_setup $sandbox_name4 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL17MiniAODv2-00083_1_cfg.py
cmssw_setup $sandbox_name5 || exit_on_error $? 151 "Could not unpack sandbox"
cmsRun SMP-RunIISummer20UL17NanoAODv9-00082_1_cfg.py
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
