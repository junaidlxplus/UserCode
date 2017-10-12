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
options.register('era', 'era2016',
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
options.register('savePF', True,
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
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff']
                 

#add them to the VID producer
for idmod in my_id_modules:
      setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

# set input to process
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('/store/mc/PhaseISpring17MiniAOD/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/0260246D-3129-E711-8B3A-001E67DDD0AA.root'
                                                              #'/store/mc/PhaseISpring17MiniAOD/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/02781287-E22A-E711-8EF8-A0000420FE80.root',
                                                              #'/store/mc/PhaseISpring17MiniAOD/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/0405C65F-3229-E711-9FEE-70106F4A469C.root'),
                            
                            #fileNames = cms.untracked.vstring('/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/36CDAE89-B3BE-E611-B022-0025905B8604.root'
                                                              ),
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck') 
                            )

if options.runOnData:
      process.source.fileNames = cms.untracked.vstring('/store/data/Run2017A/SingleMuon/MINIAOD/PromptReco-v2/000/296/168/00000/084C505D-784C-E711-8140-02163E019DA4.root',
      '/store/data/Run2017A/SingleMuon/MINIAOD/PromptReco-v2/000/296/172/00000/66D29210-674C-E711-AFD2-02163E01A270.root',
      '/store/data/Run2017A/SingleMuon/MINIAOD/PromptReco-v2/000/296/173/00000/4C85F093-654C-E711-99AA-02163E01A203.root')
                                  
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.mergedGenParticles = cms.EDProducer("MergedGenParticleProducer",
                    inputPruned = cms.InputTag("prunedGenParticles"),
                        inputPacked = cms.InputTag("packedGenParticles"),
)
from GeneratorInterface.RivetInterface.genParticles2HepMC_cfi import genParticles2HepMC
process.genParticles2HepMC = genParticles2HepMC.clone( genParticles = cms.InputTag("mergedGenParticles") )
#process.load("TopQuarkAnalysis.TopEventProducers.producers.particleLevel_cfi")
#process.load('TopQuarkAnalysis.BFragmentationAnalyzer.bfragWgtProducer_cfi')

#EGM
#from TopLJets2015.TopAnalysis.customizeEGM_cff import *
#customizeEGM(process=process,runOnData=options.runOnData)
#process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
#                                                   calibratedPatElectrons  = cms.PSet( initialSeed = cms.untracked.uint32(81),
#                                                                                      engineName = cms.untracked.string('TRandom3'),
#                                                                                     )
#                                                   )

'''process.source = cms.Source("EmptySource")
process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    nEvents = cms.untracked.uint32(options.nevents),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    numberOfParameters = cms.uint32(1),
    args = cms.vstring('/eos/user/m/mseidel/ReReco2016/b312177_merged/TT_hdamp_TuneT4_noweights_NNPDF30_13TeV_powheg_hvq.tgz')
)
'''
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('histo.root')
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
    process.p = cms.Path(process.analysis)
else:
    process.p = cms.Path(process.mergedGenParticles*process.genParticles2HepMC*process.particleLevel*process.egmGsfElectronIDSequence*process.analysis)

