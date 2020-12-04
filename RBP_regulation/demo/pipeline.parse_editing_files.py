#!/usr/bin/python
import sys
from collections import defaultdict
from glob import glob
from os import path 

from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

stats = importr('stats')

SiteFile, OutputFile = sys.argv[1:3]

out = open(OutputFile, 'w')


outlines = {}
pval_adj = {}

with open(SiteFile) as SF:
	next(SF)
	for line in SF:
		L = line.split()
		SiteID, Mean_Coverage, Obs_Ratio, Batch_Ratio, exp_std, ABS, pval, gene, region, alu, batch = L
		Mean_Coverage, Obs_Ratio, Batch_Ratio, pval = map(float, [Mean_Coverage, Obs_Ratio, Batch_Ratio, pval])
		chrom, pos, et = SiteID.split(':')
		et = et[0] + et[5]
		sig = "NA"
		outline = [SiteID, sig, et, Obs_Ratio, Batch_Ratio, Mean_Coverage, 20, pval, gene, region, alu, batch]
		abs_dER = abs(Obs_Ratio - Batch_Ratio)
		outlines[SiteID] = outline
		if abs_dER > 0.05: 
			pval_adj[SiteID] = pval

if len(pval_adj) > 0:
	k_sites, pvals = zip(*pval_adj.items())
	p_adjust = stats.p_adjust(FloatVector(pvals), method = 'BH')
	pval_adj = dict(zip(k_sites, list(p_adjust)))
else:
	pval_adj = {}

for ksite, outline in outlines.items():
	if ksite in pval_adj.keys():
		fdr = pval_adj[ksite]
		if fdr <= 0.1:
			outline[1] = "DE"
		else:
			outline[1] = "NS"
	else:
		fdr = 'NA'
		outline[1] = "NS"
	outline.append(fdr) 	
	out.write('\t'.join(map(str, outline)) + '\n')
out.close() 
			


		

