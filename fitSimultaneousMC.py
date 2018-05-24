#!/usr/bin/env python
from os import system,mkdir,getenv,path,getcwd
import argparse
from sys import argv

#NBINS=30 

parser = argparse.ArgumentParser(description='fit stuff')
parser.add_argument('--indir',metavar='indir',type=str)
parser.add_argument('--syst',metavar='syst',type=str,default='cent')
parser.add_argument('--var',metavar='var',type=str,default='efnl1_ak8_nn_top')
parser.add_argument('--constr',metavar='constr',type=float,default=0)
parser.add_argument('--ctype',metavar='ctype',type=str,default='N')
parser.add_argument('--catvals',metavar='catvals',type=str,default='')
parser.add_argument('--caterrs',metavar='caterrs',type=str,default='')
parser.add_argument('--masstag',metavar='masstag',type=str,default='efnl1_ak8mass')
parser.add_argument('--altplot',metavar='altplot',type=bool,default=False)
parser.add_argument('--signal',metavar='signal',type=str,default='top')
args = parser.parse_args()
basedir = args.indir
argv=[]

catvals=[]
if len(args.catvals) > 0:
  catvals = [float(item) for item in args.catvals.split(',')]
print catvals

caterrs=[]
if len(args.caterrs) > 0:
  caterrs = [float(item) for item in args.caterrs.split(',')]
print caterrs

iPsig=3 
if args.signal != 'top':
  iPsig=2

from math import sqrt
import ROOT as root
root.gROOT.SetBatch(True)

from PandaCore.Tools.Load import *
Load('HistogramDrawer')

def imp(w_):
  return getattr(w_,'import')

plot_labels = {
    'jer' : 'JER smeared',
    'jes_up' : 'JES Up',
    'jes_down' : 'JES Down',
    'qscale_up' : 'Q^2 scale Up',
    'qscale_down' : 'Q^2 scale Down',
    'pdf_up' : 'PDF Up',
    'pdf_down' : 'PDF Down',
    'smearedSJ' : 'SJ JER smeared',
    'scaleSJUp' : 'SJ JES Up',
    'scaleSJDown' : 'SJ JES Down',
    'topPt' : 'No top p_{T} weight',
    'btagUp' : 'b-tag Up',
    'btagDown' : 'b-tag Down',
    'mistagUp' : 'b-mistag Up',
    'mistagDown' : 'b-mistag Down',
    'mergeUp' : 'Merging radius Up',
    'mergeDown' : 'Merging radius Down',
    'cent' : 'Nominal',
    'herwig' : 'alternative shower'
    }

plot_postfix = ''
plot_label = plot_labels[args.syst]
if args.syst!='cent':
  if args.syst=='jer':
    postfix = 'Resolution'
  elif args.syst=='jes_up':
    postfix = 'ScaleUp'
  elif args.syst=='jes_down':
    postfix = 'ScaleDown'
  elif args.syst=='smearedSJ':
    postfix = 'Smeared_sj'
  elif args.syst=='scaleSJUp':
    postfix = 'ScaleUp_sj'
  elif args.syst=='scaleSJDown':
    postfix = 'ScaleDown_sj'
  else:
    postfix = ''
  if postfix!='':
    plot_postfix = postfix
  else:
    plot_postfix = args.syst
  args.syst += '_'
else:
  postfix = ''
  if args.ctype=='N':
    plot_postfix='unconstr'
  else:
    plot_postfix=args.ctype+'_'+str(args.constr)
  args.syst = ''

plot = {}
for iC in [0,1]:
  plot[iC] = root.HistogramDrawer()
  plot[iC].Ratio(1)
  plot[iC].FixRatio(.4)
  plot[iC].DrawMCErrors(False)
  plot[iC].Stack(True)
  plot[iC].DrawEmpty(True)
  plot[iC].SetTDRStyle()
  plot[iC].AddCMSLabel()
  plot[iC].SetLumi(35.9)
  plot[iC].AddLumiLabel(True)
  plot[iC].InitLegend()

hprong = {}; dhprong = {}; pdfprong = {}; norm = {}; smeared = {}; smear = {}; mu = {}; hdata = {}; dh_data={}
mcnorms = {}; mcerrs = {}; constr={}
mass = root.RooRealVar("m","m_{SD} [GeV]",50,300)

