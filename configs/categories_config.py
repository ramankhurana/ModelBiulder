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
	   ,"cutstring":"met>200 && met<1000"
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
		   "ZnunuLO_signal"  	       :['SR','ZJets',1,0]
          ,"DY_signal"	               :['SR','DYJets',1,0]
 		  ,"WJets_signal"  	           :['SR','WJets',1,0]
		  ,"VV_signal"  	           :['SR','DIBOSON',1,0]
		  ,"Top_signal"   	           :['SR','Top',1,0]
		  ,"SingleTop_signal"          :['SR','STop',1,0]
		  ,"QCD_signal"		     	   :['SR','QCD',1,0]
		  ,"data_signal"	           :['SR','data_obs',0,0]

		  # some signals 

      ,"Mchi-1_Mphi-50_signal"		   :['signal','Mchi-1_Mphi-50',1,1]

		  # Zmumu-Control
		  ,"DY_Zmumu_control"	       :['Zmumu','DYJets',1,1]
		  ,"WJets_Zmumu_control"  	   :['Zmumu','WJets',1,0]
		  ,"Diboson_Zmumu_control"  	   :['Zmumu','DIBOSON',1,0]
		  ,"Top_Zmumu_control"         :['Zmumu','Top',1,0]
		  ,"SingleTop_Zmumu_control"     :['Zmumu','STop',1,0]
		  ,"data_Zmumu_control"	   :['Zmumu','data_obs',0,0]


            # Single muon (w) control
		  ,"DY_Wmunu_control"	   :['Wmunu','DYJets',1,0]
		  ,"WJets_Wmunu_control"     :['Wmunu','WJets',1,1]
		  ,"Diboson_Wmunu_control"        :['Wmunu','DIBOSON',1,0]
		  ,"SingleTop_Wmunu_control" :['Wmunu','STop',1,0]
		  ,"Top_Wmunu_control"     :['Wmunu','Top',1,0]
		  ,"QCD_Wmunu_control"	   :['Wmunu','QCD',1,0]
		  ,"data_Wmunu_control"	   :['Wmunu','data_obs',0,0]


		  # Di electron-Control
		  ,"DY_Zee_control"	   :['Zee','DYJets',1,1]
		  ,"WJets_Zee_control"     :['Zee','WJets',1,0]
		  ,"Diboson_Zee_control"  	   :['Zee','DIBOSON',1,0]
		  ,"Top_Zee_control"      :['Zee','Top',1,0]
		  ,"SingleTop_Zee_control"  :['Zee','STop',1,0]
		  ,"data_Zee_control"	   :['Zee','data_obs',0,0]

          # Single electron (w) control
		  ,"DY_Wenu_control"       :['Wenu','DYJets',1,0]
		  ,"WJets_Wenu_control"     :['Wenu','WJets',1,1]
		  ,"Diboson_Wenu_control"        :['Wenu','DIBOSON',1,0]
		  ,"SingleTop_Wenu_control" :['Wenu','STop',1,0]
		  ,"Top_Wenu_control"     :['Wenu','Top',1,0]
		  ,"QCD_Wenu_control"       :['Wenu','QCD',1,0]
		  ,"data_Wenu_control"      :['Wenu','data_obs',0,0]
		  
		  # Top control
		  ,"Diboson_Top_control"  	   :['Top','DIBOSON',1,0]
		  ,"Top_Top_control"      :['Top','Top',1,0]
		  ,"SingleTop_Top_control"  :['Top','STop',1,0]		  
		  
		  
	   	},

}
categories = [bbMET_1btag]
