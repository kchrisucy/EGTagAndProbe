#=====================================
# User Imports
#=====================================
import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

#=====================================
# Options
#=====================================
isMC        = False
isMINIAOD   = True
maxEvents   = -1
reportEvery = 100
outputFile = 'NTuple.root'

if isMC:
    globaltag = '101X_mcRun2_asymptotic_v5'
    datasetFiles = [
        '/store/mc/RunIIFall18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v12_ext1-v1/60000/70E5316E-7F73-C94E-A6FC-9014BC36BDF0.root',
        '/store/mc/RunIIFall18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v12_ext1-v1/60000/70D11899-0FC2-5F4E-8E31-3586B5619B31.root',
        '/store/mc/RunIIFall18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v12_ext1-v1/60000/6ED73AA8-3C53-5A42-8E3B-EBF059924184.root',
        '/store/mc/RunIIFall18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v12_ext1-v1/60000/6DD6961E-C425-2B40-85F3-6082BB81D010.root',
        ]
else:
    globaltag = '101X_dataRun2_Prompt_v9'
    datasetFiles = [
        '/store/data/Run2018C/EGamma/MINIAOD/PromptReco-v3/000/320/344/00000/683F559A-5092-E811-8C89-FA163EAB8290.root',
        '/store/data/Run2018C/EGamma/MINIAOD/PromptReco-v3/000/320/340/00000/EA942623-4792-E811-A42A-FA163E2F62B7.root',
        '/store/data/Run2018C/EGamma/MINIAOD/PromptReco-v3/000/320/065/00000/F2D0EE4C-0490-E811-93A3-02163E019EB0.root',
        '/store/data/Run2018C/EGamma/MINIAOD/PromptReco-v3/000/320/065/00000/BA946D62-F38F-E811-BADB-02163E019FCC.root',
        '/store/data/Run2018C/EGamma/MINIAOD/PromptReco-v3/000/320/065/00000/80AE3770-F08F-E811-AFA7-FA163ECFC085.root',
        '/store/data/Run2018C/EGamma/MINIAOD/PromptReco-v3/000/320/065/00000/3EC4B55E-F68F-E811-8E76-FA163EC0210C.root',
        ]
    

# For debugging purposes
debug = True
RunNum_1    = 1
LumiBlock_1 = 2
EvtNum_1    = 240
RunNum_2    = 1
LumiBlock_2 = 2
EvtNum_2    = 260
    
#========================================================
# Setup the process
#========================================================
process = cms.Process("TagAndProbe", eras.Run2_2018)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(debug),
    # printDependencies = cms.untracked.bool(debug),
    )

process.maxEvents = cms.untracked.PSet(
    input         = cms.untracked.int32(maxEvents)
    )

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = reportEvery

#========================================================
# Define the input files
#========================================================
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(datasetFiles)
                            #eventsToProcess = cms.untracked.VEventRange('%s:%s:%s-%s:%s:%s' % (RunNum_1, LumiBlock_1, EvtNum_1, RunNum_2, LumiBlock_2, EvtNum_2) ),
                            )

#========================================================
# Output File
#========================================================
process.TFileService = cms.Service('TFileService', fileName = cms.string(outputFile))

#========================================================
# Global Tag
#========================================================
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
from Configuration.AlCa.autoCond import autoCond

process.GlobalTag.globaltag = globaltag

#===================================================
# Electron ID
#===================================================
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

dataFormat = DataFormat.MiniAOD

if isMINIAOD:
    dataFormat = DataFormat.MiniAOD
else:
    dataFormat = DataFormat.AOD

switchOnVIDElectronIdProducer(process, dataFormat)

# Define which IDs we want to produce
my_id_modules =[
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V1_cff',
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',
    #'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff',
    #'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_cff',
    ] 

# Add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

#================================================================================================
# Load processes
#================================================================================================
if not isMC:
    process.load('EGTagAndProbe.EGTagAndProbe.tagAndProbe_cff')
else:
    process.load('EGTagAndProbe.EGTagAndProbe.MCanalysis_cff')
    process.Ntuplizer.useHLTMatch = cms.bool(False) #In case no HLT object in MC sample considered or you're fed up with trying to find the right HLT collections
    
    
if isMINIAOD:
    process.Ntuplizer.electrons    = cms.InputTag("slimmedElectrons")
    process.Ntuplizer.genParticles = cms.InputTag("prunedGenParticles")
    process.Ntuplizer.Vertices     = cms.InputTag("offlineSlimmedPrimaryVertices")
    
#================================================================================================ 
# Module execution
#================================================================================================
process.p = cms.Path(
    process.egmGsfElectronIDSequence *
    process.NtupleSeq
)
