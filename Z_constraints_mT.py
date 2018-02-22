import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "zjets"

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname    = "mT"          # Observable variable name 

  target                = _fin.Get("signal_zjets")            # define monimal (MC) of which process this config will model


  controlmc             = _fin.Get("dimuon_zll")              # defines Zmm MC of which process will be controlled by
  controlmc_fail        = _fin.Get("dimuon_fail_zll")            # defines Zmm MC of which process will be controlled by   


  controlmc_photon      = _fin.Get("photon_gjets")            # defines Gjets MC of which process will be controlled by
  controlmc_e           = _fin.Get("dielectron_zll")          # defines Zmm MC of which process will be controlled by
  controlmc_e_fail        = _fin.Get("dielectron_fail_zll")            # defines Zmm MC of which process will be controlled by   

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = target.Clone(); ZmmScales.SetName("zmm_weights_%s"%cid)
  ZmmScales.Divide(controlmc)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 

  ZeeScales = target.Clone(); ZeeScales.SetName("zee_weights_%s"%cid)
  ZeeScales.Divide(controlmc_e)
  _fOut.WriteTObject(ZeeScales)  # always write out to the directory 

  ZmmScales_fail = target.Clone(); ZmmScales_fail.SetName("zmm_fail_weights_%s"%cid)
  ZmmScales_fail.Divide(controlmc_fail)
  _fOut.WriteTObject(ZmmScales_fail)  # always write out to the directory                                                                                                                       

  ZeeScales_fail = target.Clone(); ZeeScales_fail.SetName("zee_fail_weights_%s"%cid)
  ZeeScales_fail.Divide(controlmc_e_fail)
  _fOut.WriteTObject(ZeeScales_fail)  # always write out to the directory          

  


  
  ### met trig ###                                                                                                                                                                              
  ftrig = r.TFile.Open('files/unc/fixtrig_monoh.root')
  h_trig_down = ftrig.Get('trig_sys_down')
  h_trig_up = ftrig.Get('trig_sys_up')



  ### PHOTONS ###
  #my_function(_wspace,_fin,_fOut,cid,diag)
  #PhotonScales = _fOut.Get("photon_weights_%s"%cid)

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
  Channel("dimuonModel",_wspace,out_ws,cid+'_'+model,ZmmScales),
  Channel("dielectronModel",_wspace,out_ws,cid+'_'+model,ZeeScales),
  Channel("dimuonfailModel",_wspace,out_ws,cid+'_'+model,ZmmScales_fail),
  Channel("dielectronfailModel",_wspace,out_ws,cid+'_'+model,ZeeScales_fail),
  #Channel("photonModel",_wspace,out_ws,cid+'_'+model,PhotonScales), 
  ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  # Bin by bin nuisances to cover statistical uncertainties ...

  # define function locally for convenient access to stuff
  def addStatErrs(hx,cr,crname1,crname2):
    for b in range(1,target.GetNbinsX()+1):
      err = hx.GetBinError(b)
      if not hx.GetBinContent(b)>0:
        continue
      relerr = err/hx.GetBinContent(b)
      if relerr<0.01:
        continue
      byb_u = hx.Clone(); byb_u.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Up'%(crname1,cid,cid,crname2,b-1))
      byb_u.SetBinContent(b,hx.GetBinContent(b)+err)
      byb_d = hx.Clone(); byb_d.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Down'%(crname1,cid,cid,crname2,b-1))
      if err<hx.GetBinContent(b):
        byb_d.SetBinContent(b,hx.GetBinContent(b)-err)
      else:
        byb_d.SetBinContent(b,0)
      _fOut.WriteTObject(byb_u)
      _fOut.WriteTObject(byb_d)
      cr.add_nuisance_shape('%s_stat_error_%s_bin%d'%(cid,crname2,b-1),_fOut)


  #double_b_uncs = [
  #  0.0817371979356,
  #  0.0865396931767,
  #  0.0881842151284,
  #  0.0775698497891
  #  ]
  
  double_b_uncs = [
    0.0,
    0.02,
    0.04,
    0.08
    ]
  

  ZmmScale_doubleb_failUp = ZmmScales_fail.Clone()
  ZmmScale_doubleb_failDown = ZmmScales_fail.Clone()
  ZeeScale_doubleb_passUp = ZeeScales.Clone()
  ZeeScale_doubleb_passDown = ZeeScales.Clone()
  
  for i in range(1,ZmmScales.GetNbinsX()+1):
    val = ZmmScales.GetBinContent(i)
    val_fail = ZmmScales_fail.GetBinContent(i)

    #ZmmScale_doubleb_passUp = ZmmScales.Clone()
    #ZmmScale_doubleb_passUp.SetBinContent(i,val*(1.05+i*1/100))

    #ZmmScale_doubleb_passDown = ZmmScales.Clone()
    #ZmmScale_doubleb_passDown.SetBinContent(i,val*(0.95-i*1/100))

    #ZmmScale_doubleb_passUp.SetName('%s_weights_%s_%s_doubleb_zjets_bin%d_Up'%("zmm",cid,cid,i-1))
    #ZmmScale_doubleb_passDown.SetName('%s_weights_%s_%s_doubleb_zjets_bin%d_Down'%("zmm",cid,cid,i-1))

    ZmmScale_doubleb_failUp.SetBinContent(i,val_fail*(1+0.03))
    ZmmScale_doubleb_failDown.SetBinContent(i,val_fail*(1-0.03))

    #_fOut.WriteTObject(ZmmScale_doubleb_passUp)
    #_fOut.WriteTObject(ZmmScale_doubleb_passDown)

    val = ZeeScales.GetBinContent(i)
    val_fail = ZeeScales_fail.GetBinContent(i)

    #ZeeScale_doubleb_passUp.SetBinContent(i,val*(1.05+i*1/100))

    #ZeeScale_doubleb_passDown.SetBinContent(i,val*(0.95-i*1/100))

    #ZeeScale_doubleb_passUp.SetName('%s_weights_%s_%s_doubleb_zjets_bin%d_Up'%("zee",cid,cid,i-1))
    #ZeeScale_doubleb_passDown.SetName('%s_weights_%s_%s_doubleb_zjets_bin%d_Down'%("zee",cid,cid,i-1))

    ZeeScale_doubleb_failUp = ZeeScales_fail.Clone()
    ZeeScale_doubleb_failUp.SetBinContent(i,val_fail*(1+0.03))

    ZeeScale_doubleb_failDown = ZeeScales_fail.Clone()
    ZeeScale_doubleb_failDown.SetBinContent(i,val_fail*(1-0.03))
    
    #_fOut.WriteTObject(ZeeScale_doubleb_passUp)
    #_fOut.WriteTObject(ZeeScale_doubleb_passDown)



  ZmmScale_doubleb_failUp.SetName('%s_weights_%s_%s_doubleb_zjets_Up'%("zmm_fail",cid,cid))
  ZmmScale_doubleb_failDown.SetName('%s_weights_%s_%s_doubleb_zjets_Down'%("zmm_fail",cid,cid))

  ZeeScale_doubleb_failUp.SetName('%s_weights_%s_%s_doubleb_zjets_Up'%("zee_fail",cid,cid))
  ZeeScale_doubleb_failDown.SetName('%s_weights_%s_%s_doubleb_zjets_Down'%("zee_fail",cid,cid))
 
  _fOut.WriteTObject(ZmmScale_doubleb_failUp)
  _fOut.WriteTObject(ZmmScale_doubleb_failDown)
  _fOut.WriteTObject(ZeeScale_doubleb_failUp)
  _fOut.WriteTObject(ZeeScale_doubleb_failDown)

  CRs[2].add_nuisance_shape('%s_doubleb_zjets'%(cid),_fOut)
  CRs[3].add_nuisance_shape('%s_doubleb_zjets'%(cid),_fOut)
  
  addStatErrs(ZmmScales,CRs[0],'zmm','dimuonModelCR')
  addStatErrs(ZeeScales,CRs[1],'zee','dielectronModelCR')
  addStatErrs(ZmmScales_fail,CRs[2],'zmm_fail','dimuonfailModelCR')
  addStatErrs(ZeeScales_fail,CRs[3],'zee_fail','dielectronfailModelCR')
  #addStatErrs(ZmmScales,CRs[2],'zmm','photonModelCR')


  #######################################################################################################
  


  '''
  CRs[2].add_nuisance_shape("renscale",_fOut) 
  CRs[2].add_nuisance_shape("facscale",_fOut) 
  CRs[2].add_nuisance_shape("pdf",_fOut) 
  CRs[2].add_nuisance("PhotonEff",0.02) 
  '''
  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,target.GetName(),CRs,diag)
  # Return of course
  return cat



