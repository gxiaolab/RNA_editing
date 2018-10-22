After obtaining highly-confident editing sites using the GIREMI method [1][2], 
we generate a text file that contains all the editing sites in the format:"

Chromosome, Coordinate, Ref.Base, Number_of_edited_reads, Total_number_of_reads

We then use the following steps to calculate differential editing from these 
files:


1) Obtain data matrices

    The script: submit.training_and_testing_matrix.sh runs the python scripts:
    - pipeline.make_matrix_1.py: Writes matrices for training the regression
        model. Uses only control samples. 
    - pipeline.make_matrix_2.py: Write data matrices testing the regression 
        model respectively. The testing matrices are still incomplete at this 
        point. They need to include the batch average editing level of the sites.
        Uses all samples.
    In the 'submit.training_and_testing_matrix.sh' runs the followfing command:
    
    python pipeline.make_matrix_1.py $input_file $min_Coverage $train_matrix
    (to obtain training data from control samples) and
    
    python pipeline.make_matrix_2.py $input_file $min_Coverage $test_matrix
    (to obtain testing data from all samples) 
        
    Example input files are provided in the 'data' folder with the name
    'editing_sites.*.txt'
    

2) Obtain batch means

    The script: submit.testing_batch_mean.sh runs the python script: 
    pipeline.get_batch_means.py which obtains the average editing level of an 
    editing site in a batch. The following command obtains the average
    editing level for every site:
    
    python pipeline.get_batch_means.py $batch_test_files $batch_means
    
    the $batch_test_files is a coma-separated list of files obtained from step1 
    (testing matrices)
    
    
3) Run the regression and predict differential editing

    The script: submit.regression_and_prediction.sh runs the following python
    scripts:
    
    python pipeline.make_matrix_3.py $input_file $batch_means $final_test_file
    (Completes the testing matrices by including the batch editing level means
    to the testing matrices from step 1)
    
    Rscript pipeline.Reg.r $train_matrix $final_test_matrix $Reg_file
    (Obtains a regression of the expected variance for different coverages levels.
    It takes as input training matrices from step1 and testing matrices from step 3)
    
    Rscript pipeline.Pred.r $Reg_file $Pred_file $number_of_reps
    (Predicts the significance of an editing level change KD vs batch mean based on 
    the aforementioned regression. Takes as input the regression file from the previous
    command)
    

4) Adjust p-value for multiple testing:
    
    The script:
    
    python pipeline.parse_editing_files.py $Pred_file $Pred_file.corr
    
    will adjust the p-values obtained from the last step and adjust them using 
    Benjamin-Hochberg p-value correction and will label the sites as "DE" for 
    differentially editing or "NS" for non-significant or non-differentially edited.


To test the pipeline, simply download the main scripts (.py and .r), wrappers (.sh), the 
input files from the 'data' directory and the 'batch.job' file. The wrapper scripts already
include the filenames and parameters. 

Make sure to modify cluster parameters (e.g. memory requirements, time allocation, etc)


References:
1. Lee, J.-H., Ang, J. K. & Xiao, X. Analysis and design of RNA sequencing experiments for identifying RNA editing and other single-nucleotide variants. RNA 19, 725–732 (2013).
2. Zhang, Q. & Xiao, X. Genome sequence-independent identification of RNA editing sites. Nat. Methods 12, 347–350 (2015)

