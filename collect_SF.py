#!/usr/bin/env python
import ROOT
import math

ROOT.gROOT.SetBatch(True)

ROOT.gErrorIgnoreLevel=ROOT.kError

WPs = ['loose','medium','tight','very_tight']
particles = ['w','t']
categories = {'t':['fj_nn_top','fj_decorr_nn_top'],
              'w':['fj_nn_w','fj_decorr_nn_w']
              }

constraints = ['N']

cutvals = { 'fj_nn_top' : {'loose':'0.1883',
                           'medium':'0.8511',
                           'tight':'0.9377',
                           'very_tight':'0.9897'
                           },
            'fj_decorr_nn_top':{ 'loose':'0.04738',
                                 'medium':'0.4585',
                                 'tight':'0.6556',
                                 'very_tight':'0.8931',
                                 },
            'fj_nn_w':{ 'loose':'0.1491',
                        'medium':'0.8767',
                        'tight':'0.953',
                        'very_tight':'0.9928',
                        },
            'fj_decorr_nn_w':{ 'loose':'0.07203',
                               'medium':'0.4633',
                               'tight':'0.6482',
                               'very_tight':'0.8936',
                               },

           }

massvar ={ 'puppisd'   : 'fj_jmarcorr_sdmass'}

syserrs = ['Resolution','ScaleUp','ScaleDown','qscale_up','qscale_down','pdf_up','pdf_down','herwig']

constraintvals = { 'N': ['0']}

massbins={'t':['t1','t2','t3','t4'],
          'w':['w1','w2','w3']
          }

inclabels={'t':'paperinct',
           'w':'paperincw'
           }

ranges={ 't1':[300,400],
         't2':[400,480],
         't3':[480,600],
         't4':[600,1200],
         'w1':[200,300],
         'w2':[300,400],
         'w3':[400,800],
         }


dirprefix='20180517_nn_ak8/fj_jmarcorr_sdmass/TREE/'


ptminmax = { 't': [300,1200],
             'w': [200,800]
                 }


def readfromfile(fname):
    result=0.
    error =0.
    with open(fname) as f:
        content = f.readlines()
        for line in content:
            if line.strip()[:2]!='SF':
                continue
            substrings = line.split(' ')
                #print substrings[2],substrings[3]
            result=float(substrings[2])
            error=float(substrings[3])
    return result,error

def getscaletuple(cat,wp,ptrange):
    directory = dirprefix +'/'+cat+'_'+cutvals[cat][wp]+'/'
    #print 'reading nominal value from: ', directory
    nominal=0. # central value + stat + syst errors
    stat=0.
    sysup=0.
    sysdown=0.
    fname=directory+ptrange+'/fits/summary_unconstr.txt'
    res,err=readfromfile(fname)
    nominal=res
    stat=err
    sysup=err
    sysdown=err
    for sys in syserrs:
        fname=directory+ptrange+'/fits/summary_'+sys+'.txt'
        res,err=readfromfile(fname)
        if res > nominal:
            sysup = math.sqrt(sysup*sysup + (nominal-res)*(nominal-res))
        else:
            sysdown = math.sqrt(sysup*sysup + (nominal-res)*(nominal-res))

    return nominal,stat,sysup,sysdown
    

