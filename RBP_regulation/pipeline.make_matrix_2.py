#!/usr/bin/python
import sys
from collections import defaultdict
import numpy as np
from time import strftime


### Write matrix to test the regression model
### One matrix per RBP-KD per cell line.
### It includes the coordinates of the editing site, mean coverage, and mean editing ratio


def parse_file(ff, dic, editing_type, Rep):
	'''
	Obtain read coverage and editing ratio for every site
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
	batches = {}
	with open("all_rbps_info.tab") as FF:
		for line in FF:
			cell, rbp, acc, batch = line.split()[:4]
			if rbp.startswith('CONTROL'):
				batches[(cell, rbp)] = rbp
			else:
				batches[(cell, rbp)] = batch	
	return batches



print strftime("%a, %d %b %Y %H:%M:%S\t"), "Script starts"
cell, rbp, min_Coverage, out_file = sys.argv[1:5]

SiteDict = more_sites(cell, rbp)
print strftime("%a, %d %b %Y %H:%M:%S\t"), "Sites from RDD pipeline converted to dict"
 

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

		