ftemplate = {
      'pass' : root.TFile(basedir+'tag_%s_pass_%shists.root'%(args.var,args.syst)),
      'fail' : root.TFile(basedir+'tag_%s_fail_%shists.root'%(args.var,args.syst)),
    }

inputs = {
    1 : ['1-prong'],
    2 : ['2-prong'],
    3 : ['3-prong'],
    }

def build_sum_hist(cat,nprong):
  f = ftemplate[cat]
  hsum = None
  for i in inputs[nprong]:
    if not hsum:
      hsum = f.Get('h_%s_%s'%(args.masstag,i)).Clone('h_%s_%i'%(cat,nprong))
    else:
      hsum.Add(f.Get('h_%s_%s'%(args.masstag,i)))

  print "building sum for", cat
  for i in xrange(hsum.GetNbinsX()+1):
    #print hsum.GetBinContent(i)
    if hsum.GetBinContent(i)==0:
      hsum.SetBinContent(i,0.0001)
  return hsum

# get histograms
hdata[1] = ftemplate['pass'].Get('h_%s_Data'%(args.masstag))
NBINS=hdata[1].GetNbinsX()
dh_data[1] = root.RooDataHist('dh_data1','dh_data1',root.RooArgList(mass),hdata[1])
hdata[0] = ftemplate['fail'].Get('h_%s_Data'%(args.masstag))
dh_data[0] = root.RooDataHist('dh_data0','dh_data0',root.RooArgList(mass),hdata[0])

for iC in [0,1]:
  for iP in xrange(1,4):
    cat=(iP,iC)
    hprong[cat] = build_sum_hist(('pass','fail')[iC==0],iP) 


# build pdfs
for iC in [0,1]:
  for iP in xrange(1,4):
    cat = (iP,iC)
    dhprong[cat] = root.RooDataHist('dh%i%i'%cat,'dh%i%i'%cat,root.RooArgList(mass),hprong[cat]) 
    pdfprong[cat] = root.RooHistPdf('pdf%i%i'%cat,'pdf%i%i'%cat,root.RooArgSet(mass),dhprong[cat]) 
    norm_ = hprong[cat].Integral()
    norm[cat] = root.RooRealVar('norm%i%i'%cat,'norm%i%i'%cat,norm_,0.01*norm_,100*norm_)
    mcnorms[cat] = norm_
    err_ = 0
    for iB in xrange(1,hprong[cat].GetNbinsX()+1):
      err_ += pow(hprong[cat].GetBinError(iB),2)
    mcerrs[cat] = sqrt(err_)


#define category of interest
ntotal={}
for iP in xrange(1,4):
  ntotal[iP] = root.RooRealVar('n%d_total'%iP,'n%d_total'%iP,norm[(iP,0)].getVal()+norm[(iP,1)].getVal(),0.,10*(norm[(iP,0)].getVal()+norm[(iP,1)].getVal()))


constrainsums=False
if len(catvals)==3: # use command line provided totals
  constrainsums=True
  for iP in xrange(1,4):
    ntotal[iP].setVal(catvals[iP-1])


### use category of interest
eff_ = {}
for iP in xrange(1,4):
  eff_[iP] = mcnorms[(iP,1)]/(mcnorms[(iP,1)]+mcnorms[(iP,0)])

print "#######################################"
print "eff  = "+str(eff_[iPsig])+" =  "+ str( mcnorms[(iPsig,1)] ) +" / ("+ str(mcnorms[(iPsig,1)])+"+"+str(mcnorms[(iPsig,0)])+")"
print "#######################################"

eff = {}
normeff = {}
for iP in xrange(1,4):
  eff[iP] = root.RooRealVar('eff_%d'%iP,'eff_%d'%iP,eff_[iP],0.,1.)
  normeff[(iP,0)] = root.RooFormulaVar('nP%d_fail'%iP,'(1.0-eff_%d)*n%d_total'%(iP,iP),root.RooArgList(eff[iP],ntotal[iP]))
  normeff[(iP,1)] = root.RooFormulaVar('nP%d_pass'%iP,'eff_%d*n%d_total'%(iP,iP),root.RooArgList(eff[iP],ntotal[iP]))


