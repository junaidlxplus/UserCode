import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.register('runOnData', False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Run this on real data"
                 )
options.register('useRawLeptons', False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Do not correct electrons/muons with smearing/energy scales"
                 )
options.register('era', 'era2017',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "era to use (configurations defined in python/EraConfig.py)"
                 )
options.register('outFilename', 'MiniEvents.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Output file name"
                 )
options.register('baseJetCollection','slimmedJets',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Base jet collection"
                 )
options.register('inputFile', None,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "input file to process"
                 )
options.register('lumiJson', None,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 'apply this lumi json file'
                 )
options.register('saveTree', True,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "save summary tree"
                 )
options.register('savePF', False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 'save PF candidates'
                 )
options.parseArguments()

#get the configuration to apply
from TopLJets2015.TopAnalysis.EraConfig import getEraConfiguration
globalTag, jecTag, jecDB = getEraConfiguration(era=options.era,isData=options.runOnData)

process = cms.Process("MiniAnalysis")

# Load the standard set of configuration modules
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

# global tag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, globalTag)

process.load("GeneratorInterface.RivetInterface.mergedGenParticles_cfi")
process.load("GeneratorInterface.RivetInterface.genParticles2HepMC_cfi")
process.genParticles2HepMC.genParticles = cms.InputTag("mergedGenParticles")
process.load("GeneratorInterface.RivetInterface.particleLevel_cfi") 


#message logger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = ''
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
dataFormat = DataFormat.MiniAOD

switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V1_cff']

#add them to the VID producer
for idmod in my_id_modules:
      setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

# set input to process
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0000EFA3-9EF3-E711-AAB6-02163E01A5AC.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0021B93F-59F3-E711-9B8D-14DDA924324B.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0029B3B8-1FF3-E711-9773-B499BAAC09C8.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/005EBC23-34F4-E711-8C7B-7CD30AD09B20.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/00AE6D54-50F6-E711-BDE6-0025905B8592.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/00B8FD7E-25F3-E711-9544-02163E01A64C.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/022E0751-A5F2-E711-AB2F-FA163E846A8C.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/023E56A6-4FF3-E711-867C-68B59972C49E.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/02590E39-DFF3-E711-A692-4C79BA3201C3.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0269C180-84F3-E711-BA9B-0242AC1C0500.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/029B3C96-7CF2-E711-AB1B-02163E01A7A4.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/029E935C-7AF2-E711-8C40-02163E01A557.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/042AA2CB-8CF7-E711-9637-A0369FC5B7E0.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0456E629-D8F1-E711-AFA7-009C02AAB258.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/04798451-D4F3-E711-860D-0025905C3D96.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/049C5AEF-38F3-E711-B423-02163E0134FF.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/04B0A088-12F9-E711-AE1C-008CFA197A5C.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/04C516D4-6FF2-E711-BCC7-008CFAE4527C.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/04E17BC6-41F3-E711-ADB6-782BCB20E305.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0606CFA9-0CF3-E711-86BE-0026B92779FE.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/06126DF0-8FF2-E711-957D-FA163ED4FFD0.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/061A2E98-99F5-E711-AC8E-0242AC1C0500.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/063FEF8C-1FF4-E711-BD8D-3417EBE2F478.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/06589B94-C1F3-E711-9CCD-02163E01A1FE.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/06A3F464-12F2-E711-85D9-02163E0145D9.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/06C34F3D-46F2-E711-9741-FA163E2AE224.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/06F886AE-9FF2-E711-B75B-02163E019B24.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/08792EBF-09F3-E711-BF3E-008CFAE45118.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/08DFDF46-50F9-E711-A1C5-02163E01A648.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0A164C53-D7F2-E711-9ADA-0CC47A13D09C.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0A29636F-C3F2-E711-BB8F-0CC47A2B0700.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0A4025FF-B4F2-E711-8565-008CFAC91A20.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0A4B6F8F-26F6-E711-99A5-0025904C5DE2.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0A5AFF25-0DF3-E711-83C5-C4346BC00270.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0A77164B-E1F2-E711-99CA-02163E019DA5.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0C184E8B-F7F3-E711-9F72-24BE05C4F8B2.root',
                            '/store/mc/RunIIFall17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/0C274C4C-8FF2-E711-B10E-44A842CF057E.root'),
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck') 
                            )

