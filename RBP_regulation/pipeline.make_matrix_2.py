#!/usr/bin/python
import sys
from collections import defaultdict
import numpy as np
from time import strftime


### Write matrix to test the regression model
### One matrix per RBP-KD per cell line.
### It includes the coordinates of the editing site, mean coverage, and mean editing ratio


def parse_file(ff, dic, Rep):
	'''
	Obtain read coverage and editing ratio for every site
	'''
	f = open(ff)
	for line in f:
		l = line.split()
		chrm, pos, editing_type, edited_reads, total_reads = l[:5]
		edited_reads, total_reads = map(int, (edited_reads, total_reads))
		ratio = edited_reads/float(total_reads)
		key = (chrm, editing_type)
		try:
			dic[key][pos][Rep] = [ratio, total_reads]
		except:
			dic[key][pos] = {Rep : [ratio, total_reads]}
	f.close()



print strftime("%a, %d %b %Y %H:%M:%S\t"), "Script starts"

RDD_file_reps, min_Coverage, out_file = sys.argv[1:4]

RDD_file_reps = RDD_file_reps.strip(',')

SiteDict = defaultdict(dict)
for i, rdd_file in enumerate(RDD_file_reps.split(',')):
    parse_file(rdd_file, SiteDict, i + 1)
    sys.stderr.write('{} file, Rep{} done parsing\n'.format(rdd_file, i+1))

print strftime("%a, %d %b %Y %H:%M:%S\t"), "Sites stored to dict"
 

min_Coverage = int(min_Coverage)
mat2 = open(out_file.replace('.tab', '.no_batch_mean.both_rep_cov.tab'), 'w')
mat2.write('Site_ID\tMeanRatio\tMeanCov\n') 

for (chrm, et), posDict in SiteDict.items():
	for pos, RepDict in posDict.items():
		if 1 in RepDict.keys() and 2 in RepDict.keys():
			ratio1, cov1 = RepDict[1]
			ratio2, cov2 = RepDict[2]
		else:
			continue
		Mean_Coverage = np.mean([cov1, cov2])
		if cov1 > min_Coverage and cov2 > min_Coverage:
			siteID  = ':'.join((chrm, pos, et))
			MeanRatio = np.mean([ratio1, ratio2])
			outline2 = [siteID, MeanRatio, Mean_Coverage]
			mat2.write('\t'.join(map(str, outline2)) + '\n')
	print strftime("%a, %d %b %Y %H:%M:%S\t"), chrm, et, "DONE!"
mat2.close()

		