lineinc = ROOT.TLine()
for part in particles:

    mainhist = ROOT.TH1F('main','main',1,ptminmax[part][0],ptminmax[part][1])
    mainhist.SetMinimum(0.)
    mainhist.SetMaximum(2.)
   
    graphs={}
    
    canvas = ROOT.TCanvas("c2","c2",50,50,600,600)


    for cat in categories[part]:
        print "\\begin{tabular}{ l | ",
        numwps=3
        for i in xrange(len(massbins[part])):
            print " r@{\,}c@{\,}l@{\,}c@{\,}l ",
        print '}'
        print '\\multicolumn{',5*(len(massbins[part]))+1,'}{c}{Scale factors for ', cat.replace('_','\\_') ,' $\\pm$(stat.)$^+_-$(syst.)}\\\\'
        print "\\hline"
        print 'working point & \\multicolumn{',5*(len(massbins[part])),'}{c}{\\pt ranges [GeV]}\\\\'
        for i in xrange(len(massbins[part])):
            print "& \\multicolumn{5}{c}{",ranges[massbins[part][i]][0],"-",ranges[massbins[part][i]][1],'}',
        print "\\\\"
        print "\\hline"

        for wp in WPs:
            canvas.Clear()   
            
            print wp.replace('_',' '),

        #inclusive scale factor
            #print 'inclusive for: ' + cat +' > ' +wp
            #print getscaletuple(cat,wp,inclabels[part])
            inclusive_cent,inclusive_stat,inclusive_sysup,inclusive_sysdown=getscaletuple(cat,wp,inclabels[part])

        #scale factor
            graphs[(cat,wp,'stat','unconstr')]=ROOT.TGraphAsymmErrors(len(massbins[part]))
            graphs[(cat,wp,'syst','unconstr')]=ROOT.TGraphAsymmErrors(len(massbins[part]))
            graphs[(cat,wp,'nom','unconstr')]=ROOT.TGraphAsymmErrors(len(massbins[part]))
            graphs[(cat,wp,'stat','unconstr')].SetFillColor(ROOT.kOrange)
            graphs[(cat,wp,'syst','unconstr')].SetFillColor(ROOT.kOrange-3)
            for i in xrange(len(massbins[part])):
                #print 'differential for: '+ massbins[part][i] +' ' + cat +' > ' +wp
                #print getscaletuple(cat,wp,massbins[part][i])
                cent,stat,sysup,sysdown = getscaletuple(cat,wp,massbins[part][i])
                #print massbins[part][i]
                #print ranges['w1']
                graphs[(cat,wp,'stat','unconstr')].SetPoint(i,(ranges[massbins[part][i]][1]+ranges[massbins[part][i]][0])/2. , cent )
                graphs[(cat,wp,'stat','unconstr')].SetPointError(i,(ranges[massbins[part][i]][1]-ranges[massbins[part][i]][0])/2.,(ranges[massbins[part][i]][1]-ranges[massbins[part][i]][0])/2.,stat,stat)
                graphs[(cat,wp,'syst','unconstr')].SetPoint(i,(ranges[massbins[part][i]][1]+ranges[massbins[part][i]][0])/2. , cent )
                graphs[(cat,wp,'syst','unconstr')].SetPointError(i,(ranges[massbins[part][i]][1]-ranges[massbins[part][i]][0])/2.,(ranges[massbins[part][i]][1]-ranges[massbins[part][i]][0])/2.,sysup,sysdown)
                graphs[(cat,wp,'nom','unconstr')].SetPoint(i,(ranges[massbins[part][i]][1]+ranges[massbins[part][i]][0])/2. , cent )
                graphs[(cat,wp,'nom','unconstr')].SetPointError(i,(ranges[massbins[part][i]][1]-ranges[massbins[part][i]][0])/2.,(ranges[massbins[part][i]][1]-ranges[massbins[part][i]][0])/2.,0,0)
                
                sup=round(math.sqrt(sysup*sysup-stat*stat),2)
                if sup==0.0:
                    sup='<0.01'
                else:
                    sup='{:.02f}'.format(sup)
                sdo=round(math.sqrt(sysdown*sysdown-stat*stat),2)                
                if sdo==0.0:
                    sdo='<0.01'
                else:
                    sdo='{:.02f}'.format(sdo)
                sta=round(stat,2)
                if sta==0.0:
                    sta='<0.01'
                else:
                    sta='{:.02f}'.format(sta)
                    
                print '&','{:.02f}'.format(round(cent,2)),'&$\\pm$&',sta,'&$^+_-$&$^{',sup,'}_{',sdo,'}$',
            print "\\\\"
                
            mainhist.Draw()
        
        
            graphs[(cat,wp,'syst','unconstr')].Draw('same 2')
            graphs[(cat,wp,'stat','unconstr')].Draw('same 2')
            graphs[(cat,wp,'nom','unconstr')].Draw('same Z')
            lineinc.DrawLine(ptminmax[part][0],inclusive_cent,ptminmax[part][1],inclusive_cent)
            canvas.SaveAs(cat+'_'+wp+'.pdf')
            canvas.SaveAs(cat+'_'+wp+'.png')

        print '\\end{tabular}'
        print
