#RK001;INS,INS;Hete;1;3737058;3737058;49,1;2,6;22,22;INS_F_2_3215657,INS_SID_6_3215690
import sys
import numpy as np

annot_f = open(sys.argv[1])
total_reads = int(sys.argv[2])
variant_allele_frequency = float(sys.argv[3])
for line in annot_f:
	line = line.rstrip("\n").split("\t")
	if line[0] == "chr":
		print(*line, sep="\t")
		continue
	samples = line[20:]
	#print(samples[0], samples[-1])
	ttl_lst = []
	vaf_list = []
	for sample in samples:
		if sample == "-":
			continue
		#samp = sample.split(",R")
		support = sample.split(";")[7].split(",")
		total = sample.split(";")[8].split(",")
		for i in range(len(total)):
			ttl_lst.append(int(total[i]))
		for i in range(len(support)):
			vaf = int(support[i])/int(total[i])
			vaf_list.append(vaf)
	if np.mean(vaf_list) <= variant_allele_frequency and np.mean(ttl_lst) >= total_reads:
		continue
	else:
		print(*line, sep="\t")	
