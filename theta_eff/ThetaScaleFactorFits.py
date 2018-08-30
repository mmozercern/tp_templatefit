# -*- coding: utf-8 -*-

import numpy
import ROOT
from array import array

import os
import sys

sys.path.append('./')
from PostFitUncertainties import *
from PostFitCorrelations import *
from SFcalculation import *
#postifrom ThetaPostFitPlot import *


def run(fname_stat, fname_sys, outname_stat, outname_sys, calc_sfs = True, write_report = False):
    if write_report:report.reopen_file()

    inputpath = "thetaFilesNewSYS/mass_sub/"
    print 'use files in', inputpath

    model_stat = build_model_from_rootfile(inputpath+fname_stat)
    model_stat.fill_histogram_zerobins()

    model_sys = build_model_from_rootfile(inputpath+fname_sys)
    model_sys.fill_histogram_zerobins()

    print '================================================='
    print fname_sys
    print '================================================='

    rate_unc_high = math.log(1.0)
    rate_unc_low = math.log(1.0)

    model_stat.add_lognormal_uncertainty('3-prong_Pass_rate', rate_unc_low , procname='tn_3-prong',obsname='fj_jmarcorr_sdmass_pass')
    model_stat.add_lognormal_uncertainty('2-prong_Pass_rate',  rate_unc_high, procname='tn_2-prong',obsname='fj_jmarcorr_sdmass_pass')
    model_stat.add_lognormal_uncertainty('1-prong_Pass_rate', rate_unc_high , procname='tn_1-prong',obsname='fj_jmarcorr_sdmass_pass')

    model_sys.add_lognormal_uncertainty('3-prong_Pass_rate', rate_unc_low , procname='tn_3-prong',obsname='fj_jmarcorr_sdmass_pass')
    model_sys.add_lognormal_uncertainty('2-prong_Pass_rate',  rate_unc_high, procname='tn_2-prong',obsname='fj_jmarcorr_sdmass_pass')
    model_sys.add_lognormal_uncertainty('1-prong_Pass_rate', rate_unc_high , procname='tn_1-prong',obsname='fj_jmarcorr_sdmass_pass')


    model_stat.add_lognormal_uncertainty('3-prong_Fail_rate', rate_unc_high, procname='tn_3-prong',obsname='fj_jmarcorr_sdmass_fail')
    model_stat.add_lognormal_uncertainty('2-prong_Fail_rate', rate_unc_low, procname='tn_2-prong',obsname='fj_jmarcorr_sdmass_fail')
    model_stat.add_lognormal_uncertainty('1-prong_Fail_rate', rate_unc_low, procname='tn_1-prong',obsname='fj_jmarcorr_sdmass_fail') 

    model_sys.add_lognormal_uncertainty('3-prong_Fail_rate', rate_unc_high, procname='tn_3-prong',obsname='fj_jmarcorr_sdmass_fail')
    model_sys.add_lognormal_uncertainty('2-prong_Fail_rate', rate_unc_low, procname='tn_2-prong',obsname='fj_jmarcorr_sdmass_fail')
    model_sys.add_lognormal_uncertainty('1-prong_Fail_rate', rate_unc_low, procname='tn_1-prong',obsname='fj_jmarcorr_sdmass_fail') 


    options = Options()
    options.set('minimizer', 'strategy', 'robust')

    n_name_stat = deepcopy(outname_stat)
    n_name_stat = n_name_stat.replace(".root","_")
    n_name_sys = deepcopy(outname_sys)
    n_name_sys = n_name_sys.replace(".root","_")
 
    print '============'
    print 'stat'
    print '============'
    mle_output_stat = mle(model_stat, input='data', n=100, with_covariance=True, chi2=True, options=options, signal_process_groups ={'background_only':[]})
    print '============'
    print 'sys'
    print '============'
    mle_output_sys = mle(model_sys, input='data', n=100, with_covariance=True, chi2=True, options=options, signal_process_groups ={'background_only':[]})

    #PlotPostFitCorrelations(model_stat, mle_output_stat['background_only'], "fitResultsNewSYS/nuissance/Corr_"+n_name_stat)
    #PlotPostFitCorrelations(model_sys, mle_output_sys['background_only'], "fitResultsNewSYS/nuissance/Corr_"+n_name_sys)
   
    writeOutputFile(inputpath+fname_stat,  "fitResultsNewSYS/mass_sub/"+outname_stat, mle_output_stat['background_only'], model_stat)
    writeOutputFile(inputpath+fname_sys,  "fitResultsNewSYS/mass_sub/"+outname_sys, mle_output_sys['background_only'], model_sys)

    #writeOutputFile("thetaFilesNew+fname,  "fitResultsNewSYS/pt/"+outname, mle_output['background_only'], model, False)
    #writeOutputFile("thetaFilesNewSYS/tau32/"+fname,  "fitResultsNewSYS/tau32/"+outname, mle_output['background_only'], model, False)
    
    if calc_sfs:
        sfs = SFcalculation(inputpath+fname_stat, inputpath+fname_sys, mle_output_stat['background_only'], mle_output_sys['background_only'], model_stat, model_sys)

        if '_t_' in fname_stat:
            sfs.setMassWindow(105,210)
        else:
            sfs.setMassWindow(65,105)

        dictOut_stat = sfs.calcEfficiencies('stat')
        dictOut_sys = sfs.calcEfficiencies('sys')
    
