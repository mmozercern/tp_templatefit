import ROOT

prefix="../tp_templatefit/20180609X_nn_ak8"
outdir="thetaFilesNewSYS/mass_sub/"
WPs = ['loose','medium','tight','very_tight','50p']
particles = ['w','t']
categories = {'t':['fj_nn_top','fj_decorr_nn_top'],
              'w':['fj_nn_w','fj_decorr_nn_w']
              }

constraints = ['N']

cutvals = { 'fj_nn_top' : {'loose':'0.1883',
                           'medium':'0.8511',
                           'tight':'0.9377',
                           '50p':'0.9251',
                           'very_tight':'0.9897'
                           },
            'fj_decorr_nn_top':{ 'loose':'0.04738',
                                 'medium':'0.4585',
                                 'tight':'0.6556',
                                 '50p':'0.3452',
                                 'very_tight':'0.8931',
                                 },
            'fj_nn_w':{ 'loose':'0.1491',
                        'medium':'0.8767',
                        'tight':'0.953',
                        '50p':'0.9838',
                        'very_tight':'0.9928',
                        },
            'fj_decorr_nn_w':{ 'loose':'0.07203',
                               'medium':'0.4633',
                               'tight':'0.6482',
                               '50p':'0.6654',
                               'very_tight':'0.8936',
                               },

           }


massvar ='fj_jmarcorr_sdmass'


syserrs = ['pdf','qscale','truePUWeight_','muEffWeight_','btagWeight_HEAVY','btagWeight_LIGHT','jer','jes']
#systematic uncertainties where proper templates exist for both variations

onesideds = ['herwig']
#systematic uncertainties with only a asingle variation

massbins={'t':['paperinct','t1','t2','t3','t4'],
          'w':['paperincw','w1','w2','w3']
          }

udtrans={'up':'plus',
        'down':'minus'}


def remove_negatives(histo):# negative template entries due to NLO weights make theta crash => set them to zero
    while histo.GetMinimum() < 0:
        #print "found negative bin " , histo.GetMinimum()
        histo.SetBinContent(histo.GetMinimumBin(),0.001)

