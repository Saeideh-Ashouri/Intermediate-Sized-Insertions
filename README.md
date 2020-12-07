# Processing the list of intermediate-sized insertion calls
This is a workflow for processing the list of intermediate-sized insertions called by IMSindel software.
------------------------------------

Required softwares:   
IMSindel (https://github.com/NCGG-MGC/IMSindel)   
R (ver. 3.5.1 or higher)    
Python (ver. 3.4 or higher)   
NumPy module for python   

------------------------------------    

Input files:    
*.out file from insertion calling using IMSindel    

Before getting started, please prepare the following files:   

Annotation file used for annotating insertions for genes and exons can be downloaded from the UCSC genome browser database (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. Ensure group="Genes and Gene Predictions"; track="NCBI RefSeq"; table="UCSC RefSeq (refGene)"; assembly="Feb.2009 (GRCh37/hg19)". Plesae rename the file to "hg19_genes_ucsc.txt" and place it in the "required_files" directory.   

The annotation file used for annotating insertions for genome microsatellites is an in-house reference which can be provided upon your request. 

Annotation file used for annotating insertions for simple repeats can be downloaded from the UCSC genome browser site (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. Ensure group="Repeats"; track="Simple Repeats"; assembly="Feb.2009 (GRCh37/hg19)". Please rename the file to "hg19_simple_repeats_ucsc.txt" and place it in the "required_files" directory.    

Annotation file used for annotating insertions for repeat maskers can be downloaded from the UCSC genome browser site (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. Ensure group="Repeats"; track="RepeatMasker"; assembly="Feb.2009 (GRCh37/hg19)". Please rename the file to "hg19_repeatmasker_ucsc.txt" and place it in the "required_files" directory.   

Annotation file used for annotating insertions for centromeres and telomeres is provided in the required_files folder in this repository. This file was modified after downloading from the UCSC genome browser site (https://genome.ucsc.edu/index.html) using the Table Browser utility tool, with group="All Tables"; database=hg19; table="gap".    

----------------------------------------
How to use the scripts:

The shell script "01-process_IMSindel_results.sh", is used for processing and concatenating the list of insertions called by IMSindel software. Before using this script, please place output files from each sample in a subfolder in your input folder. Please name each subfolder same as the sample name. Please provide a list of samples in a file with each sample name in a row and name it "samples". By running this script, outpt files of each sample will be concatenated in a single file, very short each sample's name will be inserted in it, and chromosomal location will be added for each insertion. To use this shell script, type the code below:    
$sh 01-process_IMSindel_results.sh {path-to-input-folder} {path-to-output-files} {samples-name-file}

The other shell script, "02-generate_high_confidence_insertions.sh", merges insertion candidates based on their positions in the genome. Then, it annotates them for genic regions as well as repetitive regions of the genome and filters out false-positive insertion candidates based on their annotations. To use this shell script, place required annotation files in the requred_files directory and type the following command:   
$sh 02-generate_high_confidence_insertions.sh {path-to-the-processed-list-of-insertions-from-previous-step} {path-to-desired-output-folder}  
  
-----------------------------------------

Output files:   
The following file will be output for each sample from the <01-process_IMSindel_results.sh> script:
*sample_name.overall.insertions:    
This file contains the insertions extracted from the results of running IMSindel for each sample. Columns are tab-separated.    
"sample_name" column consists of the sample name as specified when making the overall concatenated file.
"contig" column shows the contig in which the insertion was called from, during IMSindel calling.
"sttpos" and "endpos" show the insertion position.
"chromosome" column shows the chromosome on which the insertion is located.
Both "stt_pos" and "end_pos" show the insertion position.
All other columns are outputs from IMSindel.

-----------------------------------------

Configuration file:   
The parameters provided in the config file could be changed based on your preference.   
1) merge_insertions_positions_difference: This parameter identifies the difference in insertions position (in base pair) based on which the insertions are merged and considered as one insertion in different samples. The default value is 10.   
2) annotation_flank: This parameter specifies the flanking regions on both sides of insertion position for which the annotation of simple repeats and repeat masker elements is conducted. The default value is 100.    
3) confident_ins_num_threshold: This parameter shows the minimum number of samples with sufficient number of support reads for a cofident insertion call. The default value is 2.
4) ins_sup_reads_threshold: The minimum number of support reads for a confident insertion call. The default value is 5. 
5) ins_len_filter_threshold: The insertion length threshold for filtering out short insertions. As IMSindel does not report the full length of insertions, it is recommended to keep this value as low as possible to ensure that less insertions are excluded. The default value is 20.    
6) total_reads: The threshold of total reads for filtering out possibly false positive insertions. The default value is 10.   
7) variant_allele_frequency: This is the variant allele frequency defined as the proportion of support reads to total reads for each insertion. Insertions with variant allele frequency less than this value are filtered out. The default value is 0.1.   
8) HWE_exclusion_threshold: The threshold for Hardy-Weinberg p-value threshold. Insertions with p-values less than this will be excluded from the data. The default value is 0.0001.
9) allele_frequency_exclusion_threshold: The insertions allele frequency threshold. Insertions with allele frequency less than this threshold will be excluded from the data. The default value is 0.05.
10) reference: Source of reference used for the sequencing data. Value should be a string describing the reference source (e.g. NCBI37).    
11) assembly: Source of genome assembly used for the sequencing data. Value should be a string describing the assembly (e.g.ncbi_build37.fa).   

----------------------------------------------

Contact: Saeideh Ashouri (saeede_ashoori@yahoo.com)
