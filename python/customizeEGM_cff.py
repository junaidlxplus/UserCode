import FWCore.ParameterSet.Config as cms
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
from RecoEgamma.EgammaTools.egammaObjectModificationsInMiniAOD_cff import egamma_modifications
from RecoEgamma.EgammaTools.egammaObjectModifications_tools import makeVIDBitsModifier,makeVIDinPATIDsModifier,makeEnergyScaleAndSmearingSysModifier                                     
# EGM corrections
# scale regression https://twiki.cern.ch/twiki/bin/view/CMS/EGMRegression
# smearer https://twiki.cern.ch/twiki/bin/view/CMS/EGMSmearer
def customizeEGM(process,runOnData):

    # turn on VID producer, indicate data format  to be
    # DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
    dataFormat = DataFormat.MiniAOD
    switchOnVIDElectronIdProducer(process, dataFormat)
    switchOnVIDPhotonIdProducer(process, dataFormat)

    # define which IDs we want to produce
    ele_id_modules =  [ 'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V1_cff',
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V1_cff', 
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff'
                        ]
    pho_id_modules =  [ 'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V1_TrueVtx_cff',
                        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V1_cff', 
                        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V1p1_cff'
                        ]

    #add them to the VID producer
    for idmod in ele_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
    for idmod in pho_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)

    process.load('EgammaAnalysis.ElectronTools.calibratedPatElectronsRun2_cfi')
    process.load('EgammaAnalysis.ElectronTools.calibratedPatPhotonsRun2_cfi')
    process.calibratedPatElectrons.electrons = cms.InputTag('slimmedElectrons',processName=cms.InputTag.skipCurrentProcess())
    process.calibratedPatPhotons.photons = cms.InputTag('slimmedPhotons',processName=cms.InputTag.skipCurrentProcess())
    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('calibratedPatElectrons')
    process.egmPhotonIDs.physicsObjectSrc = cms.InputTag('calibratedPatPhotons')
    process.electronMVAValueMapProducer.srcMiniAOD = cms.InputTag('calibratedPatElectrons') 
    process.photonMVAValueMapProducer.srcMiniAOD = cms.InputTag('calibratedPatPhotons')
    process.photonIDValueMapProducer.srcMiniAOD = cms.InputTag('calibratedPatPhotons')
    process.egmPhotonIsolation.srcToIsolate = cms.InputTag('calibratedPatPhotons')
    if hasattr(process,'heepIDVarValueMaps'):
        process.heepIDVarValueMaps.elesMiniAOD = cms.InputTag('calibratedPatElectrons')


    egamma_modifications.append(makeVIDBitsModifier(process,"egmGsfElectronIDs","egmPhotonIDs"))
    egamma_modifications.append(makeVIDinPATIDsModifier(process,"egmGsfElectronIDs","egmPhotonIDs"))
    egamma_modifications.append(makeEnergyScaleAndSmearingSysModifier("calibratedPatElectrons","calibratedPatPhotons"))
    for pset in egamma_modifications:
        pset.overrideExistingValues = cms.bool(True)
        if hasattr(pset,"electron_config"): pset.electron_config.electronSrc = cms.InputTag("calibratedPatElectrons")
        if hasattr(pset,"photon_config"): pset.photon_config.photonSrc = cms.InputTag("calibratedPatPhotons")

    process.slimmedElectrons = cms.EDProducer("ModifiedElectronProducer",
                                              src=cms.InputTag("calibratedPatElectrons"),
                                              modifierConfig = cms.PSet( modifications = egamma_modifications )
                                              )
    process.slimmedPhotons = cms.EDProducer("ModifiedPhotonProducer",
                                            src=cms.InputTag("calibratedPatPhotons"),
                                            modifierConfig = cms.PSet( modifications = cms.VPSet(egamma_modifications) )
                                            )
                                           

    #create the task and sequences
    process.egammaScaleSmearTask = cms.Task(process.calibratedPatElectrons,process.slimmedElectrons,
                                            process.calibratedPatPhotons,process.slimmedPhotons)
    process.egammaScaleSmearSeq = cms.Sequence( process.egammaScaleSmearTask)
    process.egammaScaleSmearAndVIDSeq = cms.Sequence(process.egammaScaleSmearSeq*
                                                     process.egmGsfElectronIDSequence*
                                                     process.egmPhotonIDSequence)
