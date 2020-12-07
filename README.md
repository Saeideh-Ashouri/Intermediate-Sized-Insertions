# Processing the list of intermediate-sized insertion calls
This is a workflow for processing the list of intermediate-sized insertions called by IMSindel software.
------------------------------------

Required softwares:   
IMSindel (https://github.com/NCGG-MGC/IMSindel)   
R (ver. 3.5.1 or higher)    
Python (ver. 3.4 or higher)   
NumPy module for python   

Input files:    
*.out file from insertion calling using IMSindel    

Before getting started, please prepare the following files:   
Annotation file used for annotating insertions for genes and exons can be downloaded from the UCSC genome browser database (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. Ensure group="Genes and Gene Predictions"; track="NCBI RefSeq"; table="UCSC RefSeq (refGene)"; assembly="Feb.2009 (GRCh37/hg19)". Plesae rename the file to "hg19_genes_ucsc.txt" and place it in the "required_files" directory.  
Annotation file used for annotating insertions for simple repeats can be downloaded from the UCSC genome browser site (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. Ensure group="Repeats"; track="Simple Repeats"; assembly="Feb.2009 (GRCh37/hg19)". Please rename the file to "hg19_simple_repeats_ucsc.txt" and place it in the "required_files" directory.    
Annotation file used for annotating insertions for reeat maskers can be downloaded from the UCSC genome browser site (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. Ensure group="Repeats"; track="RepeatMasker"; assembly="Feb.2009 (GRCh37/hg19)". Please rename the file to "hg19_repeatmasker_ucsc.txt" and place it in the "required_files" directory.    

This file can be downloaded from the UCSC genome browser site (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. )".Ensure group="Repeats"; track="RepeatMasker"; assembly="Feb.2009 (GRCh37/hg19
4. hg19_telomere_centromere.txt

This file is provided. The file is modified after the original data was downloaded from the UCSC genome browser site (https://genome.ucsc.edu/index.html) using the Table Browser utility tool, with group="All Tables"; database=hg19; table="gap".
5. hg19_repeatmasker_ucsc_BED.txt

This file is provided as a .zip file. The file is modified from the "hg19_repeatmasker_ucsc.txt" file. Please expand the file before use.
6. bam_files_locations.txt

Prepare a tab-delimited text file containing sample names and locations of the corresponding .bam files of the samples. First column should contain the sample name (e.g. "Sample1"), followed by the location of the .bam file in the second column (e.g. "/path/to/directory/containing/Sample1.bam").

Ensure that both .bam and .bai index files are located in the same directory/location. Name the file "bam_files_locations.txt" and place into "required_files" directory.

Note: The "bam_files_locations.txt" file provided here is only a placeholder file as an example of the file format.
The .bam files listed (together with the .bai files) can be obtained from the 1000Genomes Projects ftp server from the URLs listed in the example file.
Please provide a file that corresponds to your own data should you wish to process your own samples!

Example files:

Example files for a number of samples from the 1000Genome Project are provided in the directory "Example_files".
These files were produced from the outputs of indel calling using IMSindel software and processing the individual output files (as per the script <process_IMSindel_results.sh>) and extracting information for chromosome 21.
Please use these files if you would like to test the <generate_high_confidence_deletions.sh> script.
