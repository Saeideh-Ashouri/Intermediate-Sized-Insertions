import sys

allele_freq_f = open(sys.argv[1])
maf_threshold = float(sys.argv[2])

for line in allele_freq_f:
	line = line.rstrip("\n").split("\t")
	if line[0] == "chr":
		print(*line[:], sep="\t")
		continue
	if float(line[-1]) >= maf_threshold:
		print(*line[:], sep="\t")