#apply constraint  ==> rationalize
constraints = root.RooArgList("constraintlist")
if args.ctype == 'G' or args.ctype == 'L': #Gaussian and lognormal constraints applied to split pass/fail contributions
  for iP in [3,2,1]:
    if not constrainsums:
      if iP != iPsig: # skip signal category, that's still supposed to float when cosntraining the separate  pass/fail contributions
        for iC in [0,1]:
          cat = (iP,iC)
          if  args.ctype == 'L':
            constr[(iP,iC,0)]=root.RooFit.RooConst(mcnorms[cat])
            constr[(iP,iC,1)]=root.RooFit.RooConst(args.constr)
            constr[cat] = root.RooLognormal('constr_%d_%d'%cat,'constr_%d_%d'%cat,
                                            norm[cat],
                                            constr[(iP,iC,0)],
                                            constr[(iP,iC,1)])
          if  args.ctype == 'G':
            constr[(iP,iC,0)]=root.RooFit.RooConst(mcnorms[cat])
            constr[(iP,iC,1)]=root.RooFit.RooConst(mcnorms[cat]*args.constr)
            constr[cat] = root.RooGaussian('constr_%d_%d'%cat,'constr_%d_%d'%cat,
                                           norm[cat],
                                           constr[(iP,iC,0)],
                                           constr[(iP,iC,1)])
          constraints.add(constr[cat])
    else: #constrain totals with either percentage error or absolute error given on command line
      for iP in [3,2,1]:
        if args.ctype == 'L':
          constr[(iP,0)]=root.RooFit.RooConst(ntotal[iP].getVal())
          errval = args.constr
          if(len(caterrs)==3):
            errval = caterrs[iP-1]/ntotal[iP].getVal()
          constr[(iP,1)]=root.RooFit.RooConst(errval)
          constr[iP]=  root.RooLognormal('constr_%d'%iP,'constr_%d'%iP,
                                         ntotal[iP],
                                         constr[(iP,0)],
                                         constr[(iP,1)])
        if args.ctype == 'G':
          constr[(iP,0)]=root.RooFit.RooConst(ntotal[iP].getVal())
          errval = args.constr * ntotal[iP].getVal()
          if(len(caterrs)==3):
            errval = caterrs[iP-1]
          constr[(iP,1)]=root.RooFit.RooConst(errval)
          constr[iP] = root.RooGaussian('constr_%d'%iP,'constr_%d'%iP,
                                        ntotal[iP],
                                        constr[(iP,0)],
                                        constr[(iP,1)])
        constraints.add(constr[iP])



model = {}

#set up norm as flat number or total number*eff
for iC in [0,1]:
  if constrainsums:
    for iP in xrange(1,4):
      norm[(iP,iC)]=normeff[(iP,iC)]
  else:
    norm[(iPsig,iC)]=normeff[(iPsig,iC)]


#create sum pdf with appropriate norms
for iC in [0,1]:
  model[iC] = root.RooAddPdf('model%i'%iC,'model%i'%iC,
                            root.RooArgList(*[pdfprong[(x,iC)] for x in [1,2,3]]),
                            root.RooArgList(*[norm[(x,iC)] for x in [1,2,3]]))


# build simultaneous fit
sample = root.RooCategory('sample','')
sample.defineType('pass',1)
sample.defineType('fail',2)

datacomb = root.RooDataHist('datacomb','datacomb',root.RooArgList(mass),
                            root.RooFit.Index(sample),
                            root.RooFit.Import('pass',dh_data[1]),
                            root.RooFit.Import('fail',dh_data[0]))

simult = root.RooSimultaneous('simult','simult',sample)
simult.addPdf(model[1],'pass')
simult.addPdf(model[0],'fail')

#Apply constraint PDFs if necessary
constrlist = root.RooArgList(simult)
if args.ctype == 'G' or args.ctype =='L':
  for iP in [3,2,1]:
    if not constrainsums:
      if iP != iPsig:
        for iC in [0,1]:
          cat = (iP,iC)
          constrlist.add(constr[cat])
          constrlist.Print()
    else:
      constrlist.add(constr[iP])
      constrlist.Print()

  constr['test']=simult
  simult = root.RooProdPdf('datacomb_const','datacomb_const',constrlist)
    

# fit!
fitresult = simult.fitTo(datacomb,
                          root.RooFit.Extended(),
                          root.RooFit.Strategy(2),
                          root.RooFit.Minos(root.RooArgSet(eff[iPsig])),
                          root.RooFit.NumCPU(4),
                          root.RooFit.Save())

fitresult.Print("v")

