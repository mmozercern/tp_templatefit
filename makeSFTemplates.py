#!/usr/bin/env python

from os import system,mkdir,getenv,path,getcwd
from sys import argv,exit
import argparse

basedir = "/afs/cern.ch/work/m/mmozer/DEEP/tp/"
#basedir = getenv('PANDA_FLATDIR')
figsdir = basedir+'Sid/figs'

parser = argparse.ArgumentParser(description='plot stuff')
parser.add_argument('--indir',metavar='indir',type=str,default=basedir)
parser.add_argument('--outdir',metavar='outdir',type=str,default=figsdir)
parser.add_argument('--disc',metavar='disc',type=str,default='top_ecfv8_bdt')
parser.add_argument('--tagged',metavar='tagged',type=str,default='True')
parser.add_argument('--sel',metavar='sel',type=str,default='tag')
parser.add_argument('--cut',metavar='cut',type=float,default=0.5)
parser.add_argument('--pt',metavar='pt',type=str,default='inc')
parser.add_argument('--shower',metavar='shower',type=str,default='pythia')
parser.add_argument('--massvar',metavar='massvar',type=str,default='efnl1_ak8mass')
parser.add_argument('--binning',metavar='binning',type=str,default='50,350,30')
parser.add_argument('--matching',metavar='matching',type=str,default='POG')
parser.add_argument('--syst',metavar='syst',type=str,default='none')
args = parser.parse_args()

figsdir = args.outdir+'/'+args.massvar+'/'+args.matching+'/'+args.disc+'_'+str(args.cut)+'/'+args.pt
if not path.isdir(path.join(getcwd())+figsdir):
  system('mkdir -p '+figsdir)
basedir = args.indir
argv=[]

binnr = int(args.binning.split(',')[2])
binlow = float(args.binning.split(',')[0])
binhigh = float(args.binning.split(',')[1])

#print binnr,binlow,binhigh

import ROOT as root
root.gROOT.SetBatch(True)

from PandaCore.Tools.Load import *
from PandaCore.Tools.Misc import *
tcut = root.TCut
Load('PlotUtility')

### SET GLOBAL VARIABLES ###
lumi = 35.900
logy=False
nlo = 'sf_ewkV*sf_qcdV'
if args.sel=='mistag':
  cut = 'nFatjet==1 && fj1Pt>250 && fj1MaxCSV<0.46 && nLooseLep==1 && nTightMuon==1 && nLooseElectron==0 && nLoosePhoton==0 && nTau==0 && UWmag>250 && isojetNBtags==0'
  weight = '%f*normalizedWeight*sf_pu*sf_lep*%s*sf_sjbtag0*sf_btag0*sf_tt*sf_metTrig'%(lumi,nlo)
  label = 'mistag_'
elif args.sel=='photon':
  cut = 'nFatjet==1 && fj1Pt>250 && nLooseLep==0 && nLoosePhoton==1 && loosePho1IsTight==1 && nTau==0 && UAmag>250'
  weight = '%f*normalizedWeight*sf_pu*sf_lep*%s*sf_tt*sf_phoTrig*0.93'%(lumi,nlo)
  label = 'photon_'
else:
  #cut = ' efnl1_ak8pt > 250 && nvetolep<2 && passtriglepOR>0 && passmetfilters>0 && efnl1_leptonicwpt>250 '
  cut = ' fj_pt > 250 && nvetolep<2 && passtriglepOR>0 && passmetfilters>0 && ptlepmet>250 '
  if '_w' in args.disc:
    cut = ' fj_pt > 200 && nvetolep<2 && passtriglepOR>0 && passmetfilters>0 && ptlepmet>250 '
  weight = '%f*weight*truePUWeight*btagWeight*topptWeight'%(lumi)
  label = 'tag_'

disclabels = {
    'fj1Tau32SD':'#tau_{32}^{SD}',
    'top_ecfv6_bdt':'ECF BDT',
    'top_ecfv7_bdt':'ECF+#tau_{32}^{SD} BDT',
    'top_ecfv8_bdt':'ECF+#tau_{32}^{SD}+f_{rec} BDT',
    'top_ecf_bdt':'ECF+#tau_{32}^{SD}+f_{rec} BDT',
    'fj_nn_top':"Deep AK8 (top)",
    'fj_nn_w':"Deep AK8 (W)",
    'fj_decorr_nn_top':"Deep AK8 decor (top)",
    'fj_decorr_nn_w':"Deep AK8 decor (W)",
    }

