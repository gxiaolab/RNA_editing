#!/bin/bash

ja=batch.job

for i in `seq 1 3`
do
    PARMS=($(awk "NR==$i" $ja))
    cell=${PARMS[0]}
    rbp=${PARMS[1]}
    ctrl=${PARMS[2]}
    minCov=5
    echo $cell $rbp $ctrl 

    rdd_file=data/editing_sites.${rbp}_Rep1.txt,data/editing_sites.${rbp}_Rep2.txt 

    if [ "$ctrl" = "CONTROLNA" ]
    then
    	mat_train=data/MATRIX_1.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.tab
    	python pipeline.make_matrix_1.py $rdd_file $minCov $mat_train 
        echo "Training data set"
    fi

    mat_test=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.tab
    python pipeline.make_matrix_2.py $rdd_file $minCov $mat_test 

    echo "Testing data set" 
done
