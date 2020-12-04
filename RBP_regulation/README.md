# Regulation of RNA editing by RNA-binding proteins (RBP)

In reference to the Manuscript [Quinones et al. Comm. Bio. 2019](https://www.nature.com/articles/s42003-018-0271-8)

# Contents 
- Summary files: Lists of Differentially Edited (DE) sites found in our study. Further description of 
  these files is provided in the [Summary files description](./README_Summary_files) files. 
  - [Differentially edited sites in HepG2](./Summary.all_de_sites.all_rbps.HepG2.new_fdr_corr.final.header.tab)
  - [Differentially edited sites in K562](./Summary.all_de_sites.all_rbps.HepG2.new_fdr_corr.final.header.tab)
- data: [Data folder](./data)Folder containing sample data that can be processed by our pipeline. 
- pipeline scripts: Python (.py) and R (.r) scripts that run the differential editing analysis. Further 
  description of the scripts and arguments is provided in the 'README_DE_pipeline.txt' file.
- wrapper scripts: Bash (.sh) scripts that run the pipeline scripts. 

# Systems requirements
- Python: Python version 2.7.12 was used. The Python scripts require the following non-standard 
  packages:
  - Numpy 
  - rpy2.robjects.packages
  - rpy2.robjects.vectors
- R: R version 2.15 was used. The R scripts uses the following non-standard packages:
  - ggplot2
- Bash: Unix-based operating systems are required to run the wrappers (.sh) 
  
# Installation guide
There is no need to install or compile the scripts in this repository. 

# Demo
The wrapper scripts (.sh) contain the parameters and file names from the 'data' directory
and are ready to be ran. If the 'data' folder is in the directory as the wrapper scripts simply run:
```
bash submit.training_and_testing_matrix.sh  

bash submit.testing_batch_mean.sh

bash submit.regression_and_prediction.sh
```

After running the third bash script, you should obtain the final output files:
- data/MATRIX_2.all_editing_sites.HepG2_ADAR.minCov_5.with_batch_mean.both_rep_cov.out.fdr_corr.txt
- data/MATRIX_2.all_editing_sites.HepG2_DHX30.minCov_5.with_batch_mean.both_rep_cov.out.fdr_corr.txt

corresponding to the list of DE sites from ADAR-KD and DHX30-KD respectively

# Instructions for use
After having identified high-confidence editing sites, write down their coordinates, editing type, 
and read count as shown in the demo input sample files. 
These scripts do not require great memory allocations or prolonged runtime, therefore the editing sites
from a single RNA-Seq experiment (10^4 to 10^5 editing sites) can be run on a standar desktop computer. 
In average, the run time is less than 10 minutes. 

