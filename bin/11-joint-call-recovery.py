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
	ULI_sr_ins = 0
	LI_sr_ins = 0
	SID_sr_ins = 0
	B_sr_ins = 0
	F_sr_ins = 0
	reliable_ins = 0
	ins_stat = "None"
	samples = line[20:]
	#print(samples[0], samples[-1])
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
			sam = samp[9].split("_")
			ins_sup_reads = int(sam[2])
			sr_list.append(ins_sup_reads)
			ins_class = sam[1]
			if ins_class == "SID":
				SID += 1
				if ins_sup_reads >= ins_sup_reads_threshold:
					SID_sr_ins += 1
			elif ins_class == "ULI":
				ULI += 1
				if ins_sup_reads >= ins_sup_reads_threshold:
					ULI_sr_ins += 1						
			elif ins_class == "LI":
				LI += 1
				if ins_sup_reads >= ins_sup_reads_threshold:
					LI_sr_ins +=1
			elif ins_class == "LD":
				LD += 1
			elif ins_class == "B":
				B += 1
				if ins_sup_reads >= ins_sup_reads_threshold:
					B_sr_ins += 1
			elif ins_class == "F":
				F += 1
				if ins_sup_reads >= ins_sup_reads_threshold:
					F_sr_ins += 1
	reliable_ins += SID_sr_ins
	reliable_ins += ULI_sr_ins
	reliable_ins += LI_sr_ins
	reliable_ins += B_sr_ins
	reliable_ins += F_sr_ins
	ins_classes = "SID:" + str(SID) + ";ULI:" + str(ULI) + ";LI:" + str(LI) + ";B:" + str(B) + ";F:" + str(F) + ";LD:"+ str(LD)
	
	#Joint_call recovery:
	if sample_num == 1:
		ins_stat = "Excl_sn"	 #exclude because of sample number
	elif int(max(sr_list)) < 5:
		ins_stat = "Excl_sr"     #exclude because the maximum number of support reads for this insertion group is less than 5
	elif np.mean(tr_list) >= 150:
		ins_stat = "Excl_tr"	 #exclude because the average of total reads in individual insertions for this insertion group is more than 150
	elif LD > 0 and SID == 0 and ULI == 0 and LI == 0 and (F == 0 or B == 0):
		ins_stat = "Excl_ld" 	 #exclude because of existance of only LD in this insertion group
	elif ULI != 0 or LI != 0 or SID != 0:
		if reliable_ins >= ins_num_threshold:
			ins_stat = "Rescue"             #Rescue if insertion is detected using reads with both f and r in some samples and using B or F in other samples
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
