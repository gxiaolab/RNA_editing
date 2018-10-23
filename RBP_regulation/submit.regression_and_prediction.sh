#!/bin/bash

ja=batch.job

for i in 1 3
do
	PARMS=($(awk "NR==$i" $ja))
	cell=${PARMS[0]}
	rbp=${PARMS[1]}
	ctrl=${PARMS[2]}
	minCov=5


	mat_train=data/MATRIX_1.all_editing_sites.${cell}_${ctrl}.minCov_${minCov}.tab

	### Make RBP matrix for testing
	date 
	echo $outf 


	### Write matrix with editing ratios from batch means for differential editing  
	mat_test_in=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.no_batch_mean.both_rep_cov.tab
	mat_test=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.with_batch_mean.both_rep_cov.tab
	mat_batch_mean=data/BATCH_MEAN.${cell}_${ctrl}.by_rep.both_rep_cov.txt
	python pipeline.make_matrix_3.py $mat_test_in $mat_batch_mean $mat_test 
	echo "Batch editing means added to testing matrices" 
	date 


	### Variance Regression with training and testing datasets
	Reg_File=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.with_batch_mean.both_rep_cov.in
	Rscript pipeline.Reg.r $mat_train $mat_test $Reg_File 
	echo "Variance regression done" 
	date 


	### Predicting p-value from regression
	Pred_File=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.with_batch_mean.both_rep_cov.out
	number_of_reps=2
	Rscript pipeline.Pred.r $Reg_File $Pred_File $number_of_reps  
	echo "P-value prediction done"
	date 

    ### Correct p-value for multiple testing and add label
    python pipeline.parse_editing_files.py $Pred_File $Pred_File.fdr_corr.txt
    echo "BH correction done"
    date 
done
