import sys
import datetime
date = datetime.datetime.today().strftime('%Y%m%d')

ins_f = open(sys.argv[1])
reference = sys.argv[2]
assembly = sys.argv[3]
for line in ins_f:
	line = line.rstrip("\n").split("\t")
	if line[0] == "chr":
		print("##fileformat=VCFv4.2")
		print("##fileDate=" + date)
		print("##assembly=" + assembly)
		print("##INFO=<ID=SVTYPE,Number=1,Type=String,Description=\"Type of structural variant\">")
		print("##ALT=<ID=INS,Description=\"Insertion\">")
		print("##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">")
		print("#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT", "\t".join(line[20:-8]), sep="\t") 
		continue
	samples = line[23:-8]
	#print(samples[0], samples[-1])
	chromosome = line[0]
	ins_pos = line[1]
	genotype_list = []
	for sample in samples:
		if sample == "-":
			genotype = "0/0"
		elif sample != "-":
			sample = sample.split(",R")
			sample[0] = sample[0].split(";")
			if sample[0][2] == "Hete":
				genotype = "1/0"
			elif sample[0][2] == "Homo":
				genotype = "1/1"
		genotype_list.append(genotype)
	ins_id = "INS"+":"+line[0]+"_"+line[1]
	info = "SVTYPE=INS"
	print(chromosome, ins_pos, ins_id, ".", "<INS>", ".", ".", info, "GT", "\t".join(genotype_list), sep="\t")
	 
