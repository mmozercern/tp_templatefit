#!/usr/bin/env python
from os import system,mkdir,getenv,path,getcwd
import argparse
from sys import argv

parser = argparse.ArgumentParser(description='fit stuff')
parser.add_argument('--indir',metavar='indir',type=str)
parser.add_argument('--var',metavar='var',type=str,default='efnl1_ak8_nn_top')
parser.add_argument('--masstag',metavar='masstag',type=str,default='efnl1_ak8mass')
parser.add_argument('--indices',metavar='indices',type=str,default='1,2,3,4,6,8') # comaa-separted list or X-Y
parser.add_argument('--type',metavar='type',type=str,default='envelope') # envelope or quantile
parser.add_argument('--nametag',metavar='nametag',type=str,default='qscale')
args = parser.parse_args()
basedir = args.indir

import ROOT as root
root.gROOT.SetBatch(True)



errnums=[]
if "," in args.indices:
    errnums = [int(item) for item in args.indices.split(',')]

if "-" in args.indices:
    errnums = range( int(args.indices.split('-')[0]), int(args.indices.split('-')[1])+1)
print errnums


procs=['1-prong','2-prong','3-prong']
cats=['pass','fail']

for cat in cats:
    inf  = root.TFile(basedir+'tag_%s_%s_hists.root'%(args.var,cat),'READ')
    outf = root.TFile(basedir+'tag_%s_%s_%s_up_hists.root'%(args.var,cat,args.nametag),"RECREATE")
    datahist=inf.Get('h_%s_Data'%(args.masstag))
    datahist.Write()
    for proc in procs:
        histos=[inf.Get('h_%s_%s_systweights[%d]_Up'%(proc,args.masstag,errno)) for errno in errnums]
        binarrays=[ [hist.GetBinContent(binnr)  for hist in histos ] for binnr in range(1,histos[0].GetNbinsX()+1)]
        for array in binarrays:
            array.sort()
        
        histoout=histos[0].Clone('h_%s_%s'%(args.masstag,proc))
        if args.type=='envelope':
            for bin in range(histos[0].GetNbinsX()):
                histoout.SetBinContent(bin+1,binarrays[bin][-1])
        if args.type=='quantile':
            for bin in range(histos[0].GetNbinsX()):
                histoout.SetBinContent(bin+1,binarrays[bin][-int(0.16*len(binarrays[0]))])
        histoout.Write()                

    #copy data hist as well
    

    inf.Close()
    outf.Close()

for cat in cats:
    inf  = root.TFile(basedir+'tag_%s_%s_hists.root'%(args.var,cat))
    outf = root.TFile(basedir+'tag_%s_%s_%s_down_hists.root'%(args.var,cat,args.nametag),"RECREATE")
    datahist=inf.Get('h_%s_Data'%(args.masstag))
    datahist.Write()
    for proc in procs:
        histos=[inf.Get('h_%s_%s_systweights[%d]_Up'%(proc,args.masstag,errno)) for errno in errnums]
        binarrays=[ [hist.GetBinContent(binnr)  for hist in histos ] for binnr in range(1,histos[0].GetNbinsX()+1)]
        for array in binarrays:
            array.sort()
        
        histoout=histos[0].Clone('h_%s_%s'%(args.masstag,proc))
        if args.type=='envelope':
            for bin in range(histos[0].GetNbinsX()):
                histoout.SetBinContent(bin+1,binarrays[bin][0])
        if args.type=='quantile':
            for bin in range(histos[0].GetNbinsX()):
                histoout.SetBinContent(bin+1,binarrays[bin][int(0.16*len(binarrays[0]))])
        histoout.Write()                

    inf.Close()
    outf.Close()