for part in particles:
    for cat in categories[part]:
        for wp in WPs:
            for bin in massbins[part]:
                print "setting up histos for :",part,cat,wp,bin
                
                outf=ROOT.TFile.Open(outdir+'sf_%s_%s_%s_%s.root'%(part,cat,wp,bin),'recreate')
                outfunsc=ROOT.TFile.Open(outdir+'sf_%s_%s_%s_%s_NotScaled.root'%(part,cat,wp,bin),'recreate')
                outfstat=ROOT.TFile.Open(outdir+'sf_%s_%s_%s_%s_stat.root'%(part,cat,wp,bin),'recreate')
                outfstatunsc=ROOT.TFile.Open(outdir+'sf_%s_%s_%s_%s_stat_NotScaled.root'%(part,cat,wp,bin),'recreate')


                normmap={}

                for pf in ['pass','fail']:
                #nominal:
                    inf=ROOT.TFile.Open(prefix+'/%s/TREE/%s_%s/%s/tag_%s_%s_hists.root'%(massvar,cat,cutvals[cat][wp],bin,cat,pf))
                    data = inf.Get('h_%s_Data'%(massvar)).Clone('%s_%s__DATA'%(massvar,pf))
                    outf.cd()
                    data.Write()
                    outfstat.cd()
                    data.Write()
                    outfunsc.cd()
                    data.Write()
                    outfstatunsc.cd()
                    data.Write()
                    
                    for prong in ['1-prong','2-prong','3-prong']:
                        tmph = inf.Get('h_%s_%s'%(massvar,prong)).Clone('%s_%s__%s'%(massvar,pf,prong))
                        remove_negatives(tmph)
                        normmap[(pf,prong)]=tmph.Integral(0,tmph.GetNbinsX()+1)
                        outf.cd()
                        tmph.Write()
                        outfstat.cd()
                        tmph.Write()
                        outfunsc.cd()
                        tmph.Write()
                        outfstatunsc.cd()
                        tmph.Write()
                    inf.Close()
                   
                for syst in syserrs:
                    for ud in ['up','down']:
                        infp=ROOT.TFile.Open(prefix+'/%s/TREE/%s_%s/%s/tag_%s_%s_%s_%s_hists.root'%(massvar,cat,cutvals[cat][wp],bin,cat,'pass',syst,ud))
                        inff=ROOT.TFile.Open(prefix+'/%s/TREE/%s_%s/%s/tag_%s_%s_%s_%s_hists.root'%(massvar,cat,cutvals[cat][wp],bin,cat,'fail',syst,ud))
                        adjustedsys=''
                        if(syst[-1]=='_'):
                            adjustedsys=syst[0:-1]
                        else:
                            adjustedsys=syst

                        for prong in ['1-prong','2-prong','3-prong']:
                            tmphp = infp.Get('h_%s_%s'%(massvar,prong)).Clone('%s_%s__%s__%s__%s'%(massvar,'pass',prong,adjustedsys,udtrans[ud]))
                            tmphf = inff.Get('h_%s_%s'%(massvar,prong)).Clone('%s_%s__%s__%s__%s'%(massvar,'fail',prong,adjustedsys,udtrans[ud]))
                            remove_negatives(tmphp)
                            remove_negatives(tmphf)                            
                            scalefac = (normmap[('pass',prong)]+normmap[('fail',prong)])/(tmphf.Integral(0,tmphf.GetNbinsX()+1) + tmphp.Integral(0,tmphp.GetNbinsX()+1))
                            tmphp.Scale(scalefac)
                            tmphf.Scale(scalefac)
                            outf.cd()
                            tmphp.Write()
                            tmphf.Write()
                        inff.Close()
                        infp.Close()

                for syst in onesideds:
                    infp=ROOT.TFile.Open(prefix+'/%s/TREE/%s_%s/%s/tag_%s_%s_%s_hists.root'%(massvar,cat,cutvals[cat][wp],bin,cat,'pass',syst))
                    inff=ROOT.TFile.Open(prefix+'/%s/TREE/%s_%s/%s/tag_%s_%s_%s_hists.root'%(massvar,cat,cutvals[cat][wp],bin,cat,'fail',syst))
                    
                    infnomp = ROOT.TFile.Open(prefix+'/%s/TREE/%s_%s/%s/tag_%s_%s_hists.root'%(massvar,cat,cutvals[cat][wp],bin,cat,'pass'))
                    infnomf = ROOT.TFile.Open(prefix+'/%s/TREE/%s_%s/%s/tag_%s_%s_hists.root'%(massvar,cat,cutvals[cat][wp],bin,cat,'fail'))

                    for prong in ['1-prong','2-prong','3-prong']:
                        tmphp = infp.Get('h_%s_%s'%(massvar,prong)).Clone('%s_%s__%s__%s__%s'%(massvar,'pass',prong,syst,udtrans['up']))
                        tmphf = inff.Get('h_%s_%s'%(massvar,prong)).Clone('%s_%s__%s__%s__%s'%(massvar,'fail',prong,syst,udtrans['up']))
                        remove_negatives(tmphp)
                        remove_negatives(tmphf)                            
                        scalefac = (normmap[('pass',prong)]+normmap[('fail',prong)])/(tmphf.Integral(0,tmphf.GetNbinsX()+1) + tmphp.Integral(0,tmphp.GetNbinsX()+1))
                        tmphp.Scale(scalefac)
                        tmphf.Scale(scalefac)
                        outf.cd()
                        tmphp.Write()
                        tmphf.Write()

                        tmphnomp = infnomp.Get('h_%s_%s'%(massvar,prong)).Clone('%s_%s__%s__%s__%s'%(massvar,'pass',prong,syst,udtrans['down'])) 
                        tmphnomf = infnomf.Get('h_%s_%s'%(massvar,prong)).Clone('%s_%s__%s__%s__%s'%(massvar,'fail',prong,syst,udtrans['down']))
                        tmphnomp.Scale(2.0)
                        tmphnomf.Scale(2.0)
                        tmphnomp.Add(tmphp,-1.)
                        tmphnomf.Add(tmphf,-1.)
                        remove_negatives(tmphnomp)
                        remove_negatives(tmphnomf)                            
                        outf.cd()
                        tmphnomp.Write()
                        tmphnomf.Write()



                    inff.Close()
                    infp.Close()
                    infnomf.Close()
                    infnomp.Close()
                    

                outf.Close()
                outfstat.Close()
                outfunsc.Close()
                outfstatunsc.Close()
