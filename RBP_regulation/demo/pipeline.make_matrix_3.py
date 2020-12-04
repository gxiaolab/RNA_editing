#!/usr/bin/python
import sys
from collections import defaultdict
import numpy as np
from time import strftime


### Finish writing the matrix with testing data 
### by including the batch mean editing ratio


def get_batch_means(Batch_Ratios_File):
	gg = open(Batch_Ratios_File)	
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
RBP_Ratios_File, Batch_Ratios_File, RBP_Ratios_File_with_batch = sys.argv[1:4]

BatchMeans = get_batch_means(Batch_Ratios_File)
print strftime("%a, %d %b %Y %H:%M:%S\t"), "Batch means obtained"

mat2 = open(RBP_Ratios_File_with_batch, 'w')
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

		



