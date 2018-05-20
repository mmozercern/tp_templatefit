#!/bin/bash

ind=20180517_nn_ak8
massv=fj_jmarcorr_sdmass
match=TREE

for ptrange in  paperinct t1 t2 t3 t4 
do
    for syst in cent jes_up jes_down jer
    do
	for cuts in 0.1883 0.8511 0.9377 0.9897
	do
	    echo python distill_quantiles.py --indir=${ind}/${massv}/${match}/fj_nn_top_${cuts}/${ptrange}/ --var=fj_nn_top --masstag=$massv --nametag=pdf --type=quantile --indices=9-108
	    echo python distill_quantiles.py --indir=${ind}/${massv}/${match}/fj_nn_top_${cuts}/${ptrange}/ --var=fj_nn_top --masstag=$massv --nametag=qscale --type=envelope --indices=1,2,3,4,6,8
	done
	
	for cuts in 0.04738 0.4585 0.6556 0.8931
	do
	    echo python distill_quantiles.py --indir=${ind}/${massv}/${match}/fj_decorr_nn_top_${cuts}/${ptrange}/ --var=fj_decorr_nn_top --masstag=$massv --nametag=pdf --type=quantile --indices=9-108
	    echo  python distill_quantiles.py --indir=${ind}/${massv}/${match}/fj_decorr_nn_top_${cuts}/${ptrange}/ --var=fj_decorr_nn_top --masstag=$massv --nametag=qscale --type=envelope --indices=1,2,3,4,6,8	    
	done

    done
done

for ptrange in  paperincw w1 w2 w3 w4 
do
    for syst in cent jes_up jes_down jer
    do

	for cuts in 0.1491 0.8767 0.953 0.9928
	do
	    python distill_quantiles.py --indir=${ind}/${massv}/${match}/fj_nn_w_${cuts}/${ptrange}/ --var=fj_nn_w --masstag=$massv --nametag=pdf --type=quantile --indices=9-108
	    python distill_quantiles.py --indir=${ind}/${massv}/${match}/fj_nn_w_${cuts}/${ptrange}/ --var=fj_nn_w --masstag=$massv --nametag=qscale --type=envelope --indices=1,2,3,4,6,8	    
	done
	
	for cuts in 0.07203 0.4633 0.6482 0.8936
	do
	    python distill_quantiles.py --indir=${ind}/${massv}/${match}/fj_decorr_nn_w_${cuts}/${ptrange}/ --var=fj_decorr_nn_w --masstag=$massv --nametag=pdf --type=quantile --indices=9-108
	    python distill_quantiles.py --indir=${ind}/${massv}/${match}/fj_decorr_nn_w_${cuts}/${ptrange}/ --var=fj_decorr_nn_w --masstag=$massv --nametag=qscale --type=envelope --indices=1,2,3,4,6,8	    
	done

    done    
done


