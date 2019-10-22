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
isMC = False
isMINIAOD = True
process = cms.Process("TagAndProbe", eras.Run2_2018)  # Marina
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')


options = VarParsing.VarParsing ('analysis')
#options.register ('secondaryFilesList','',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "List of secondary input files")

options.register ('skipEvents',
        -1,                                            # Defaul  = -1
        VarParsing.VarParsing.multiplicity.singleton,  # Options = [singleton, list]
        VarParsing.VarParsing.varType.int,             # Options = [string, int, float]
        "Number of events to skip")
options.register ('JSONfile',
        "",                                            # Default = -1
        VarParsing.VarParsing.multiplicity.singleton,  # Options = [singleton, list]
        VarParsing.VarParsing.varType.string,          # Options = [string, int, float]
        "JSON file (empty for no JSON)")
options.outputFile = 'NTuple.root'
options.inputFiles = []
options.maxEvents  = 500
options.parseArguments()




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
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff',
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_cff',
    ]


# Add them to the VID producer                                                                                                                                                                                     
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

#========================================
# START ELECTRON CUT BASED ID SECTION
#========================================
# Set up everything that is needed to compute electron IDs and
# add the ValueMaps with ID decisions into the event data stream
# Load tools and function definitions
#from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

#process.load("RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi")


#**********************
#dataFormat = DataFormat.AOD
#if isMINIAOD:
#    dataFormat = DataFormat.MiniAOD
#switchOnVIDElectronIdProducer(process, dataFormat)
#**********************

#process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
## overwrite a default parameter: for miniAOD, the collection name is a slimmed one
#if isMINIAOD:
#    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('slimmedElectrons')
#
#from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
#process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)

# Marina
# Define which IDs we want to produce
# Each of these two example IDs contains all four standard 
#my_id_modules =[
#######'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
#######'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
#'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                 # recommended for both 50 and 25 ns
########'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns, triggering still to come
########'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',    # 25 ns trig
########'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',    # 50 ns trig
#'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',   #Spring16
#'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',   #Spring16 HZZ
#'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',     # Fall17
#]


#Add them to the VID producer
#for idmod in my_id_modules:
#    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)


#egmMod = 'egmGsfElectronIDs'
#mvaMod = 'electronMVAValueMapProducer'
#regMod = 'electronRegressionValueMapProducer'
#egmSeq = 'egmGsfElectronIDSequence'
#setattr(process,egmMod,process.egmGsfElectronIDs.clone())
#setattr(process,mvaMod,process.electronMVAValueMapProducer.clone())
#setattr(process,regMod,process.electronRegressionValueMapProducer.clone())
#setattr(process,egmSeq,cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod)))
#process.electrons = cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod))

#process.load('EGTagAndProbe.EGTagAndProbe.triggerProducer_cfi')

import FWCore.Utilities.FileUtils as FileUtils
#listSecondaryFiles = FileUtils.loadListFromFile (options.secondaryFilesList)

# Marina
if not isMC: # will use 80X
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = '102X_dataRun2_Prompt_v4'

