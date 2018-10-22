#!/bin/bash
#SBATCH -o cluster.out
#SBATCH -e cluster.error
#SBATCH -p short
#SBATCH --mem=2G

# ^^ cluster parameters to run jobs in parallel

ja=batch.job

PARMS=($(awk "NR==$SLURM_ARRAY_TASK_ID" $ja))
cell=${PARMS[0]}
rbp=${PARMS[1]}
ctrl=${PARMS[2]}
minCov=5


echo $cell $rbp $ctrl > log/matrix1.$cell.$ctrl.$SLURM_ARRAY_TASK_ID


rdd_file=data/editing_sites.${rbp}_Rep1.txt,data/editing_sites.${rbp}_Rep2.txt 

if [ "$ctrl" = "CONTROLNA" ]
then
	mat_train=data/MATRIX_1.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.tab
	python pipeline.make_matrix_1.py $rdd_file $minCov $mat_train &>> log/matrix1.$cell.$ctrl.$SLURM_ARRAY_TASK_ID
    echo "Training data set" &>> log/matrix1.$cell.$ctrl.$SLURM_ARRAY_TASK_ID
fi

mat_test=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.tab
python pipeline.make_matrix_2.py $rdd_file $minCov $mat_test &>> log/matrix2.$cell.$ctrl.$SLURM_ARRAY_TASK_ID
echo "Testing data set" &>> log/matrix1.$cell.$ctrl.$SLURM_ARRAY_TASK_ID

