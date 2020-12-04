import sys

hwe_combined = open(sys.argv[1])
hwe_filter_threshold = float(sys.argv[2])
for line in hwe_combined:
	line = line.rstrip("\n").split("\t")
	if line[0] == "chr":
		print(*line[:], sep = "\t")
		continue
	if float(line[-1]) > hwe_filter_threshold:
		print(*line[:], sep = "\t")
