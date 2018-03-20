#include "../../../../CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/interface/RooParametricHist.h" 
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooConstVar.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooWorkspace.h"
#include "RooPlot.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TFile.h"
#include "TH1.h"
//using namespace RooFit ;

void AddRooDataHistToWorkSpace(TString histname ){
  TFile* fin = new TFile ("combined_model.root","UPDATE");
  RooWorkspace* ws_in = (RooWorkspace*) fin->Get("combinedws");
  //ws_in->Print();

  std::cout<<" file opened "<<std::endl;
  //TFile* freweighted = new TFile("original.root");
  TFile* freweighted = new TFile("Merged_ZpBarShaped.root");
  
  TString outhistname = "reweighted_" + histname;

  std::cout<<" getting histogram"<<std::endl;
  bool objExist = freweighted->GetListOfKeys()->Contains(histname);
  std::cout<<" object exist ======"<<objExist<<std::endl;
  
  if (objExist){
    TH1F* h_rew = (TH1F*) freweighted->Get(histname);
    std::cout<<" got the histogram"<<std::endl;
    h_rew->SetName(outhistname);
    std::cout<<" renamed"<<std::endl;
    
    std::cout<< " integral for "<< outhistname <<" is "<<h_rew->Integral()<<std::endl;
    //fOut->WriteTObject(h_rew);
    if( h_rew->Integral() == 0.0 ){ return;}
    
    RooRealVar x("min(999.9999,met)_monohiggs","min(999.9999,met)_monohiggs",200,1000.) ;
    
    RooDataHist dh(outhistname,outhistname,x,Import(*h_rew)) ;
    ws_in->import(dh);
    //RooHistPdf tmp_pdf(h_rew->GetName(),h_rew->GetTitle(),RooArgSet(*(ws_in->var(varstring.c_str()))),*((RooDataHist*)(ws_in->data(tmp_hist.GetName()))));
    //ws_in->import(tmp_pdf);
    ws_in->writeToFile("combined_model.root");
  }

}


void AddRooDataHist(TString mzp, TString mchi){
  //TString name = "original_signal_BarZp-"+mzp+"-"+mchi+"_signal";
  TString name = "signal_BarZp-"+mzp+"-"+mchi+"_signal";
  std::cout<<" saving "<<name<<std::endl;
  AddRooDataHistToWorkSpace(name);

  
  AddRooDataHistToWorkSpace(name+"_btagUp");
  AddRooDataHistToWorkSpace(name+"_btagDown");
  AddRooDataHistToWorkSpace(name+"_mistagUp");
  AddRooDataHistToWorkSpace(name+"_mistagDown");

}
