'''
Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
'''

#================================================================================================
#  Definitions
#================================================================================================
CMSSWrel = '101X'
isMC     = False 
name     = 'L1EG_Unpacked_'+CMSSWrel

if isMC:
    name+='_MC'
else:
    name+='_Data'

dirName = 'multicrab_'+name


dataset = {    
    # 101X
    'EGamma_2018A_v1' : '/EGamma/Run2018A-PromptReco-v1/MINIAOD',
    'EGamma_2018A_v2' : '/EGamma/Run2018A-PromptReco-v2/MINIAOD',
    'EGamma_2018A_v3' : '/EGamma/Run2018A-PromptReco-v3/MINIAOD',
    'EGamma_2018B_v1' : '/EGamma/Run2018B-PromptReco-v1/MINIAOD',
    'EGamma_2018B_v2' : '/EGamma/Run2018B-PromptReco-v2/MINIAOD',
    'EGamma_2018C_v1' : '/EGamma/Run2018C-PromptReco-v1/MINIAOD',
    'EGamma_2018C_v2' : '/EGamma/Run2018C-PromptReco-v2/MINIAOD',
    'EGamma_2018C_v3' : '/EGamma/Run2018C-PromptReco-v3/MINIAOD',
    
    # 102X
    #'EGamma_2018D_v1' : '/EGamma/Run2018D-PromptReco-v1/MINIAOD',
    #'EGamma_2018D_v2' : '/EGamma/Run2018D-PromptReco-v2/MINIAOD',
    }

eventsPerJob = {
    'EGamma_2018A_v1' : 30000,
    'EGamma_2018A_v2' : 30000,
    'EGamma_2018A_v3' : 30000,
    'EGamma_2018B_v1' : 30000,
    'EGamma_2018B_v2' : 30000,
    'EGamma_2018C_v1' : 30000,
    'EGamma_2018C_v2' : 30000,
    'EGamma_2018C_v3' : 30000,
    'EGamma_2018D_v1' : 30000,
    'EGamma_2018D_v2' : 30000,
    }

listOfSamples = [
    
    # 101X
    'EGamma_2018A_v1',
    'EGamma_2018A_v2',
    'EGamma_2018A_v3',
    'EGamma_2018B_v1',
    'EGamma_2018B_v2',
    'EGamma_2018C_v1',
    'EGamma_2018C_v2',
    'EGamma_2018C_v3',

    # 102X
    #'EGamma_2018D_v1',
    #'EGamma_2018D_v2',
    
    ]

if __name__ == '__main__':
    
    #============================================================================================
    #  Import Modules
    #============================================================================================
    from WMCore.Configuration import Configuration
    from CRABClient.UserUtilities import getUsernameFromSiteDB
    from CRABAPI.RawCommand import crabCommand
    from multiprocessing import Process
    
    config = Configuration()

    def submit(config):
        res = crabCommand('submit', config = config)
    
    #================================================================================================
    # General Section: The user specifies generic parameters about the request (e.g. request name).
    #================================================================================================ 
    config.section_("General")
    config.General.workArea        = dirName
    config.General.transferOutputs = True
    config.General.transferLogs    = True
    
    #================================================================================================
    # JobType Section: Contains all the parameters of the user job type and related configurables
    #================================================================================================
    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName   = 'test.py'    # Options = ['reEmulL1_new.py', 'test.py']
    
    #================================================================================================
    # Data Section: Contains all parameters related to the data to be analyzed (incl. splitting params)
    #================================================================================================
    config.section_("Data")
    config.Data.inputDBS      = 'global'
    config.Data.outLFNDirBase = '/store/user/mkolosov/CRAB3_TransferData/L1EG/Performance/Data2018/Unpacked/'
    config.Data.splitting     = 'Automatic' 
    config.Data.publication   = False
    config.Data.totalUnits    = -1
    config.Data.lumiMask      = 'Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
    # Lumi Mask taken from:  'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
    
    #================================================================================================
    # Site Section: Contains the Grid site parameters (incl. stage out information)
    #================================================================================================
    config.section_("Site")
    config.Site.storageSite = 'T3_US_FNALLPC'
    
    listOfSamples.reverse()
    
    for sample in listOfSamples:
      config.General.requestName   = sample
      config.Data.inputDataset     = dataset[sample]
      #      config.Data.useParent       = True   # Needed for L1 Emulator (or grandparent?)
      #      config.Data.unitsPerJob      = eventsPerJob[sample]
      config.Data.outputDatasetTag = sample
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()
