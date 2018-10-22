#!/usr/bin/python
import sys
from collections import defaultdict
import numpy as np

### Write matrix to train the regression model
### We select sites from control samples.
### It includes the coordinates of the editing site, mean coverage, mean editing ratio, and variance of the editing ratio


       
def parse_file(ff, dic, Rep):
	'''
	Obtain read count and coverage for every site
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



RDD_file_reps, minCov, out_file = sys.argv[1:4]
minCov = int(minCov)

RDD_file_reps = RDD_file_reps.strip(',')
SiteDict = defaultdict(dict)
for i, rdd_file in enumerate(RDD_file_reps.split(',')):
    parse_file(rdd_file, SiteDict, i + 1)
    sys.stderr.write('{} file, Rep{} done parsing\n'.format(rdd_file, i+1))

mat1 = open(out_file, 'w')
mat1.write('Site_ID\tMean_Coverage\tVar_Ratio\tMean_Ratio\n')


for (chrm, et), posDict in SiteDict.items():
	for pos, RepDict in posDict.items():
		if 1 in RepDict.keys() and 2 in RepDict.keys():
			ratio1, cov1 = RepDict[1]
			ratio2, cov2 = RepDict[2]
		else:
			continue
		Mean_Coverage = np.mean([cov1, cov2])
		Var_Editing_Ratio = np.var([ratio1, ratio2])
		Mean_Editing_Ratio = np.mean([ratio1, ratio2])
		siteID = '{}:{}:{}'.format(chrm, pos, et)
		### Select sites with a Min. Mean Cov. and with Mean editing ratio of 0.1
		if Mean_Coverage >= minCov and np.mean([ratio1, ratio2]) >= 0.1:
			outline1 = [siteID, Mean_Coverage, Var_Editing_Ratio, Mean_Editing_Ratio]	
			mat1.write('\t'.join(map(str, outline1)) + '\n')

sys.stderr.write('DONE! output file:{} \n'.format(out_file))

mat1.close()

		



