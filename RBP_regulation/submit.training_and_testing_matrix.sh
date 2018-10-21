#!/bin/bash
#SBATCH -o cluster.out
#SBATCH -e cluster.error
#SBATCH -p medium
#SBATCH --mem=24G

# ^^ cluster parameters to run jobs in parallel

ja=all_rbps_info.tab

PARMS=($(awk "NR==$SLURM_ARRAY_TASK_ID" $ja))
cell=${PARMS[0]}
rbp=${PARMS[1]}
ctrl=${PARMS[3]}
minCov=5


echo $cell $rbp $cntrl > log/matrix1.$cell.$cntrl.$SLURM_ARRAY_TASK_ID

if [ "$ctrl" eq "CONTROLNA" ]
then
	mat_train=data/MATRIX_1.all_editing_sites.${cell}_${cntrl}.minCov_${minCov}.tab
	python pipeline.make_matrix_1.py $cell $cntrl $minCov $mat_train &>> log/matrix1.$cell.$cntrl.$SLURM_ARRAY_TASK_ID
fi

mat_test=data/MATRIX_2.all_editing_sites.${cell}_${rbp}.minCov_${minCov}.tab
python pipeline.make_matrix_2.py $cell $rbp $minCov $mat_test &>> $log/matrix2.$cell.$cntrl.$SLURM_ARRAY_TASK_ID