#Martin's addition (not necessary for me)

    #process.GlobalTag.toGet = cms.VPSet(
     #       cms.PSet(record = cms.string("EcalTPGLinearizationConstRcd"),
      #          tag = cms.string("EcalTPGLinearizationConst_IOV_280026_beginning_at_1"),
       #         connect =cms.string('sqlite_file:/home/llr/cms/novoa/PedestalCond/EcalTPG_280026_moved_to_1_Ped_161310.db')),
        #    cms.PSet(record = cms.string("EcalTPGPedestalsRcd"),
         #       tag = cms.string("EcalTPGPedestals_280026_beginning_at_1"),
          #      connect =cms.string('sqlite_file:/home/llr/cms/novoa/PedestalCond/EcalTPG_280026_moved_to_1_Ped_161310.db')))

    # Marina
    process.load('EGTagAndProbe.EGTagAndProbe.tagAndProbe_cff')
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
            '/store/data/Run2018D/EGamma/MINIAOD/PromptReco-v2/000/325/172/00000/DDCDF0D5-6217-3948-B73B-E812BCCEBAF1.root',
            ),
                                secondaryFileNames = cms.untracked.vstring(
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/24CBAFE6-3FA1-6E43-AB6E-6CD135928C89.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/DF2255BF-FD87-314D-B1E1-2833CCDA2710.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/2C891235-BE75-A54B-94DB-ABDCE766AEC5.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/447406C9-B5C7-C840-83FA-DAC632209105.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/1E2C3BE1-876F-A64D-A5EC-374244F12D7B.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/7C23F17B-89B7-B541-8680-80EA6173DA7F.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/003134B4-F570-0848-85F2-C1AE302D3591.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/091F0666-7D0A-D843-B4EA-AFEDDC9309B6.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/7F4658A2-54F7-4A4E-B59F-59DB70B1DBC5.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/E024A5DA-BD1D-AB46-A8FF-7A05BCDCDD1E.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/DFE754C6-28D0-9040-AE5A-184072684983.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/B8C60C09-8091-9E44-9E1A-F848181C24DD.root',
            '/store/data/Run2018D/EGamma/RAW/v1/000/325/172/00000/E2179434-951B-E746-8730-8C67D5F6E369.root',
            ),
                                )
    #process.source.eventsToProcess = cms.untracked.VEventRange('281613:108:12854629')
    #process.source.eventsToProcess = cms.untracked.VEventRange('274199:353:670607108')

########################################## Addition for Ntuples ###################################### 
if isMINIAOD:
       process.Ntuplizer.electrons = cms.InputTag("slimmedElectrons")
       process.Ntuplizer.genParticles = cms.InputTag("prunedGenParticles")
       process.Ntuplizer.Vertices = cms.InputTag("offlineSlimmedPrimaryVertices")      
      # process.Ntuplizer.triggerSet = cms.InputTag("slimmedPatTrigger","","RECO")
######################################################################################################

else:
    process.GlobalTag.globaltag = '102X_mcRun2_asymptotic_v3'
    process.load('EGTagAndProbe.EGTagAndProbe.MCanalysis_cff')
    process.source = cms.Source("PoolSource",
            fileNames = cms.untracked.vstring(
                '/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/50000/1A13CB76-9B67-E611-A143-0050560210EC.root'
                ),
            )

process.schedule = cms.Schedule()

## L1 emulation stuff

if not isMC:
    from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW 
    process = L1TReEmulFromRAW(process)
else:
    from L1Trigger.Configuration.customiseReEmul import L1TReEmulMCFromRAW
    process = L1TReEmulMCFromRAW(process) 
    from L1Trigger.Configuration.customiseUtils import L1TTurnOffUnpackStage2GtGmtAndCalo 
    process = L1TTurnOffUnpackStage2GtGmtAndCalo(process)

# Marina
process.load("L1Trigger.L1TCalorimeter.caloParams_2018_v1_3_cfi")

#### handling of cms line options for tier3 submission
#### the following are dummy defaults, so that one can normally use the config changing file list by hand etc.



if options.JSONfile:
    print "Using JSON: " , options.JSONfile
    process.source.lumisToProcess = LumiList.LumiList(filename = options.JSONfile).getVLuminosityBlockRange()

if options.inputFiles:
    process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(-1)
        )

if options.maxEvents >= -1:
    process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if options.skipEvents >= 0:
    process.source.skipEvents = cms.untracked.uint32(options.skipEvents)

process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(True)
        )

 
process.p = cms.Path (
    #process.electrons +
    process.egmGsfElectronIDSequence +
    process.RawToDigi +
    process.L1TReEmul +
    process.NtupleSeq #+
    #process.patTriggerSeq        
    )


'''
## Pantelis
process.p = cms.Path(process.electrons)
print("after process.electrons")
process.p = cms.Path(process.RawToDigi)
print("after process.RawToDigi")
process.p = cms.Path(process.L1TReEmul)
print("after process.L1TReEmul")
process.p = cms.Path(process.NtupleSeq)
print("after process.NtupleSeq")
'''


process.schedule = cms.Schedule(process.p) # do my sequence pls

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))
