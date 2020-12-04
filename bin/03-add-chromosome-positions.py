import sys

contig_file = open(sys.argv[1])
insertions = open(sys.argv[2])
list_1=[]
list_2=[]
contig_dictionary={}
chrom_pos=""

for line in contig_file:
	line=line.rstrip("\n").split("\t")
	contig = line[5]
	if contig == "start" or contig == "end": 
		continue
	chromosomal_location = [line[1], line[2], line[3]]
	contig_dictionary[contig] = chromosomal_location
	
chr_start = 0
chr_end = 0
for line in insertions:
	line = line.rstrip("\n").split("\t")
	if line[0] == "Sample_name":
		print("\t".join(line[0:6]), "Chromosome", "stt_pos", "end_pos", *line[6:], sep="\t")
		continue
	contig = line[3].split("|")[3]
	chromosome = contig_dictionary[contig][0]
	chr_start = int(contig_dictionary[contig][1]) + int(line[4]) - 1
	chr_end = int(contig_dictionary[contig][1]) + int(line[5]) - 1
	if chromosome.isdigit() and 1 <= int(chromosome) <= 22 and (type(chromosome) != float):
		print("\t".join(line[0:6]), chromosome, chr_start, chr_end, *line[6:], sep="\t")
