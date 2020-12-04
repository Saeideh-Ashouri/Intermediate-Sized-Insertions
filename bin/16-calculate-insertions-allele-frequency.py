import sys

hwe_f = open(sys.argv[1])

for line in hwe_f:
	line = line.rstrip("\n").split("\t")
	if line [0] == "chr":
		print("\t".join(line[0:]), "allele_freq", sep="\t")
		continue
	ref = 0
	hete = 0
	alt = 0
	samples = line[23:-7]
	#print(samples[0], samples[-1])
	for sample in samples:
		if sample == "-":
			ref += 1
		elif sample != "-":
			sample = sample.split(",R")
			samp = sample[0].split(";")
			if samp[2] == "Hete":
				hete += 1
			elif samp[2] == "Homo":
				alt += 1
	sample_number = ref + hete + alt
	ins_allele_freq = ((2 * float(alt)) + float(hete)) / (2 * (float(sample_number)))
	print("\t".join(line[0:]), ins_allele_freq, sep = "\t")
	#print(ref, hete, alt, sample_number)
