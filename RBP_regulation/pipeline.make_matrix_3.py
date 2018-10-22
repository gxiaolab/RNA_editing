#!/usr/bin/python
import sys
from collections import defaultdict
import numpy as np
from time import strftime


### Finish writing the matrix with testing data 
### by including the batch mean editing ratio


def get_batch_info():
	batches = {}
	with open("batch.job") as FF:
		for line in FF:
			cell, rbp, batch = line.split()[:3]
			if rbp.startswith('CONTROL'):
				batches[(cell, rbp)] = rbp
			else:
				batches[(cell, rbp)] = batch	
	return batches


def get_batch_means(cell, rbp):
	batches = get_batch_info()
	control = batches[(cell, rbp)]
	gg = open("data/BATCH_MEAN.{}_{}.by_rep.both_rep_cov.txt".format(cell, control))	
	BatchMeans = defaultdict(dict)
	for line in gg:
		# chr9:74597981:A.to.G    NA      C9orf85 UTR3    antisense-ALU   CONTROL003EKR
		L = line.split()
		ksite, batch_mean, gene, region, alu, batch = L
		chrom, pos = ksite.split(':')[:2]
		if batch_mean == "NA":
			continue
		BatchMeans[(chrom, pos[:3])][ksite] = [float(batch_mean), gene, region, alu, batch]
	return BatchMeans


print strftime("%a, %d %b %Y %H:%M:%S\t"), "Script starts"
cell, rbp = sys.argv[1:3]
RBP_Ratios_File = "data/MATRIX_2.all_editing_sites.{}_{}.minCov_5.no_batch_mean.both_rep_cov.tab".format(cell, rbp)

BatchMeans = get_batch_means(cell, rbp)
print strftime("%a, %d %b %Y %H:%M:%S\t"), "Batch means obtained"

mat2 = open(RBP_Ratios_File.replace('.no_batch_mean.both_rep_cov.tab', '.with_batch_mean.both_rep_cov.tab'), 'w')
mat2.write('Site_ID\tMeanRatio\tMeanCov\tBatchRatio\tGene\tRegion\tALU\tbatch\n')

	
with open(RBP_Ratios_File) as FF:
	next(FF)
	for line in FF:
		ksite, kd_MeanRatio, MeanCov = line.split()
		chrom, pos = ksite.split(':')[:2]
		kd_MeanRatio = float(kd_MeanRatio)
		try:
			ext_info = BatchMeans[(chrom, pos[:3])][ksite]
			batch_MeanRatio = ext_info[0]
		except:
			continue
		if max(batch_MeanRatio, kd_MeanRatio) > 0.1:
			outline2 = [ksite, kd_MeanRatio, MeanCov] + ext_info
			mat2.write('\t'.join(map(str, outline2)) + '\n')
	print strftime("%a, %d %b %Y %H:%M:%S\t"),  "File DONE!"
mat2.close()

		



