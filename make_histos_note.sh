#!/bin/bash

ind=/dev/shm/mmozer/20180608_nn_ak8/lep/
outd=20180609X_nn_ak8
massv='fj_jmarcorr_sdmass'

for ptrange in paperinct #t1 t2 t3 t4 
do
    for match in TREE
    do
        for tag in True False
        do
	    for syst in herwig  #none jer_down jer_up jes_down jes_up herwig
	    do
		#top quark nominal
		for cuts in 0.1883 #0.8511 0.9251 0.9377 0.9897
		do
		    echo python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc='fj_nn_top' --cut=$cuts --massvar=$massv --tagged=$tag --binning='50,300,25' --matching=$match --syst=$syst
		    python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc='fj_nn_top' --cut=$cuts --massvar=$massv --tagged=$tag --binning='50,300,25' --matching=$match --syst=$syst &
		done
        	#top quark decorr
		for cuts in 0.04738 #0.3452 0.4585 0.6556 0.8931
		do
		    echo X
		    #echo python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc='fj_decorr_nn_top' --cut=$cuts --massvar=$massv --tagged=$tag --binning='50,300,25' --matching=$match --syst=$syst
		    #python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc='fj_decorr_nn_top' --cut=$cuts --massvar=$massv --tagged=$tag --binning='50,300,25' --matching=$match --syst=$syst &
		done
		
		wait
	    done
	done
    done
done 

for ptrange in paperincw w1 w2 w3 
do
    for match in TREE
    do
        for tag in True False
        do
	    for syst in herwig jer_up #none jer_down jer_up jes_down jes_up herwig
	    do

	    	# W nominal
		for cuts in  0.1491 0.8767 0.9530 0.9838 0.9928
		do
		    echo  python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc='fj_nn_w' --cut=$cuts --massvar=$massv --tagged=$tag --binning='50,250,40' --matching=$match --syst=$syst
		    #python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc='fj_nn_w' --cut=$cuts --massvar=$massv --tagged=$tag --binning='50,250,40' --matching=$match --syst=$syst
		done
		
		# W decorrelated
		for cuts in 0.07203 0.4633 0.6482 0.6654 0.8936
		do
		    echo  python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc='fj_decorr_nn_w' --cut=$cuts --massvar=$massv --tagged=$tag --binning='50,250,40' --matching=$match --syst=$syst
		    #python makeSFTemplates.py --pt=$ptrange --indir=$ind --outdir=$outd --disc='fj_decorr_nn_w' --cut=$cuts --massvar=$massv --tagged=$tag --binning='50,250,40' --matching=$match --syst=$syst
	    
		done
	    done
	done
    done
done
