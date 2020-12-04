import sys

HWE_f = open(sys.argv[1])
JCR_f = open(sys.argv[2])
HWE_dict = {}
for line in HWE_f:
	line = line.rstrip("\n").split("\t")
	if line[0] == '"obs_homo_ref"':
		#print(line)
		continue
	HWE_dict[line[0]] = line[-1]

for line in JCR_f:
	line = line.rstrip("\n").split("\t")
	if line[0] == "chr":
		print("\t".join(line[0:]), "obs_homo_ref", "obs_het", "obs_homo_alt", "exp_homo_ref", "exp_het", "exp_homo_alt", "HWE_P", sep = "\t")
		continue
	samples = line[23:]
	sample_number = len(samples)
	#print(samples[0], samples[-1], sample_number)
	obs_homo_alt = 0
	obs_het = 0
	obs_homo_ref = 0
	exp_homo_alt = 0
	exp_het = 0
	exp_homo_ref = 0
	for sample in samples:
		if sample == "-":
			obs_homo_ref += 1
		elif sample != "-":
			sample = sample.split(",R")
			for samp in sample:
				samp = samp.split(";")
				if samp[2] == "Homo":
					obs_homo_alt += 1
				if samp[2] == "Hete":
					obs_het += 1
				break
	ref_freq = ((obs_homo_ref * 2) + obs_het) / (sample_number * 2)
	alt_freq = ((obs_homo_alt * 2) + obs_het) / (sample_number * 2)
	exp_homo_ref = (ref_freq ** 2) * sample_number
	exp_het = 2 * ref_freq * alt_freq * sample_number
	exp_homo_alt = (alt_freq ** 2) * sample_number
	insertion = '"' + line[0] + "_" + line[1] + "_" + line[2] + '"' 
	hwe_p = ""
	if insertion in HWE_dict.keys():
		hwe_p = HWE_dict[insertion]
	
	print("\t".join(line[0:]), round(obs_homo_ref, 0), round(obs_het, 0), round(obs_homo_alt, 0), round(exp_homo_ref, 0), round(exp_het, 0), round(exp_homo_alt, 0), hwe_p, sep = "\t")
