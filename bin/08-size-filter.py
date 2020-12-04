#chr     stt     edd     Gene    Exon    UTR     centromere/telomere     micro-satellite Simple_Repeats  Repeat_masker   simrep_fr       simrep_rv       repmasker_fr    repmasker_rv
#1       768116  768116  LINC01128;unk;unk       -       5_UTR,LINC01128 -       768117,768161,p5,(GTTTT)9,1     simple_repeat,trf:768116:768161 SINE,Alu        fr_flank,covers_sim


import sys
import numpy as np

annotation_f = open(sys.argv[1])
size_filter_threshold = int(sys.argv[2])
for line in annotation_f:
	line = line.rstrip("\n").split("\t")
	if line[0] == "chr":
		print(line[0], line[1], line[2], "length_min", "length_max", "length_average", *line[3:], sep = "\t")
		continue
	samples = line[17:]
	ins_list=[]
	pos_list=[]
	for sample in samples:
		if sample=="-":
			continue
		sample=sample.split(",R")
		for element in sample:
			element=element.split(";")
			length=element[6].split(",")
			for ele in length:
				ele = int(ele)
				ins_list.append(ele)
			
	if np.mean(ins_list) < size_filter_threshold:
		continue
	else:
		print(line[0], line[1], line[2], min(ins_list), max(ins_list), int(np.mean(ins_list)), *line[3:], sep = "\t")
