from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = 'WW_2018'
config.General.transferLogs= True
config.General.workArea = 'crab2018'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = '../WWG_selector/WWG_crab_script.sh'
config.JobType.inputFiles = ['../scripts/haddnano.py','../WWG_selector/WWG_postproc.py','../WWG_selector/WWG_Module.py','../WWG_selector/branches/WWG_keep_and_drop_2018.txt','../WWG_selector/branches/WWG_outbranch_mc_2018.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.scriptArgs = ['kind=True','mode=crab','year=2018','which_data=MC']
config.JobType.sendPythonFolder  = True

config.section_("Data")
config.Data.inputDataset = '/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1

config.Data.outLFNDirBase ='/store/user/zguan/WWG_2018_v1/'
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True
config.Data.outputDatasetTag = 'WW_2018'

config.section_("Site")
config.Site.storageSite = "T3_CH_CERNBOX"
config.Site.whitelist = ['T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T2_US_Nebraska']

