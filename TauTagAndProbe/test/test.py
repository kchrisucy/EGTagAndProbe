import FWCore.ParameterSet.Config as cms
process = cms.Process("TagAndProbe")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff") 

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/082EC2A0-4C28-E611-BC61-02163E014412.root',
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/1014078C-4C28-E611-85FB-02163E0141C1.root',
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/203E5176-4C28-E611-B4F8-02163E014743.root',
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/32508866-4C28-E611-A38D-02163E011BAF.root',
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/44AF1068-4C28-E611-80D0-02163E01367B.root',
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/5AF4B08A-4C28-E611-AEC9-02163E01342C.root',
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/6E3FD070-4C28-E611-9A1E-02163E011DC7.root',
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/7005DB70-4C28-E611-8628-02163E0144DD.root',
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/7C2CB76B-4C28-E611-8D90-02163E01467F.root',
        # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/86B68469-4C28-E611-92A6-02163E01419C.root',
        '/store/mc/RunIIFall15MiniAODv2/GluGluToRadionToHHTo2B2Tau_M-700_narrow_13TeV-madgraph/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/60000/2CD9692A-9EB8-E511-A944-FACADE0000C9.root'
    )
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

# import TauTagAndProbe.TauTagAndProbe.tagAndProbe_cff as TAndP
process.load('TauTagAndProbe.TauTagAndProbe.tagAndProbe_cff')
process.p = cms.Path(
    process.TAndPseq
)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string('NTuple.root'))
