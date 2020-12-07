# Processing the list of intermediate-sized insertion calls
This is a workflow for processing the list of intermediate-sized insertions called by IMSindel software.
------------------------------------

Required softwares:   
IMSindel (https://github.com/NCGG-MGC/IMSindel)   
R (ver. 3.5.1 or higher)    
Python (ver. 3.4 or higher)   
NumPy module for python   
::::::::::::::::::::::::::::::::::::::
Input files:    
*.out file from insertion calling using IMSindel    

Before getting started, please prepare the following files:   

Annotation file used for annotating insertions for genes and exons can be downloaded from the UCSC genome browser database (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. Ensure group="Genes and Gene Predictions"; track="NCBI RefSeq"; table="UCSC RefSeq (refGene)"; assembly="Feb.2009 (GRCh37/hg19)". Plesae rename the file to "hg19_genes_ucsc.txt" and place it in the "required_files" directory.   

The annotation file used for annotating insertions for genome microsatellites is an in-house reference which can be provided upon your request. 

Annotation file used for annotating insertions for simple repeats can be downloaded from the UCSC genome browser site (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. Ensure group="Repeats"; track="Simple Repeats"; assembly="Feb.2009 (GRCh37/hg19)". Please rename the file to "hg19_simple_repeats_ucsc.txt" and place it in the "required_files" directory.    

Annotation file used for annotating insertions for repeat maskers can be downloaded from the UCSC genome browser site (https://genome.ucsc.edu/index.html) under the Table Browser utility tool. Ensure group="Repeats"; track="RepeatMasker"; assembly="Feb.2009 (GRCh37/hg19)". Please rename the file to "hg19_repeatmasker_ucsc.txt" and place it in the "required_files" directory.   

Annotation file used for annotating insertions for centromeres and telomeres is provided in the required_files folder in this repository. This file was modified after downloading from the UCSC genome browser site (https://genome.ucsc.edu/index.html) using the Table Browser utility tool, with group="All Tables"; database=hg19; table="gap".
