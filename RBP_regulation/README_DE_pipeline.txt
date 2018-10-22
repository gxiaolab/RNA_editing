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

2) Obtain batch means

    The script submit.testing_batch_mean.sh runs the python script: 
    pipeline.get_batch_means.py which obtains the average editing level of an
    editing site in a batch. 

3) Run the regression and predict differential editing

    The script: submit.regression_and_prediction.sh runs the following python
    scripts:
    - pipeline.make_matrix_3.py: Completes the testing matrices by including 
        the batch editing level means.
    - pipeline.Reg.r: Obtains a regression of the expected variance for 
        different coverages levels.
    - pipeline.Pred.r: Predicts the significance of an editing level change 
        (KD vs batch mean) based on the aforementioned regression. 

4) Adjust p-value for multiple testing:
    
    The script: pipeline.parse_editing_files.py will adjust the p-values 
    obtained from the last step and adjust them using Benjamin-Hochberg 
    p-value correction and will label the sites as "DE" for differentially
    editing or "NS" for non-significant or non-differentially edited.


The file: all_rbps_info.tab contains the name of all the RBPs with their 
respective batch name in HepG2 and K562 cell

References:
1. Lee, J.-H., Ang, J. K. & Xiao, X. Analysis and design of RNA sequencing experiments for identifying RNA editing and other single-nucleotide variants. RNA 19, 725–732 (2013).
2. Zhang, Q. & Xiao, X. Genome sequence-independent identification of RNA editing sites. Nat. Methods 12, 347–350 (2015)

