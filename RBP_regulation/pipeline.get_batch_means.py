#!/usr/bin/bash
import sys
from collections import defaultdict 
from glob import glob
import os
import numpy as np 


### Calculate the mean editing ratio per
### site per batch


def get_batches():
	batches = defaultdict(list)
	g = open("batch.job")
	for line in g:
		CELL, rbp, control = line.split()[:3]
		if rbp.startswith("CONTROL"):
			batches[rbp].append(rbp)
		else:
			batches[control].append(rbp)
	g.close()
	return batches


cell, batch = sys.argv[1:3]

batches = get_batches()

NA = "NA"
cov_cutoff = 0.5



outfile = "data/BATCH_MEAN.{}_{}.by_rep.both_rep_cov.txt".format(cell, batch)	
out = open(outfile, 'w')	

rbplist = batches[batch]
batch_N = len(rbplist)

if batch_N > 2:
	batch_means = defaultdict(dict)
	for rbp in rbplist:
		ff = "data/MATRIX_2.all_editing_sites.{}_{}.minCov_5.no_batch_mean.both_rep_cov.tab".format(cell, rbp)
		f = open(ff)
		next(f)
		for line in f:
			L = line.split()
			mean_ratio, mean_cov = map(float, L[1:3])
			chrm, pos, et = L[0].split(':')
			posbin = (chrm, pos[:3])
			ksite = L[0]
			try: 
				batch_means[posbin][ksite].append(mean_ratio)
			except: 
				batch_means[posbin][ksite] = [mean_ratio]
		f.close()
		print rbp, 'in', batch, 'done processing ....'
else:
	batch_means = defaultdict(dict)
	ff = "data/MATRIX_2.all_editing_sites.{}_{}.minCov_5.no_batch_mean.tab".format(cell, batch)
	f = open(ff)
	next(f)
	for line in f:
		L = line.split()
		mean_ratio, mean_cov = map(float, L[1:3])
		chrm, pos, et = L[0].split(':')
		posbin = (chrm, pos[:3])
		ksite = L[0]
		batch_means[posbin][ksite] = [mean_ratio]
	f.close()

print "Batch means {} done".format(batch)

for posbin, sitedict in batch_means.items():
	for ksite, ratios_list in sitedict.items():
		testable_n = len(ratios_list)
		testable_fraction = testable_n/float(batch_N)
		if testable_fraction >= cov_cutoff:
			batch_mean = np.mean( ratios_list )
		else:
			batch_mean = NA
		outline = [ksite, batch_mean, '.', '.', '.', batch]
		out.write('\t'.join(map(str, outline)) + '\n')
print "File writting {} done".format(batch)
    	
out.close()






