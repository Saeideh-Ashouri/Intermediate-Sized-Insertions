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
$sh 01-process_IMSindel_results.sh <path-to-input-folder> <samples-name-file> <path-to-output-files>

The other shell script, "02-generate_high_confidence_insertions.sh", merges insertion candidates based on their positions in the genome. Then, it annotates them for genic regions as well as repetitive regions of the genome and filters out false-positive insertion candidates based on their annotations. To use this shell script, place required annotation files in the requred_files directory and type the following command:     

<path-to-processed-list-of-insertions-from-previous-step> <path-to-desired-output-folder> 
$sh 02-generate_high_confidence_insertions.sh <path-to-processed-list-of-insertions-from-previous-step>   
  
-------------------------------------------------------

Output files from each step:

  