label += args.disc+'_'
if args.tagged.upper()=='TRUE':
  label += 'pass_'
  if 'Tau' in args.disc:
    cut = tAND(cut,'%s<%f'%(args.disc,args.cut))
    plotlabel = '%s<%.2f'%(disclabels[args.disc],args.cut)
  else:
    cut = tAND(cut,'%s>%f'%(args.disc,args.cut))
    plotlabel = '%s>%.2f'%(disclabels[args.disc],args.cut)
else:
  label += 'fail_'
  if 'Tau' in args.disc:
    cut = tAND(cut,'%s>%f'%(args.disc,args.cut))
    plotlabel = '%s>%.2f'%(disclabels[args.disc],args.cut)
  else:
    cut = tAND(cut,'%s<%f'%(args.disc,args.cut))
    plotlabel = '%s<%.2f'%(disclabels[args.disc],args.cut)

if args.syst!='none':
  label += args.syst+'_'

if args.pt=='' or args.pt=='inc':
  cut = tAND(cut,'fj_pt>250 && fj_pt<1000')
  plotlabel = '#splitline{%s}{250 < p_{T} < 1000 GeV}'%plotlabel
elif args.pt=='lo':
  cut = tAND(cut,'efnl1_ak8pt>250 && efnl1_ak8pt<475')
  plotlabel = '#splitline{%s}{250 < p_{T} < 475 GeV}'%plotlabel
elif args.pt=='med':
  cut = tAND(cut,'efnl1_ak8pt>475 && efnl1_ak8pt<600')
  plotlabel = '#splitline{%s}{475 < p_{T} < 600 GeV}'%plotlabel
elif args.pt=='hi':
  cut = tAND(cut,'efnl1_ak8pt>600 && efnl1_ak8pt<1000')
  plotlabel = '#splitline{%s}{600 < p_{T} < 1000 GeV}'%plotlabel
elif args.pt=='inch':
  cut = tAND(cut,'efnl1_ak8pt>400 && efnl1_ak8pt<1000')
  plotlabel = '#splitline{%s}{400 < p_{T} < 1000 GeV}'%plotlabel
elif args.pt=='paperinct':
  cut = tAND(cut,'fj_pt>300 && fj_pt<1200')
  plotlabel = '#splitline{%s}{300 < p_{T} < 1200 GeV}'%plotlabel
elif args.pt=='t1':
  cut = tAND(cut,'fj_pt>300 && fj_pt<400')
  plotlabel = '#splitline{%s}{300 < p_{T} < 400 GeV}'%plotlabel
elif args.pt=='t2':
  cut = tAND(cut,'fj_pt>400 && fj_pt<480')
  plotlabel = '#splitline{%s}{400 < p_{T} < 480 GeV}'%plotlabel
elif args.pt=='t3':
  cut = tAND(cut,'fj_pt>480 && fj_pt<600')
  plotlabel = '#splitline{%s}{480 < p_{T} < 600 GeV}'%plotlabel
elif args.pt=='t4':
  cut = tAND(cut,'fj_pt>600 && fj_pt<1200')
  plotlabel = '#splitline{%s}{600 < p_{T} < 1200 GeV}'%plotlabel
elif args.pt=='paperincw':
  cut = tAND(cut,'fj_pt>200 && fj_pt<800')
  plotlabel = '#splitline{%s}{200 < p_{T} < 800 GeV}'%plotlabel
elif args.pt=='w1':
  cut = tAND(cut,'fj_pt>200 && fj_pt<300')
  plotlabel = '#splitline{%s}{200 < p_{T} < 300 GeV}'%plotlabel
elif args.pt=='w2':
  cut = tAND(cut,'fj_pt>300 && fj_pt<400')
  plotlabel = '#splitline{%s}{300 < p_{T} < 400 GeV}'%plotlabel
elif args.pt=='w3':
  cut = tAND(cut,'fj_pt>400 && fj_pt<800')
  plotlabel = '#splitline{%s}{400 < p_{T} < 800 GeV}'%plotlabel

