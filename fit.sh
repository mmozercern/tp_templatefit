#!/bin/bash

ind=20180517_nn_ak8
massv=fj_jmarcorr_sdmass
match=TREE

for ptrange in  paperinct t1 t2 t3 t4 
do
    for syst in cent jes_up jes_down pdf_up pdf_down qscale_up qscale_down jer
    do
	for cuts in 0.1883 0.8511 0.9377 0.9897
	do
	    python fitSimultaneousMC.py --indir=${ind}/${massv}/${match}/fj_nn_top_${cuts}/${ptrange}/ --var=fj_nn_top --masstag=$massv --signal=top --syst=$syst
	    echo  python fitSimultaneousMC.py --indir=${ind}/${massv}/${match}/fj_nn_top_${cuts}/${ptrange}/ --var=fj_nn_top --masstag=$massv --signal=top --syst=$syst
	done
	
	for cuts in 0.04738 0.4585 0.6556 0.8931
	do
	    python fitSimultaneousMC.py --indir=${ind}/${massv}/${match}/fj_decorr_nn_top_${cuts}/${ptrange}/ --var=fj_decorr_nn_top --masstag=$massv --signal=top --syst=$syst
	    echo python fitSimultaneousMC.py --indir=${ind}/${massv}/${match}/fj_decorr_nn_top_${cuts}/${ptrange}/ --var=fj_decorr_nn_top --masstag=$massv --signal=top --syst=$syst
	done

    done
done

for ptrange in  paperincw w1 w2 w3 w4 
do
    for syst in cent jes_up jes_down pdf_up pdf_down qscale_up qscale_down jer
    do

	for cuts in 0.1491 0.8767 0.953 0.9928
	do
	    python fitSimultaneousMC.py --indir=${ind}/${massv}/${match}/fj_nn_w_${cuts}/${ptrange}/ --var=fj_nn_w --masstag=$massv --signal=W --syst=$syst
	    echo python fitSimultaneousMC.py --indir=${ind}/${massv}/${match}/fj_nn_w_${cuts}/${ptrange}/ --var=fj_nn_w --masstag=$massv --signal=W --syst=$syst
	done
	
	for cuts in 0.07203 0.4633 0.6482 0.8936
	do
	    python fitSimultaneousMC.py --indir=${ind}/${massv}/${match}/fj_decorr_nn_w_${cuts}/${ptrange}/ --var=fj_decorr_nn_w --masstag=$massv --signal=W --syst=$syst
	    echo python fitSimultaneousMC.py --indir=${ind}/${massv}/${match}/fj_decorr_nn_w_${cuts}/${ptrange}/ --var=fj_decorr_nn_w --masstag=$massv --signal=W --syst=$syst
	done

    done    
done


