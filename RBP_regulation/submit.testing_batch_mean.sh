#!/bin/bash
#SBATCH -o cluster.out
#SBATCH -e cluster.error
#SBATCH -p medium
#SBATCH --mem=4G

cell=HepG2   
batch=CONTROL305XWT

outfile=data/BATCH_MEAN.${cell}_${batch}.by_rep.both_rep_cov.txt

batch_files=`ls data/MATRIX_2.all_editing_sites.*.minCov_5.no_batch_mean.both_rep_cov.tab | tr '\n' ','`

python pipeline.get_batch_means.py $batch_files $outfile &> log/Batch.Means.$cell
