#chr     stt     edd     length_min      length_max      length_average  Gene    Exon    UTR     centromere/telomere     micro-satellite Simple_Repeats  Repeat_masker   simrep_fr       simrep_rv
import sys
import numpy as np

annotation_filtered_f = open(sys.argv[1])      #input file
ins_num_threshold = int(sys.argv[2])           #least number of samples with that insertion (here 2)
ins_sup_reads_threshold = int(sys.argv[3])     #least number of support reads in 2 samples (here 5)

for line in annotation_filtered_f:
	line=line.rstrip("\n").split("\t")
	if line[0] == "chr":
		print("\t".join(line[0:6]), "sample_num", "reliable_ins", "insertion_classes", *line[6:], sep="\t")
		continue
	reliable_ins = 0
	ins_stat = "None"
	samples = line[20:]
	sample_num = 0
	for sample in samples:
		if sample != "-":
			sample_num += 1
	SID = 0
	ULI = 0
	LI = 0
	LD = 0
	B = 0
	F = 0
	sr_list = []           #a list for number of support reads
	tr_list = []           #a list for total number of reads
	for sample in samples:
		if sample == "-":
			continue
		sample = sample.split(",R")
		for samp in sample:
			samp = samp.split(";")
			total_r = samp[8].split(",")
			for element in total_r:
				element=int(element)
				tr_list.append(element)
			support_r = samp[7].split(",")
			for element in support_r:
				element=int(element)
				sr_list.append(element)
			sam = samp[9].split(" ")
			if len(sam) == 1:
				ins_class = sam[0].split("_")[1]
				if ins_class == "SID":
					SID += 1
				elif ins_class == "ULI":
					ULI += 1
				elif ins_class == "LI":
					LI += 1
				elif ins_class == "LD":
					LD += 1
				elif ins_class == "B":
					B += 1
				elif ins_class == "F":
					F += 1
			elif len(sam) > 1:
				for ele in sam:
					ins_class = ele.split("_")[1]
					if ins_class == "SID":
						SID += 1
					elif ins_class == "ULI":
						ULI += 1
					elif ins_class == "LI":
						LI += 1
					elif ins_class == "LD":
						LD += 1
					elif ins_class == "B":
						B += 1
					elif ins_class == "F":
						F += 1
	ins_classes = "SID:" + str(SID) + ";ULI:" + str(ULI) + ";LI:" + str(LI) + ";B:" + str(B) + ";F:" + str(F) + ";LD:"+ str(LD)
	for element in sr_list:
		if element >= ins_sup_reads_threshold:
			reliable_ins += 1
	
	#Joint_call recovery:
	if sample_num == 1:
		ins_stat = "Excl_sn"	 #exclude because of sample number
	elif int(max(sr_list)) < ins_sup_reads_threshold:
		ins_stat = "Excl_sr"     #exclude because the maximum number of support reads for this insertion group is less than 5
	elif np.mean(tr_list) >= 150:
		ins_stat = "Excl_tr"	 #exclude because the average of total reads for this insertion group is more than 150
	elif LD > 0 and SID == 0 and ULI == 0 and LI == 0 and (F == 0 or B == 0):
		ins_stat = "Excl_ld" 	 #exclude because of existance of only LD in this insertion group
	elif ULI != 0 or LI != 0 or SID != 0:
		if reliable_ins >= ins_num_threshold:
			ins_stat = "Rescue" 
		else:
			if B != 0 and F != 0:
				ins_stat = "Rescue" 
			else:
				ins_stat = "Excl"
	elif SID == 0 and ULI == 0 and LI == 0 and B != 0 and F != 0:
		ins_stat = "Rescue"             #Rescue if insertion is detected using B and F reads but not both-type reads
	elif SID == 0 and ULI == 0 and LI == 0 and (F == 0 or B == 0):
		ins_stat = "Excl"               #Exclude if insertion is detected using only B or F reads and no both-type reads
	if ins_stat == "Rescue":
		print("\t".join(line[0:6]), sample_num, reliable_ins, ins_classes, *line[6:], sep="\t")
