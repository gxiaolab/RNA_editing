#!/bin/bash
#SBATCH -o cluster.out
#SBATCH -e cluster.error
#SBATCH -p medium
#SBATCH --mem=64G

# ^^ cluster parameters to run jobs in parallel


ja=all_rbps_info.controls.tab

PARMS=($(awk "NR==$SLURM_ARRAY_TASK_ID" $ja))
cell=${PARMS[0]}
rbp=${PARMS[1]}
ctrl=${PARMS[3]}
minCov=5


mat_train=data/MATRIX_1.all_editing_sites.${cell}_${ctrl}.minCov_${minCov}.tab
logi=log/NewReg.matrix2.$cell.$rbp.$SLURM_ARRAY_TASK_ID


### Make RBP matrix for testing
date > $logi
echo $outf >> $logi


### Write matrix with editing ratios from batch means for differential editing  
mat_test=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.with_batch_mean.both_rep_cov.tab
python pipeline.make_matrix_3.py $cell $rbp &>> $logi


### Variance Regression with training and testing datasets
Reg_File=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.with_batch_mean.both_rep_cov.in
Rscript pipeline.Reg.r $mat_train $mat_test $Reg_File &>> $logi
echo "Variance prediction done" >> $logi
date >> $logi


### Predicting p-value from regression
Pred_File=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.with_batch_mean.both_rep_cov.out
number_of_reps=2
Rscript pipeline.Pred.r $Reg_File $Pred_File $number_of_reps &>> $logi 
echo "P-value prediction done" >> $logi
date >> $logi

