#!/bin/bash
#SBATCH -o cluster.out
#SBATCH -e cluster.error
#SBATCH -p medium
#SBATCH --mem=104G

ja=cell.job #HepG2 and K562

PARMS=($(awk "NR==$SLURM_ARRAY_TASK_ID" $ja))
cell=${PARMS[0]}


python pipeline.get_batch_means.py $cell &> log/Batch.Means.$cell