# dump the efficiencies
pcat=(iPsig,1); fcat=(iPsig,0)
masslo=105; masshi =210 # to get on binedges for now
if args.signal !='top':
  masslo=65; masshi=105


effMass_ = hprong[pcat].Integral(hprong[pcat].FindBin(masslo),hprong[pcat].FindBin(masshi)-1)/hprong[pcat].Integral() # prefit efficiency of the mass cut on the pass distribution
mass.setRange('MASSWINDOW',masslo,masshi)
massint = pdfprong[pcat].createIntegral(root.RooArgSet(mass),root.RooArgSet(mass),'MASSWINDOW')
effMass = massint.getVal(); effMassErr = massint.getPropagatedError(fitresult)

# make nice plots

colors = {
  1:8,
  2:6,
  3:root.kOrange
}
labels = {
  1:'Unmatched',
  2:'Matched W',
  3:'Matched top',
}

for iC in [0,1]:
  plotlist = [1,2,3]
  if args.altplot:
    plotlist = [3]

  for iP in plotlist:
    cat = (iP,iC)
    h = pdfprong[cat].createHistogram('h%i%i'%cat,mass,root.RooFit.Binning(NBINS))
    h.SetLineWidth(3)
    h.SetLineStyle(1)
    h.SetLineColor(colors[iP])
    if h.Integral() > 1.0e-6:
      h.Scale(norm[cat].getVal()/h.Integral())
    else:
      h.Scale(0)
    plot[iC].AddAdditional(h,'hist',labels[iP])
  
  if args.altplot:
    hbkg = hprong[(1,0)].Clone('prefit')
    hbkg.Reset()
    for jP in [2,1]:
      h = pdfprong[(jP,iC)].createHistogram('h%i%i'%cat,mass,root.RooFit.Binning(NBINS))
      h.Scale(norm[(jP,iC)].getVal()/h.Integral())
      hbkg.Add(h)
    hbkg.SetLineWidth(3)
    hbkg.SetLineStyle(1)
    hbkg.SetFillStyle(0)
    hbkg.SetLineColor(root.kRed)
    plot[iC].AddAdditional(hbkg,'hist',"W- and unmatched")

  hprefit = hprong[(1,0)].Clone('prefit')
  hprefit.Reset()
  for jP in [3,2,1]:
    hprefit.Add(hprong[(jP,iC)])
  hprefit.SetLineWidth(2)
  hprefit.SetLineStyle(2)
  hprefit.SetLineColor(root.kBlue+2)
  hprefit.SetFillStyle(0)
  plot[iC].AddAdditional(hprefit,'hist','Pre-fit')

  if args.altplot:
    hprefitbkg = hprong[(1,0)].Clone('prefit')
    hprefitbkg.Reset()
    for jP in [2,1]:
      hprefitbkg.Add(hprong[(jP,iC)])
    hprefitbkg.SetLineWidth(2)
    hprefitbkg.SetLineStyle(2)
    hprefitbkg.SetLineColor(root.kRed)
    hprefitbkg.SetFillStyle(0)
    plot[iC].AddAdditional(hprefitbkg,'hist')
 
  for iP in plotlist:
    cat = (iP,iC)
    hprong[cat].SetLineColor(colors[iP])
    hprong[cat].SetFillStyle(0)
    hprong[cat].SetLineWidth(2)
    hprong[cat].SetLineStyle(2)
    plot[iC].AddAdditional(hprong[cat],'hist')

  hdata[iC].SetLineColor(root.kBlack)
  hdata[iC].SetMarkerStyle(20);
  plot[iC].AddHistogram(hdata[iC],'Data',root.kData)

  hmodel_ = model[iC].createHistogram('hmodel%i'%iC,mass,root.RooFit.Binning(NBINS))
  hmodel = root.TH1D(); hmodel_.Copy(hmodel)
  hmodel.SetLineWidth(3);
  hmodel.SetLineColor(root.kBlue+10)
  hmodel.GetXaxis().SetTitle('fatjet m_{SD} %s [GeV]'%postfix)
  hmodel.GetYaxis().SetTitle('Events/10 GeV')
  if hmodel.Integral()>1.e-6:
    hmodel.Scale(sum([norm[(x,iC)].getVal() for x in [1,2,3]])/hmodel.Integral())
  else:
     hmodel.Scale(0)
  hmodel.SetFillStyle(0)
  plot[iC].AddHistogram(hmodel,'Post-fit',root.kExtra5)
  plot[iC].AddAdditional(hmodel,'hist')


  plot[iC].AddPlotLabel('#varepsilon_{tag}^{Data} = %.4g^{+%.2g}_{-%.2g}'%(eff[iPsig].getVal(),abs(eff[iPsig].getErrorHi()),abs(eff[iPsig].getErrorLo())),
                        .65,.47,False,42,.04)
  #plot[iC].AddPlotLabel('#varepsilon_{tag}^{MC} = %.3g^{+%.2g}_{-%.2g}'%(eff_,err_,err_),
  plot[iC].AddPlotLabel('#varepsilon_{tag}^{MC} = %.4g'%(eff_[iPsig]),
                        .65,.37,False,42,.04)
  plot[iC].AddPlotLabel('#varepsilon_{tag+mSD}^{Data} = %.4g^{+%.2g}_{-%.2g}'%(effMass*eff[iPsig].getVal(),effMass*abs(eff[iPsig].getErrorHi()),effMass*abs(eff[iPsig].getErrorLo())),
                        .65,.27,False,42,.04)
  #plot[iC].AddPlotLabel('#varepsilon_{tag+mSD}^{MC} = %.3g^{+%.2g}_{-%.2g}'%(eff_*effMass_,err_*effMass_,err_*effMass_),
  plot[iC].AddPlotLabel('#varepsilon_{tag+mSD}^{MC} = %.4g'%(eff_[iPsig]*effMass_),
                        .65,.17,False,42,.04)

