# Pipeline description (Differential editing calculation)
Here, we describe the steps used to identify differentially edited sites. Our approach to call differentially-edited sites is adapted from the BEAPR package [Yang et al.](https://www.nature.com/articles/s41467-019-09292-w).

After obtaining highly-confident editing sites using the GIREMI method ([Lee et al. 2013](https://rnajournal.cshlp.org/content/19/6/725.long), [Zhang et al. 2015](https://www.nature.com/articles/nmeth.3314)), we generate a text files that contains all the editing sites in the format:
```
Chromosome, Coordinate, Reference Base, Number of edited reads, Total number of reads
```
(e.g.  [input file](./data/editing_sites.ADAR_Rep1.txt))

We then use the following steps to calculate differential editing from these files:


## Systems requirements
- Python: Python version 2.7.12 was used. The Python scripts require the following non-standard packages:
  - Numpy 
  - rpy2.robjects.packages
  - rpy2.robjects.vectors
- R: R version 2.15 was used. The R scripts uses the following non-standard packages:
  - ggplot2
- Bash: Unix-based operating systems are required to run the wrappers (.sh) 
  
## Installation guide
There is no need to install or compile the scripts in this repository. 


## Instructions for use
After having identified high-confidence editing sites, write down their coordinates, editing type, and read count as shown in the demo input sample files. 
These scripts do not require great memory allocations or prolonged runtime, therefore the editing sites from a single RNA-Seq experiment (10^4 to 10^5 editing sites) can be run on a standar desktop computer. In average, the run time is less than 10 minutes. 

## 1) Obtain data matrices
The script: *submit.training_and_testing_matrix.sh* is used to obtain training matrices from the control samples
```
python pipeline.make_matrix_1.py <input_files> <min_Coverage> <train_matrix_file_batch1>
```
Subsequently, run the following command to obtain testing matrices from all samples. 
```
python pipeline.make_matrix_2.py <input_files> <min_Coverage> <test_matrix_file1_batch1>
```
The testing matrices are still incomplete at this point. They need to include the batch average editing level of the sites.
        
The <input_files> is a list of coma-separated files corresponding to all the replicates from one sample. Example input files are provided e.g.:
- [Editing sites from ADAR-KD (Rep1)](./data/editing_sites.ADAR_Rep1.txt).
- [Editing sites from ADAR-KD (Rep2)](./data/editing_sites.ADAR_Rep2.txt)
    

## 2) Obtain batch means
The script *submit.testing_batch_mean.sh* runs the python script: 
```
python pipeline.get_batch_means.py <test_matrix_file1_batch1,test_matrix_file2_batch1> <test_matrix_all_batch_files_means>
```
which obtains the average editing level of an editing site in a batch. 
    
    
## 3) Run the regression and predict differential editing

The script: *submit.regression_and_prediction.sh* runs the following python scripts:
```
python pipeline.make_matrix_3.py <test_matrix_file1_batch1> <test_matrix_all_batch_files_means> <final_test_matrix_file1_batch1>
```
It completes the testing matrices by including the batch editing level means to the testing matrices from step 1.
Then, it runs the command:
```    
Rscript pipeline.Reg.r <train_matrix_file_batch1> <final_test_matrix_file1_batch1> <regression_file1_batch1>
````
Which obtains a regression of the expected variance for different coverages levels.
It takes as input training matrices from step1 and testing matrices from step 3)
```    
Rscript pipeline.Pred.r <regression_file1_batch1> <prediction_file1_batch1> <n>
```
It predicts the significance of an editing level change KD vs batch mean based on the aforementioned regression. 
    

## 4) Adjust p-value for multiple testing:
    
The command:
```
python pipeline.parse_editing_files.py <prediction_file1_batch1> <prediction_file1_batch1_p-val_corrected>
```
will adjust the p-values obtained from the last step and adjust them using Benjamin-Hochberg p-value correction and will label the sites as "DE" for differentially editing or "NS" for non-significant or non-differentially edited.


# Test Run
To test the pipeline, simply download the main scripts (.py and .r), wrappers (.sh), the input files from the 'data' directory and the 'batch.job' file. 
The wrapper scripts already include the filenames and parameters and are ready to run the input sample from the 'data' folder. 
```
bash submit.training_and_testing_matrix.sh  

bash submit.testing_batch_mean.sh

bash submit.regression_and_prediction.sh
```
After running the third bash script, you should obtain the final output files:

- data/MATRIX_2.all_editing_sites.HepG2_ADAR.minCov_5.with_batch_mean.both_rep_cov.out.fdr_corr.txt
- data/MATRIX_2.all_editing_sites.HepG2_DHX30.minCov_5.with_batch_mean.both_rep_cov.out.fdr_corr.txt

corresponding to the list of DE sites from ADAR-KD and DHX30-KD respectively
Make sure to modify cluster parameters (e.g. memory requirements, time allocation, etc)


# References
1. Lee, J.-H., Ang, J. K. & Xiao, X. Analysis and design of RNA sequencing experiments for identifying RNA editing and other single-nucleotide variants. RNA 19, 725–732 (2013).
2. Zhang, Q. & Xiao, X. Genome sequence-independent identification of RNA editing sites. Nat. Methods 12, 347–350 (2015)
3. Yang, E.-W. et al. Allele-specific binding of RNA-binding proteins reveals functional genetic variants in the RNA. bioRxiv 396275 (2018). doi:10.1101/396275
