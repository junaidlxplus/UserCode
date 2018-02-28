from WMCore.Configuration import Configuration
import os
config = Configuration()

config.section_("General")
config.General.requestName = "Data13TeV_SingleMuon_2017F_PromptReco-v1"
config.General.workArea = "my_grid"
config.General.transferOutputs=True
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = "Analysis"
config.JobType.psetName = "/afs/cern.ch/user/q/qhassan/workQhassan/top2017/CMSSW_9_4_0/src/TopLJets2015/TopAnalysis/test/runMiniAnalyzer_cfg.py"
config.JobType.disableAutomaticOutputCollection = False
config.JobType.pyCfgParams = ['runOnData=True']
config.JobType.inputFiles = ['jec_DATA.db']

config.section_("Data")
config.Data.inputDataset = "/SingleMuon/Run2017F-PromptReco-v1/MINIAOD"
config.Data.inputDBS = "global"
config.Data.splitting = "LumiBased"
config.Data.unitsPerJob = 10
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
config.Data.runRange = '305040-306462' 
config.Data.publication = True
config.Data.ignoreLocality = False
#config.Data.outLFNDirBase = 'None/6c5beb6/'

config.section_("Site")
config.Site.storageSite = "T2_IT_Legnaro"