### LOAD PLOTTING UTILITY ###
plot = root.PlotUtility()
plot.Ratio(True) 
plot.SetTDRStyle()
plot.Stack(True)
plot.InitLegend()
plot.SetCut(tcut(cut))
plot.FixRatio(.5)
plot.SetLumi(lumi/1000)
plot.DrawMCErrors(True)
plot.SetNormFactor(False)
plot.AddCMSLabel()
plot.AddLumiLabel()
if plotlabel:
  plot.AddPlotLabel(plotlabel,.18,.77,False,42,.04)
plot.SetMCWeight(weight)


### DEFINE PROCESSES ###
prong1     = root.Process('1-prong',root.kExtra2); 
prong2     = root.Process('2-prong',root.kExtra1); 
prong3     = root.Process('3-prong',root.kTTbar);  
if args.matching=='POG':
  prong1.additionalCut = root.TCut("(!(efnl1_ak8drgenwq<0.8) && !(efnl1_ak8drgent<0.6 && efnl1_gendrqtop<0.6))"); prong1.Init("Events");
  prong2.additionalCut = root.TCut("(efnl1_ak8drgenwq<0.8 && !(efnl1_ak8drgent<0.6 && efnl1_gendrqtop<0.6))");prong2.Init("Events");
  prong3.additionalCut = root.TCut("(efnl1_ak8drgent<0.6 && efnl1_gendrqtop<0.6)");prong3.Init("Events");
if args.matching=='TREE':
  prong1.additionalCut = root.TCut("(fj_no_match)"); prong1.Init("Events");
  prong2.additionalCut = root.TCut("(fj_w_match)");prong2.Init("Events");
  prong3.additionalCut = root.TCut("(fj_top_match)");prong3.Init("Events");
if args.matching=='POG8':
  prong1.additionalCut = root.TCut("(!(efnl1_ak8drgenwq<0.8) && !(efnl1_ak8drgent<0.8 && efnl1_gendrqtop<0.8))"); prong1.Init("Events");
  prong2.additionalCut = root.TCut("(efnl1_ak8drgenwq<0.8 && !(efnl1_ak8drgent<0.8 && efnl1_gendrqtop<0.8))");prong2.Init("Events");
  prong3.additionalCut = root.TCut("(efnl1_ak8drgent<0.8 && efnl1_gendrqtop<0.8)");prong3.Init("Events");
if args.matching=='HYBRID':
  prong1.additionalCut = root.TCut("(!(efnl1_ak8drgentb>0.8 && efnl1_ak8drgenwq<0.8) && !(efnl1_ak8drgent<0.6 && efnl1_gendrqtop<0.6))"); prong1.Init("Events");
  prong2.additionalCut = root.TCut("((efnl1_ak8drgentb>0.8 && efnl1_ak8drgenwq<0.8) && !(efnl1_ak8drgent<0.6 && efnl1_gendrqtop<0.6))");prong2.Init("Events");
  prong3.additionalCut = root.TCut("(efnl1_ak8drgent<0.6 && efnl1_gendrqtop<0.6)");prong3.Init("Events");
if args.matching=='HYBRID8':
  prong1.additionalCut = root.TCut("(!(efnl1_ak8drgentb>0.8 && efnl1_ak8drgenwq<0.8) && !(efnl1_ak8drgent<0.8 && efnl1_gendrqtop<0.8))"); prong1.Init("Events");
  prong2.additionalCut = root.TCut("((efnl1_ak8drgentb>0.8 && efnl1_ak8drgenwq<0.8) && !(efnl1_ak8drgent<0.8 && efnl1_gendrqtop<0.8))");prong2.Init("Events");
  prong3.additionalCut = root.TCut("(efnl1_ak8drgent<0.8 && efnl1_gendrqtop<0.8)");prong3.Init("Events");
if args.matching=='MATCH':
  prong1.additionalCut = root.TCut("(!(efnl1_ak8drgentb>0.8 && efnl1_ak8drgenwq<0.8) && !(efnl1_ak8drgent<0.6 && efnl1_ak8drgentq<0.8))"); prong1.Init("Events");
  prong2.additionalCut = root.TCut("((efnl1_ak8drgentb>0.8 && efnl1_ak8drgenwq<0.8) && !(efnl1_ak8drgent<0.6 && efnl1_ak8drgentq<0.8))");prong2.Init("Events");
  prong3.additionalCut = root.TCut("(efnl1_ak8drgent<0.6 && efnl1_ak8drgentq<0.8)");prong3.Init("Events");
