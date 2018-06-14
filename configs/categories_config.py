# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
out_file_name = 'bbMET.root'

# can define any thing useful here which may be common to several categories, eg binning in MET 
#bins = range(200,1200,200)
bins = [200,250,300,400,500,700,1000]
#bins = [250,300,350,400,500,600,1000]
# will expect samples with sample_sys_Up/Down but will skip if not found 
#systematics=["Met","FP","btag","mistag","wjethf","zjethf","gjethf"]
systematics=['met','btag','ewkTop','ewkW','ewkZ','lep']
# Define each of the categories in a dictionary of the following form .. 
#	'name' : the category name 
#	'in_file_name' : input ntuple file for this category 
#	'cutstring': add simple cutrstring, applicable to ALL regions in this category (eg mvamet > 200)
#	'varstring': the main variable to be fit in this category (eg mvamet), must be named as the branch in the ntuples
#	'weightname': name of the weight variable 
#	'bins': binning given as a python list
#	'additionalvars': list additional variables to be histogrammed by the first stage, give as a list of lists, each list element 
#			  as ['variablename',nbins,min,max]
#	'pdfmodel': integer --> N/A  redudant for now unless we move back to parameteric fitting estimates
# 	'samples' : define tree->region/process map given as a dictionary with each entry as follows 
#		TreeName : ['region','process',isMC,isSignal] --> Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!!

#  OPTIONAL --> 'extra_cuts': additional cuts maybe specific to this control region (eg ptphoton cuts) if this key is missing, the code will not complain   
 
bbMET_1btag = {
	    'name':"bbMET_SR1"
	   #,'in_file_name':"/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_7_4_12_patch1/src/MonoX/../BaconAnalyzer/MJSelection/skim/monojet-combo-electron.root"  # Without recoil corrections
	   #,'in_file_name':"/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_7_4_12_patch1/src/MonoX/monojet-combo-electron.root_recoil"
       #,'in_file_name':"files/monotop-boosted-combo-weight.root"
#       ,'in_file_name':"files/monotop-boosted-combo-mar9.root"
       ,'in_file_name':"files/AllMETHistos.root"
	   ,"cutstring":""      #met>200 && met<1000
	   ,"varstring":["met",200,1000]
	   ,"weightname":"weight"
	   ,"bins":bins[:]
	   #,"bins":[200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000]
  	   #,"additionalvars":[['jet1pt',25,150,1000]]
	   ,"additionalvars":[]
           ,"pdfmodel":0
	   #,"extra_cuts":[["singleelectron","rmet>40"],["photon","ptpho>200"]]
	   #,"extra_cuts":[["singleelectron","rmet>40"]]
	   ,"samples":
	   	{  
		  # Signal Region
		   "SR_1b_ZJets"  	           :['SR_1b','ZJets',1,0]
          ,"SR_1b_DYJets"	           :['SR_1b','DYJets',1,0]
 		  ,"SR_1b_WJets"  	           :['SR_1b','WJets',1,0]
		  ,"SR_1b_DIBOSON"  	       :['SR_1b','DIBOSON',1,0]
		  ,"SR_1b_Top"   	           :['SR_1b','Top',1,0]
		  ,"SR_1b_STop"                :['SR_1b','STop',1,0]
		  ,"SR_1b_QCD"		     	   :['SR_1b','QCD',1,0]
		  ,"SR_1b_data_obs"	           :['SR_1b','data_obs',0,0]

		  # some signals 

      ,"bbNLO_pseudo_1b_Mchi-1_Mphi-50"		   :['signal','Mchi-1_Mphi-50',1,1]

		  # Zmumu-Control
		  ,"Zmumu_1b_DYJets"	       :['Zmumu_1b','DYJets',1,1]
		  ,"Zmumu_1b_WJets"  	       :['Zmumu_1b','WJets',1,0]
		  ,"Zmumu_1b_DIBOSON"  	       :['Zmumu_1b','DIBOSON',1,0]
		  ,"Zmumu_1b_To"               :['Zmumu_1b','Top',1,0]
		  ,"Zmumu_1b_STop"             :['Zmumu_1b','STop',1,0]
		  ,"Zmumu_1b_dataobs"	       :['Zmumu_1b','data_obs',0,0]


            # Single muon (w) control
		  ,"Wmunu_1b_DYJets"	       :['Wmunu_1b','DYJets',1,0]
		  ,"Wmunu_1b_WJets"            :['Wmunu_1b','WJets',1,1]
		  ,"Wmunu_1b_DIBOSON"          :['Wmunu_1b','DIBOSON',1,0]
		  ,"Wmunu_1b_STop"             :['Wmunu_1b','STop',1,0]
		  ,"Wmunu_1b_Top"              :['Wmunu_1b','Top',1,0]
		  ,"Wmunu_1b_QCD"	           :['Wmunu_1b','QCD',1,0]
		  ,"Wmunu_1b_data_obs"	       :['Wmunu_1b','data_obs',0,0]


		  # Di electron-Control
		  ,"Zee_1b_DYJets"	           :['Zee_1b','DYJets',1,1]
		  ,"Zee_1b_WJets"              :['Zee_1b','WJets',1,0]
		  ,"Zee_1b_DIBOSON"  	       :['Zee_1b','DIBOSON',1,0]
		  ,"Zee_1b_Top"                :['Zee_1b','Top',1,0]
		  ,"Zee_1b_STop"               :['Zee_1b','STop',1,0]
		  ,"Zee_1b_data_obs"           :['Zee_1b','data_obs',0,0]

          # Single electron (w) control
		  ,"Wenu_1b_DYJets"            :['Wenu_1b','DYJets',1,0]
		  ,"Wenu_1b_WJets"             :['Wenu_1b','WJets',1,1]
		  ,"Wenu_1b_DIBOSON"           :['Wenu_1b','DIBOSON',1,0]
		  ,"Wenu_1b_STop"              :['Wenu_1b','STop',1,0]
		  ,"Wenu_1b_Top"               :['Wenu_1b','Top',1,0]
		  ,"Wenu_1b_QCD"               :['Wenu_1b','QCD',1,0]
		  ,"Wenu_1b_data_obs"          :['Wenu_1b','data_obs',0,0]
		  
		  # Top control
		  ,"Top_1b_DIBOSON"  	       :['Top_1b','DIBOSON',1,0]
		  ,"Top_1b_Top"                :['Top_1b','Top',1,0]
		  ,"Top_1b_STop"               :['Top_1b','STop',1,0]		  
		  
		  
	   	},

}
categories = [bbMET_1btag]