if options.runOnData:
      process.source.fileNames = cms.untracked.vstring('/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/0AC61DCE-457E-E711-9CAE-02163E014217.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/240BA088-597E-E711-ADE4-02163E019C30.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/425DFEF6-5D7E-E711-8F2F-02163E01A1DD.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/4A64A758-627E-E711-B55A-02163E014764.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/6607066B-827E-E711-A4FF-02163E01A27A.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/6A2A982C-5D7E-E711-80E2-02163E012546.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/6CADC67B-737E-E711-93D6-02163E019C51.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/76DF8902-527E-E711-BA23-02163E0144B1.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/7C1C8736-6A7E-E711-94A9-02163E01A4AC.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/90DD97DD-E17E-E711-8F3D-02163E01A1E4.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/A045CBA8-7A7E-E711-8A9D-02163E012987.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/A8BE187C-657E-E711-BAD2-02163E01A4AE.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/CA41CDD8-547E-E711-BFE1-02163E01A377.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/CA87CF59-6D7E-E711-8450-02163E01A20B.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/DA895311-577E-E711-84E0-02163E01A1DD.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/E0CEB7C0-4D7E-E711-BEFC-02163E0138AE.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/742/00000/ECCD56AF-4B7E-E711-8DF8-02163E011F05.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/048EC98B-C97E-E711-9A39-02163E01A332.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/0AD43799-D97E-E711-A4DB-02163E011E52.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/20CE08EE-BC7E-E711-B19F-02163E01A66B.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/224E9A52-DB7E-E711-94BC-02163E01A2B9.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/34292AB2-D67E-E711-91EB-02163E013932.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/56E232CA-C17E-E711-A8D4-02163E01A377.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/609A2F31-C47E-E711-8C83-02163E014217.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/62721118-CC7E-E711-8329-02163E01391F.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/66AEDE01-CB7E-E711-BD5A-02163E01A1E4.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/7462C883-B67E-E711-9F66-02163E01A1E4.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/7C286622-B17E-E711-B065-02163E01A1E4.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/7CB07F4C-B37E-E711-96A3-02163E013932.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/8469F17B-BA7E-E711-BD23-02163E01A5C1.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/94F6A903-B57E-E711-9307-02163E01A5A5.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/B41547AE-E27E-E711-9D9D-02163E014217.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/B8406799-C67E-E711-B471-02163E01420B.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/C2C0C6BB-AB7E-E711-A4E6-02163E011EF1.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/CAC8D66C-D47F-E711-8063-02163E01420B.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/D67325CA-F47E-E711-B64D-02163E011C6E.root',
      '/store/data/Run2017C/SingleMuon/MINIAOD/PromptReco-v3/000/300/777/00000/DAC0CB43-C07E-E711-B09C-02163E01479A.root')
      #process.source.fileNames = cms.untracked.vstring('/store/data/Run2017F/SingleMuon/MINIAOD/17Nov2017-v1/50000/FEED7A3F-D3E2-E711-84DD-0025905A6134.root')

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.mergedGenParticles = cms.EDProducer("MergedGenParticleProducer",
                    inputPruned = cms.InputTag("prunedGenParticles"),
                        inputPacked = cms.InputTag("packedGenParticles"),
)
from GeneratorInterface.RivetInterface.genParticles2HepMC_cfi import genParticles2HepMC
process.genParticles2HepMC = genParticles2HepMC.clone( genParticles = cms.InputTag("mergedGenParticles") )
#process.load("TopQuarkAnalysis.TopEventProducers.producers.particleLevel_cfi")
#process.load('TopQuarkAnalysis.BFragmentationAnalyzer.bfragWgtProducer_cfi')

#apply lumi json, if passed in command line
if options.lumiJson:
    print 'Lumi sections will be selected with',options.lumiJson
    from FWCore.PythonUtilities.LumiList import LumiList
    myLumis = LumiList(filename = options.lumiJson).getCMSSWString().split(',')
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange()
    process.source.lumisToProcess.extend(myLumis)

#EGM
#from TopLJets2015.TopAnalysis.customizeEGM_cff import *
#customizeEGM(process=process,runOnData=options.runOnData)
#process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
#                                                   calibratedPatElectrons  = cms.PSet( initialSeed = cms.untracked.uint32(81),
#                                                                                      engineName = cms.untracked.string('TRandom3'),
#                                                                                     )
#                                                   )

#jet energy corrections
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
from JetMETCorrections.Configuration.DefaultJEC_cff import *
from JetMETCorrections.Configuration.JetCorrectionServices_cff import *
from TopLJets2015.TopAnalysis.customizeJetTools_cff import *
customizeJetTools(process=process,
                  jecTag=jecTag,
                  jecDB=jecDB,
                  baseJetCollection=options.baseJetCollection,
                  runOnData=options.runOnData)#False) #FIXME when residuals are available options.runOnData)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outFilename)
                                  )

process.load('TopLJets2015.TopAnalysis.miniAnalyzer_cfi')
print 'Ntuplizer configuration is as follows'
process.analysis.saveTree=cms.bool(options.saveTree)
process.analysis.savePF=cms.bool(options.savePF)
if options.useRawLeptons:
    process.selectedElectrons.src=cms.InputTag('slimmedElectrons')
    process.analysis.electrons=cms.InputTag('selectedElectrons')
    process.analysis.useRawLeptons=cms.bool(True)
    print 'Switched off corrections for leptons'
if not process.analysis.saveTree :
    print '\t Summary tree won\'t be saved'
if not process.analysis.savePF :
    print 'Summary PF info won\'t be saved'

if options.runOnData:
    process.analysis.metFilterBits = cms.InputTag("TriggerResults","","RECO")

if options.runOnData:
    process.p = cms.Path(process.analysis*process.egmGsfElectronIDSequence)
else:
    process.p = cms.Path(process.mergedGenParticles*process.genParticles2HepMC*process.particleLevel*process.egmGsfElectronIDSequence*process.analysis)

