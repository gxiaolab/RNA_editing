#!/usr/bin/python
import sys
from collections import defaultdict
import numpy as np

### Write matrix to train the regression model
### We select sites from control samples.
### It includes the coordinates of the editing site, mean coverage, mean editing ratio, and variance of the editing ratio


       
def parse_file(ff, dic, editing_type, Rep):
	'''
	Obtain read count and coverage for every site
	'''
	f = open(ff)
	for line in f:
		l = line.split()
		chrm, pos, ref, edited_reads, total_reads = l[:5]
		edited_reads, total_reads = map(int, (edited_reads, total_reads))
		ratio = edited_reads/float(total_reads)
		key = (chrm, editing_type)
		try:
			dic[key][pos][Rep] = [ratio, total_reads]
		except:
			dic[key][pos] = {Rep : [ratio, total_reads]}
	f.close()


def more_sites(cell, rbp):
	'''
	Parse through the RDD files
	'''
	sites = defaultdict(dict)
	nts = ['A','G','T','C']
	editing_types = [x + '.to.' + y for x in nts for y in nts if x != y]
	chromosomes   = ['chr' + str(z) for z in range(1,23) + ['X', 'Y']]
    ### Location of RDD files:
	gx_dir = '/home/gxxiao/projects/u87/editing/newdata.gang/final.scripts/ss/editout.encode.{0}.sep.rep/{1}/{1}'.format(cell.lower(), rbp)
    '''
    RDD files are split by replicate, by chromosome, and by editing type
    '''
	for editing_type in editing_types:
		for chrm in chromosomes:
			for Rep in (1, 2):
				rbp_file_non_zero = '{0}_Rep{1}.{2}.{3}.readpos.0.dist2end.1.txt'.format(gx_dir, Rep, chrm, editing_type)
				rbp_file_zero = rbp_file_non_zero.replace('.txt', '.sites.with.no.edits.txt')
				for edit_file in (rbp_file_non_zero, rbp_file_zero):
					parse_file(edit_file, sites, editing_type, Rep)
	return sites


def get_batch_info():
	batches = defaultdict(list)
	with open("all_rbps_info.tab") as FF:
		for line in FF:
			cell, rbp, acc, batch = line.split()[:4]
			if rbp.startswith('CONTROL'):
				batches[rbp].append( rbp )
			else:
				batches[batch].append( rbp )	
	return batches


cell, control, minCov, out_file = sys.argv[1:5]
batches = get_batch_info()
minCov = int(minCov)

mat1 = open(out_file, 'w')
mat1.write('Site_ID\tMean_Coverage\tVar_Ratio\tMean_Ratio\n')

if control in batches.keys():
	SiteDict = more_sites(cell, control)
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
			siteID = '{}:{}:{}:{}'.format(chrm, pos, et, control)
			### Select sites with a Min. Mean Cov. and with Mean editing ratio of 0.1
			if Mean_Coverage >= minCov and np.mean([ratio1, ratio2]) >= 0.1:
				outline1 = [siteID, Mean_Coverage, Var_Editing_Ratio, Mean_Editing_Ratio]	
				mat1.write('\t'.join(map(str, outline1)) + '\n')
mat1.close()

		



