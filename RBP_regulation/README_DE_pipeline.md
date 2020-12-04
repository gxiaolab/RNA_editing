After obtaining highly-confident editing sites using the GIREMI method ([Lee et al. 2013](https://rnajournal.cshlp.org/content/19/6/725.long), [Zhang et al. 2015](https://www.nature.com/articles/nmeth.3314)), we generate a text file that contains all the editing sites in the format:
```
Chromosome, Coordinate, Reference Base, Number of edited reads, Total number of reads
```
Our approach to call differentially-edited sites is adapted from the BEAPR package [Yang et al.](https://www.nature.com/articles/s41467-019-09292-w).
We then use the following steps to calculate differential editing from these 
files:


## 1) Obtain data matrices

    The script: *submit.training_and_testing_matrix.sh* is used to obtain training matrices from the control samples
    ```
    python pipeline.make_matrix_1.py <input_files> <min_Coverage> <train_matrix_file>
    ```
    Subsequently, run the following command to obtain testing matrices from all samples. 
    ```
    python pipeline.make_matrix_2.py <input_files> <min_Coverage> <test_matrix_file>
    ```
    The testing matrices are still incomplete at this point. They need to include the batch average editing level of the sites.
        
    The <input_files> is a list of coma-separated files corresponding to all the replicates from one sample. Example input files are provided e.g.:
    - [Editing sites from ADAR-KD (Rep1)](./data/editing_sites.ADAR_Rep1.txt).
    - [Editing sites from ADAR-KD (Rep2)](./data/editing_sites.ADAR_Rep2.txt)
    

## 2) Obtain batch means

    The script *submit.testing_batch_mean.sh* runs the python script: 
    ```
    python pipeline.get_batch_means.py <test_matrix_file1,test_matrix_file2,test_matrix_file3> <test_matrix_all_batch_files_means>
    ```
    which obtains the average editing level of an editing site in a batch. 
    
    
## 3) Run the regression and predict differential editing

    The script: *submit.regression_and_prediction.sh* runs the following python scripts:
    ```
    python pipeline.make_matrix_3.py $input_file $batch_means $final_test_file
    ```
    (Completes the testing matrices by including the batch editing level means
    to the testing matrices from step 1)
    
    Rscript pipeline.Reg.r $train_matrix $final_test_matrix $Reg_file
    (Obtains a regression of the expected variance for different coverages levels.
    It takes as input training matrices from step1 and testing matrices from step 3)
    
    Rscript pipeline.Pred.r $Reg_file $Pred_file $number_of_reps
    (Predicts the significance of an editing level change KD vs batch mean based on 
    the aforementioned regression. Takes as input the regression file from the previous
    command)
    

## 4) Adjust p-value for multiple testing:
    
    The script:
    
    python pipeline.parse_editing_files.py $Pred_file $Pred_file.corr
    
    will adjust the p-values obtained from the last step and adjust them using 
    Benjamin-Hochberg p-value correction and will label the sites as "DE" for 
    differentially editing or "NS" for non-significant or non-differentially edited.


To test the pipeline, simply download the main scripts (.py and .r), wrappers (.sh), the 
input files from the 'data' directory and the 'batch.job' file. The wrapper scripts already
include the filenames and parameters and ready to run the input sample from the 'data' folder. 

Make sure to modify cluster parameters (e.g. memory requirements, time allocation, etc)


References:
1. Lee, J.-H., Ang, J. K. & Xiao, X. Analysis and design of RNA sequencing experiments for identifying RNA editing and other single-nucleotide variants. RNA 19, 725–732 (2013).
2. Zhang, Q. & Xiao, X. Genome sequence-independent identification of RNA editing sites. Nat. Methods 12, 347–350 (2015)
3. Yang, E.-W. et al. Allele-specific binding of RNA-binding proteins reveals functional genetic variants in the RNA. bioRxiv 396275 (2018). doi:10.1101/396275
