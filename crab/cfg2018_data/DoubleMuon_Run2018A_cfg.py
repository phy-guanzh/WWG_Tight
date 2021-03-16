from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = 'DoubleMuon_Run2018A_2018'
config.General.transferLogs= True
config.General.workArea = 'crab2018'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = '../WWG_selector/WWG_crab_script.sh'
config.JobType.inputFiles = ['../scripts/haddnano.py','../WWG_selector/WWG_postproc.py','../WWG_selector/WWG_Module.py','../WWG_selector/branches/WWG_keep_and_drop_2018.txt','../WWG_selector/branches/WWG_outbranch_data_2018.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.scriptArgs = ['kind=data','mode=crab','year=2018','which_data=DoubleMuon']
config.JobType.sendPythonFolder  = True

config.section_("Data")
config.Data.inputDataset = '/DoubleMuon/Run2018A-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'

config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.allowNonValidInputDataset = True
config.Data.outputDatasetTag = 'DoubleMuon_Run2018A_2018'

config.section_("Site")
config.Site.storageSite = "T3_CH_CERNBOX"
config.Site.whitelist = ['T2_US_MIT','T2_US_Wisconsin','T2_US_Purdue','T2_US_UCSD','T2_US_Florida','T2_US_Caltech','T2_US_Nebraska']

