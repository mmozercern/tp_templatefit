#!/bin/bash

ind=../20170921_nn_ak8/lep/
outd=20170921_nn_ak8
massv='efnl1_ak8puppi_sdmass'

for ptrange in inc inch 
do
    for match in MATCH POG POG8 HYBRID HYBRID8 NEW
    do
    #top quark
	for cuts in 0.11 0.77
	do
	    for tag in True False
	    do
		python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc=efnl1_ak8_nn_top --cut=$cuts --massvar='efnl1_ak8puppi_sdmass' --tagged=$tag --binning='50,350,30' --matching=$match
	    done
	done
    #W boson
	for cuts in 0.15 0.66
	do
	    for tag in True False
	    do                                                                             
		python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc=efnl1_ak8_nn_w --cut=$cuts --massvar='efnl1_ak8puppi_sdmass' --tagged=$tag --binning='50,250,40' --matching=$match
	    done
	done   
    done
done