plot[1].AddPlotLabel('Pass category',.18,.77,False,42,.05)
plot[0].AddPlotLabel('Fail category',.18,.77,False,42,.05)
for _,p in plot.iteritems():
  p.AddPlotLabel(plot_label,.18,.7,False,42,.05)
plot_postfix = '_'+plot_postfix

if not path.isdir(path.join(getcwd())+basedir+'/fits/'):
  system('mkdir -p '+basedir+'/fits/')

plot[1].Draw(basedir,'/fits/pass%s'%plot_postfix)
plot[0].Draw(basedir,'/fits/fail%s'%plot_postfix)

# save outpuat
w = root.RooWorkspace('w','workspace')
w.imp = imp(w)
w.imp(mass)
for x in [ntotal[iPsig],eff[iPsig],sample,datacomb,simult]:
  w.imp(x)
for iC in [0,1]:
  w.imp(normeff[(iPsig,iC)])
  w.imp(dh_data[iC])
  w.imp(model[iC])
  for iP in [1,2,3]:
    cat = (iP,iC)
#    w.imp(smear[iP]); w.imp(mu[iP])
    w.imp(dhprong[cat])
    w.imp(pdfprong[cat])
    w.imp(norm[cat])
#    w.imp(pdfprong[cat])
w.writeToFile(basedir+'/fits/wspace%s.root'%plot_postfix)

#need to check!
s = []
s.append( 'Tagging cut:' )
s.append( '\tPre-fit efficiency was %f'%(eff_[iPsig]) )
s.append( '\tPost-fit efficiency is %f +%.5g -%.5g'%(eff[iPsig].getVal(),abs(eff[iPsig].getErrorHi()),abs(eff[iPsig].getErrorLo())) )
s.append( 'Tagging+mass cut:' )
s.append( '\tPre-fit mass efficiency was %f'%(effMass_) )
s.append( '\tPost-fit mass efficiency is %f +/-%.5g'%(effMass,effMassErr) )
s.append( '\tPre-fit mass+tag efficiency was %f'%(effMass_*eff_[iPsig]) )
s.append( '\tPost-fit mass+tag efficiency is %f +%.5g -%.5g'%(effMass*eff[iPsig].getVal(),effMass*abs(eff[iPsig].getErrorHi()),effMass*abs(eff[iPsig].getErrorLo())) )
s.append( '\tSF = %f +%f -%f'%(effMass*eff[iPsig].getVal()/(eff_[iPsig]*effMass_), effMass*abs(eff[iPsig].getErrorHi())/(eff_[iPsig]*effMass_), effMass*abs(eff[iPsig].getErrorLo())/(eff_[iPsig]*effMass_)) )

s = '\n'.join(s)

with open(basedir+'/fits/summary%s.txt'%plot_postfix,'w') as fout:
  fout.write(s)
print s
