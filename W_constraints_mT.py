import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "wjets"


def addTopErrors(TopScales,targetmc,newName,crName,_fOut,CRs,nCR,cid,doBtag=True):

  if doBtag:
    uncerts = ['btag','mistag']
    for uncert in uncerts:
      CRs[nCR].add_nuisance_shape(uncert,_fOut)

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin    = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName  = "WJets" # Give a name of the process being modelled
  metname      = "mT"    # Observable variable name 
  targetmc     = _fin.Get("signal_wjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("singlemuonw_wjets")  # defines in / out acceptance
  controlmc_fail    = _fin.Get("singlemuonw_fail_wjets")  # defines in / out acceptance
  controlmc_e  = _fin.Get("singleelectronw_wjets")  # defines in / out acceptance
  controlmc_e_fail  = _fin.Get("singleelectronw_fail_wjets")  # defines in / out acceptance
  controlmc_ttbar_fail    = _fin.Get("singlemuontop_fail_wjets")  # defines in / out acceptance
  controlmc_ttbar_e_fail    = _fin.Get("singleelectrontop_fail_wjets")  # defines in / out acceptance

  # btag systs
  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  
  WScales = targetmc.Clone(); WScales.SetName("wmn_weights_%s"%cid)
  WScales.Divide(controlmc);  _fOut.WriteTObject(WScales)  

  WScales_e = targetmc.Clone(); WScales_e.SetName("wen_weights_%s"%cid)
  WScales_e.Divide(controlmc_e);  _fOut.WriteTObject(WScales_e)  

  WScales_fail = targetmc.Clone(); WScales_fail.SetName("wmn_fail_weights_%s"%cid)
  WScales_fail.Divide(controlmc_fail);  _fOut.WriteTObject(WScales_fail)  


  WScales_e_fail = targetmc.Clone(); WScales_e_fail.SetName("wen_fail_weights_%s"%cid)
  WScales_e_fail.Divide(controlmc_e_fail);  _fOut.WriteTObject(WScales_e_fail)  
  
  
  WScales_ttbar_fail = targetmc.Clone(); WScales_ttbar_fail.SetName("wtopmn_fail_weights_%s"%cid)
  WScales_ttbar_fail.Divide(controlmc_ttbar_fail); _fOut.WriteTObject(WScales_ttbar_fail);

  WScales_ttbar_e_fail = targetmc.Clone(); WScales_ttbar_e_fail.SetName("wtopen_fail_weights_%s"%cid)
  WScales_ttbar_e_fail.Divide(controlmc_ttbar_e_fail); _fOut.WriteTObject(WScales_ttbar_e_fail);

  
  for uncert in ['btag','mistag']:
    WScales_ttbar_failUp = _fin.Get("signal_wjets_%sUp"%(uncert)); WScales_ttbar_failUp.SetName("wtopmn_fail_weights_%s_%s_Up"%(cid,uncert))
    controlmc_ttbar_failUp = _fin.Get("singlemuontop_fail_wjets_%sUp" %(uncert))
    WScales_ttbar_failUp.Divide(controlmc_ttbar_failUp); _fOut.WriteTObject(WScales_ttbar_failUp);

    WScales_ttbar_e_failUp = _fin.Get("signal_wjets_%sUp"%(uncert)); WScales_ttbar_e_failUp.SetName("wtopen_fail_weights_%s_%s_Up"%(cid,uncert))
    controlmc_ttbar_e_failUp = _fin.Get("singleelectrontop_fail_wjets_%sUp" %(uncert))
    WScales_ttbar_e_failUp.Divide(controlmc_ttbar_e_failUp); _fOut.WriteTObject(WScales_ttbar_e_failUp);

    WScales_ttbar_failDown = _fin.Get("signal_wjets_%sDown"%(uncert)); WScales_ttbar_failDown.SetName("wtopmn_fail_weights_%s_%s_Down"%(cid,uncert))
    controlmc_ttbar_failDown = _fin.Get("singlemuontop_fail_wjets_%sDown" %(uncert))
    WScales_ttbar_failDown.Divide(controlmc_ttbar_failDown); _fOut.WriteTObject(WScales_ttbar_failDown);

    WScales_ttbar_e_failDown = _fin.Get("signal_wjets_%sDown"%(uncert)); WScales_ttbar_e_failDown.SetName("wtopen_fail_weights_%s_%s_Down"%(cid,uncert))
    controlmc_ttbar_e_failDown = _fin.Get("singleelectrontop_fail_wjets_%sDown" %(uncert))
    WScales_ttbar_e_failDown.Divide(controlmc_ttbar_e_failDown); _fOut.WriteTObject(WScales_ttbar_e_failDown);



  ### met trig ###

  ftrig = r.TFile.Open('files/unc/fixtrig_monoh.root')
  h_trig_down = ftrig.Get('trig_sys_down')
  h_trig_up = ftrig.Get('trig_sys_up')




  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  #   (name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("singlemuonwModel",_wspace,out_ws,cid+'_'+model,WScales),
   Channel("singleelectronwModel",_wspace,out_ws,cid+'_'+model,WScales_e),
   Channel("singlemuonwfailModel",_wspace,out_ws,cid+'_'+model,WScales_fail),
   Channel("singleelectronwfailModel",_wspace,out_ws,cid+'_'+model,WScales_e_fail),
   Channel("singlemuontopwfailModel",_wspace,out_ws,cid+'_'+model,WScales_ttbar_fail),
   Channel("singleelectrontopwfailModel",_wspace,out_ws,cid+'_'+model,WScales_ttbar_e_fail),
  ]


  addTopErrors(WScales_ttbar_fail,    targetmc,"topmn", "singlemuontopwfailModel",     _fOut,CRs,4,cid)
  addTopErrors(WScales_ttbar_e_fail,  targetmc,"topen", "singleelectrontopwfailModel", _fOut,CRs,5,cid)


  #for c in CRs:
  #  c.add_nuisance_shape('mettrig',_fOut)

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  def addStatErrs(hx,cr,crname1,crname2):
    for b in range(1,targetmc.GetNbinsX()+1):
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

  addStatErrs(WScales,CRs[0],'wmn','singlemuonwModel')
  addStatErrs(WScales_e,CRs[1],'wen','singleelectronwModel')
  addStatErrs(WScales_fail,CRs[2],'wmn_fail','singlemuonwfailModel')
  addStatErrs(WScales_e_fail,CRs[3],'wen_fail','singleelectronwfailModel')
  addStatErrs(WScales_ttbar_fail,CRs[4],'wtopmn_fail','singlemuontopwfailModel')
  addStatErrs(WScales_ttbar_e_fail,CRs[5],'wtopen_fail','singleelectrontopwfailModel')




  #double_b_uncs = [
  #  0.0604635961354,
  #  0.0719763711095,
  #  0.091203905642,
  #  0.0752378106117
  #  ]

  double_b_uncs = [
    0.0,
    0.02,
    0.04,
    0.08
    ]


  WScale_doubleb_failUp = WScales_fail.Clone()
  WScale_doubleb_failDown = WScales_fail.Clone()
  WScale_e_doubleb_failUp = WScales_e_fail.Clone()
  WScale_e_doubleb_failDown = WScales_e_fail.Clone()
  WScale_ttbar_doubleb_failUp = WScales_ttbar_fail.Clone()
  WScale_ttbar_doubleb_failDown = WScales_ttbar_fail.Clone()
  WScale_ttbar_e_doubleb_failUp = WScales_ttbar_e_fail.Clone()
  WScale_ttbar_e_doubleb_failDown = WScales_ttbar_e_fail.Clone()

  for i in range(1,WScales_fail.GetNbinsX()+1):
    val_fail = WScales_fail.GetBinContent(i)
    val_e_fail = WScales_e_fail.GetBinContent(i)
    val_ttbar_fail = WScales_ttbar_fail.GetBinContent(i)
    val_ttbar_e_fail = WScales_ttbar_e_fail.GetBinContent(i)

    WScale_doubleb_failUp.SetBinContent(i,val_fail*(1+0.02))
    WScale_doubleb_failDown.SetBinContent(i,val_fail*(1-0.02))
    WScale_e_doubleb_failUp.SetBinContent(i,val_e_fail*(1+0.02))
    WScale_e_doubleb_failDown.SetBinContent(i,val_e_fail*(1-0.02))
    WScale_ttbar_doubleb_failUp.SetBinContent(i,val_ttbar_fail*(1+0.02))
    WScale_ttbar_doubleb_failDown.SetBinContent(i,val_ttbar_fail*(1-0.02))
    WScale_ttbar_e_doubleb_failUp.SetBinContent(i,val_ttbar_e_fail*(1+0.02))
    WScale_ttbar_e_doubleb_failDown.SetBinContent(i,val_ttbar_e_fail*(1-0.02))

  WScale_doubleb_failUp.SetName('%s_weights_%s_%s_doubleb_wjets_Up'%("wmn_fail",cid,cid))
  WScale_doubleb_failDown.SetName('%s_weights_%s_%s_doubleb_wjets_Down'%("wmn_fail",cid,cid))

  WScale_e_doubleb_failUp.SetName('%s_weights_%s_%s_doubleb_wjets_Up'%("wen_fail",cid,cid))
  WScale_e_doubleb_failDown.SetName('%s_weights_%s_%s_doubleb_wjets_Down'%("wen_fail",cid,cid))

  WScale_ttbar_doubleb_failUp.SetName('%s_weights_%s_%s_doubleb_wjets_Up'%("wtopmn_fail",cid,cid))
  WScale_ttbar_doubleb_failDown.SetName('%s_weights_%s_%s_doubleb_wjets_Down'%("wtopmn_fail",cid,cid))

  WScale_ttbar_e_doubleb_failUp.SetName('%s_weights_%s_%s_doubleb_wjets_Up'%("wtopen_fail",cid,cid))
  WScale_ttbar_e_doubleb_failDown.SetName('%s_weights_%s_%s_doubleb_wjets_Down'%("wtopen_fail",cid,cid))

  _fOut.WriteTObject(WScale_doubleb_failUp)
  _fOut.WriteTObject(WScale_doubleb_failDown)
  _fOut.WriteTObject(WScale_e_doubleb_failUp)
  _fOut.WriteTObject(WScale_e_doubleb_failDown)
  _fOut.WriteTObject(WScale_ttbar_doubleb_failUp)
  _fOut.WriteTObject(WScale_ttbar_doubleb_failDown)
  _fOut.WriteTObject(WScale_ttbar_e_doubleb_failUp)
  _fOut.WriteTObject(WScale_ttbar_e_doubleb_failDown)

  CRs[2].add_nuisance_shape('%s_doubleb_wjets'%(cid),_fOut)
  CRs[3].add_nuisance_shape('%s_doubleb_wjets'%(cid),_fOut)
  CRs[4].add_nuisance_shape('%s_doubleb_wjets'%(cid),_fOut)
  CRs[5].add_nuisance_shape('%s_doubleb_wjets'%(cid),_fOut)


  # # Statistical uncertainties too!, one per bin 
  # for b in range(targetmc.GetNbinsX()):
  #   err = WScales.GetBinError(b+1)
  #   if not WScales.GetBinContent(b+1)>0: continue 
  #   relerr = err/WScales.GetBinContent(b+1)
  #   if relerr<0.001: continue
  #   byb_u = WScales.Clone(); byb_u.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singlemuonwModel",b))
  #   byb_u.SetBinContent(b+1,WScales.GetBinContent(b+1)+err)
  #   byb_d = WScales.Clone(); byb_d.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singlemuonwModel",b))
  #   byb_d.SetBinContent(b+1,WScales.GetBinContent(b+1)-err)
  #   _fOut.WriteTObject(byb_u)
  #   _fOut.WriteTObject(byb_d)
  #   print "Adding an error -- ", byb_u.GetName(),err
  #   CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singlemuonwModel",b),_fOut)

  # # Statistical uncertainties too!, one per bin 
  # for b in range(targetmc.GetNbinsX()):
  #   err_e = WScales_e.GetBinError(b+1)
  #   if not WScales_e.GetBinContent(b+1)>0: continue 
  #   relerr_e = err_e/WScales_e.GetBinContent(b+1)
  #   if relerr_e<0.001: continue
  #   byb_u_e = WScales_e.Clone(); byb_u_e.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singleelectronwModel",b))
  #   byb_u_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)+err_e)
  #   byb_d_e = WScales_e.Clone(); byb_d_e.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singleelectronwModel",b))
  #   byb_d_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)-err_e)
  #   _fOut.WriteTObject(byb_u_e)
  #   _fOut.WriteTObject(byb_d_e)
  #   print "Adding an error -- ", byb_u_e.GetName(),err_e
  #   CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singleelectronwModel",b),_fOut)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  # cat.setDependant("zjets","wzModel")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat

