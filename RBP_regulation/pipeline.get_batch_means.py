#!/usr/bin/bash
import sys
from collections import defaultdict 
from glob import glob
import os
import numpy as np 


### Calculate the mean editing ratio per
### site per batch

batch_files, outfile = sys.argv[1:3]

NA = "NA"
cov_cutoff = 0.5

	

batch_files = batch_files.strip(',').split(',')

batch_N = len(batch_files)


if batch_N > 2:
	batch_means = defaultdict(dict)
	for ff in batch_files:
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
else:
	batch_means = defaultdict(dict)
	ff = batch_files[0]
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


out = open(outfile, 'w')

for posbin, sitedict in batch_means.items():
	for ksite, ratios_list in sitedict.items():
		testable_n = len(ratios_list)
		testable_fraction = testable_n/float(batch_N)
		if testable_fraction >= cov_cutoff:
			batch_mean = np.mean( ratios_list )
		else:
			batch_mean = NA
		outline = [ksite, batch_mean, '.', '.', '.', '.']
		out.write('\t'.join(map(str, outline)) + '\n')
print "Batch means obtained"
out.close()