#        for pf_vals in mle_output_stat.itervalues():
#            del pf_vals['__nll']
#            del pf_vals['__cov']
#        for pf_vals in mle_output_sys.itervalues():
#            del pf_vals['__nll']
#            del pf_vals['__cov']
     
#        postfit_stat = ThetaPostFitPlot(mle_output_stat)
#        postfit_stat.make_plots("fitResultsNewSYS/nuissance/",n_name_stat)

#       postfit_sys = ThetaPostFitPlot(mle_output_sys)
#       postfit_sys.make_plots("fitResultsNewSYS/nuissance/",n_name_sys)

        return [dictOut_stat, dictOut_sys]


###loop over taggers and wps


bins = array('d', [300, 400, 480, 600, 1200])
calculate_scaleFactors = True

#run("thetaFile_400_PUPPI_sys_.root", "Hists_400_PUPPI_sys.root")

wps = ["loose","medium","tight","50p"]


categories = { 't':['fj_nn_top','fj_decorr_nn_top'],
               'w':['fj_decorr_nn_w'] #['fj_nn_w','fj_decorr_nn_w']
               }

massbins={'t':['t1','t2','t3','t4'],
        'w':['w1','w2','w3']
        }

ranges={ 't1':[300,400],
         't2':[400,480],
         't3':[480,600],
         't4':[600,1200],
         'w1':[200,300],
         'w2':[300,400],
         'w3':[400,800],
         }

for part in ['w']: #['t','w']:
    for cat in categories[part]:
        for wp in wps: 

            fitresults=[]
            dicts_stat=[]
            dicts_sys=[]
            bins=[ranges[massbins[part][0]][0]]

            for bin in massbins[part]:
                fitresults.append(run("sf_"+part+"_"+cat+"_"+wp+"_"+bin+"_stat.root", "sf_"+part+"_"+cat+"_"+wp+"_"+bin+".root", "Hists_"+part+"_"+cat+"_"+wp+"_"+bin+"_stat.root", "Hists_"+part+"_"+cat+"_"+wp+"_"+bin+"_syst.root", calculate_scaleFactors))
                bins.append(ranges[bin][1])
        
            for res in fitresults:
                dicts_stat.append(res[0])
                dicts_sys.append(res[1])

            print bins
            print dicts_stat
            print dicts_sys

            WriteEffGraphs_separate("ScaleFactors_NoIso/eff_hists_"+part+"_"+cat+"_"+wp+".root", dicts_stat, dicts_sys, bins)