if args.matching=='NEW':
  prong1.additionalCut = root.TCut("(!(efnl1_ak8drgentb>0.8 && efnl1_ak8drgenwq<0.8) && !(efnl1_ak8drgentq<0.8))"); prong1.Init("Events");
  prong2.additionalCut = root.TCut("(efnl1_ak8drgentb>0.8 && efnl1_ak8drgenwq<0.8)");prong2.Init("Events");
  prong3.additionalCut = root.TCut("(efnl1_ak8drgentq<0.8)");prong3.Init("Events");
  

photon     = root.Process('#gamma+jets',root.kGjets)
qcd        = root.Process('QCD',root.kQCD)
#prong1     = root.Process('wjets',root.kWjets) 
data       = root.Process('Data',root.kData);data.Init("Events")
if args.sel=='photon':
  data.additionalCut = root.TCut('(trigger&4)!=0')
  processes = [photon,qcd,data]
else:
  #data.additionalCut = root.TCut('(trigger&1)!=0')
  processes = [prong1,prong2,prong3,data]

### ASSIGN FILES TO PROCESSES ###
if args.sel=='photon':
  data.AddFile(basedir+'SinglePhoton.root')
  photon.AddFile(basedir+'GJets.root')
  qcd.AddFile(basedir+'QCD.root')
else:
  data.AddFile(basedir+'singlemu_tree.root') 
  data.AddFile(basedir+'met_tree.root') 
  if args.shower.upper()=='HERWIG':
    prong1.AddFile(basedir+'prong1.root')
    prong2.AddFile(basedir+'prong2_Herwig.root')
    prong3.AddFile(basedir+'prong3_Herwig.root')
    label += 'herwig_'
    print label
  else:
    if args.syst!='none' and args.syst!='herwig':
      basedir=basedir.replace('lep','lep_'+args.syst)
    print basedir
    prong1.AddFile(basedir+'qcd_tree.root')
    prong2.AddFile(basedir+'qcd_tree.root')
    prong3.AddFile(basedir+'qcd_tree.root')
    prong1.AddFile(basedir+'singletop_tree.root')
    prong2.AddFile(basedir+'singletop_tree.root')
    prong3.AddFile(basedir+'singletop_tree.root')
    prong1.AddFile(basedir+'ttV_tree.root')
    prong2.AddFile(basedir+'ttV_tree.root')
    prong3.AddFile(basedir+'ttV_tree.root')
    if args.syst!='herwig':
      prong1.AddFile(basedir+'ttbar_tree.root')
      prong2.AddFile(basedir+'ttbar_tree.root')
      prong3.AddFile(basedir+'ttbar_tree.root')
    else:
      ttbd=basedir.replace('lep','lep_syst')
      prong1.AddFile(ttbd+'ttbar-powheg-herwigpp_tree.root')
      prong2.AddFile(ttbd+'ttbar-powheg-herwigpp_tree.root')
      prong3.AddFile(ttbd+'ttbar-powheg-herwigpp_tree.root')     
    prong1.AddFile(basedir+'wjets-nlo_tree.root')
    prong2.AddFile(basedir+'wjets-nlo_tree.root')
    prong3.AddFile(basedir+'wjets-nlo_tree.root')
    prong1.AddFile(basedir+'ww_tree.root')
    prong2.AddFile(basedir+'ww_tree.root')
    prong3.AddFile(basedir+'ww_tree.root')
    prong1.AddFile(basedir+'wz_tree.root')
    prong2.AddFile(basedir+'wz_tree.root')
    prong3.AddFile(basedir+'wz_tree.root')
    prong1.AddFile(basedir+'zz_tree.root')
    prong2.AddFile(basedir+'zz_tree.root')
    prong3.AddFile(basedir+'zz_tree.root')

#processes = [prong1,data]
for p in processes:
  plot.AddProcess(p)

if args.syst=='none':
  for weightnum in xrange(109):
    plot.AddSyst("systweights[%d]"%(weightnum),"systweights[%d]"%(weightnum), "systweights[%d]"%(weightnum))
  


plot.AddDistribution(root.Distribution(args.massvar,binlow,binhigh,binnr,'M_jet [GeV]','Events/%f GeV'%((binhigh-binlow)/binnr)))

### DRAW AND CATALOGUE ###
plot.DrawAll(figsdir+'/'+label)
