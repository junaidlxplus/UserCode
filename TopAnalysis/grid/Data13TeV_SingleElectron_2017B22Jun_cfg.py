from WMCore.Configuration import Configuration
import os
config = Configuration()

config.section_("General")
config.General.requestName = "Data13TeV_SingleElectron_2017B22Jun"
config.General.workArea = "grid"
config.General.transferOutputs=True

config.section_("JobType")
config.JobType.pluginName = "Analysis"
config.JobType.psetName = "/afs/cern.ch/work/q/qhassan/top2017/CMSSW_9_4_0/src/TopLJets2015/TopAnalysis/test/runMiniAnalyzer_cfg.py"
config.JobType.disableAutomaticOutputCollection = False
config.JobType.pyCfgParams = ['runOnData=True','era=era2017']
config.JobType.inputFiles = ['jec_DATA.db']

config.section_("Data")
config.Data.inputDataset = "/SingleElectron/Run2017B-22Jun2017-v1/MINIAOD"
config.Data.inputDBS = "global"
config.Data.splitting = "LumiBased"
config.Data.unitsPerJob = 100
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
config.Data.ignoreLocality = False
config.Data.publication = False
config.Data.outLFNDirBase = "/store/group/cmst3/group/top/psilva/997546d/"

config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"
