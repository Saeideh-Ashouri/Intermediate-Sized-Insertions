#genes file:
##bin    name    chrom   strand  txStart txEnd   cdsStart        cdsEnd  exonCount       exonStarts      exonEnds        score   name2   cdsStartStat    cdsEndStat      exonFrames
#9       NM_012405       chr1    -       6281252 6296044 6285139 6295971 5       6281252,6291961,6293533,6294945,6295776,        6285322,6292179,6293703,6295034,6296044,        0       ICMT    cmpl    cmpl    0,1,2,0,0,

#insertions file:
#chr     stt     edd     contig  contig_stt      contig_edd      RK001   RK002   RK004   RK007   RK010   RK012   RK014   RK016   RK018   RK020   RK021   RK022   RK024   RK026   RK027   RK028   RK029   RK032   RK033   RK034
#1       601984  601984  gi|224514624|ref|NT_004350.19|  80616   80616   RK001;INS;Hete;1;601984;601984;1;14;59;INS_SID_14_80616 -       RK004;INS;Hete;1;601984;601984;1;3;40;INS_SID_3_80616   RK007;INS;Hete;1;601984;601984;1;

import sys

genes = open(sys.argv[1])
centelo = open(sys.argv[2])
simrep = open(sys.argv[3])
repmasker = open(sys.argv[4])
insertions = open(sys.argv[5])
flanking_range = sys.argv[6]
genes_dict = {}
for line in genes:
	line = line.rstrip("\n").split("\t")
	chrom = line[2]
	genes_dict.setdefault(chrom, []).append(line)
centelo_dict = {}
for line in centelo:
	line = line.rstrip("\n").split("\t")
	chrom = line[0]
	annot = [line[1], line[2], line[-1]]
	centelo_dict.setdefault(chrom, []).append(annot)
simrep_dict = {}
for line in simrep:
	line = line.rstrip("\n").split("\t")
	chrom = line[1]
	annot = [line[2], line[3], line[4]]
	simrep_dict.setdefault(chrom, []).append(annot)
repmask_dict = {}
for line in repmasker:
	line = line.rstrip("\n").split("\t")
	chrom = line[5]
	annot = [line[6], line[7], line[11], line[12]]
	repmask_dict.setdefault(chrom, []).append(annot)

for line in insertions:
	line = line.rstrip("\n").split("\t")
	gene_dict_out = {}
	exon_dic_out = {}
	centelo_dict_out = {}
	simrep_dict_out = {}
	simrep_fr_flank_dict_out = {}
	simrep_rv_flank_dict_out = {}
	repmask_dict_out = {}
	fr_flank_dict_out = {}
	rv_flank_dict_out = {}
	if line[0] == "chr":
		print("\t".join(line[0:3]), "Gene", "Exon", "centromere/telomere", "Simple_Repeats", "Repeat_masker", "simrep_fr", "simrep_rv", "repmasker_fr", "repmasker_rv", *line[3:], sep="\t")
		continue
	chrm = "chr" + line[0]
	for element in genes_dict[chrm]:
		gene_name = ""
		status = "within"
		if int(line[1]) < int(element[4]) or int(line[1]) > int(element[5]):
			continue
		elif int(element[4]) <= int(line[1]) <= int(element[5]):
			gene_name = element[12] + ";" + element[13] + ";" + element[14]
			gene_dict_out[gene_name] = 1
		if status == "within":
			exon_stt_list = element[9].split(",")
			del exon_stt_list[-1]
			exon_edd_list = element[10].split(",")
			del exon_edd_list[-1]
			for stt,edd in zip(exon_stt_list, exon_edd_list):
				exon_pos = ""
				if int(stt) <= int(line[1]) <= int(edd):
					exon_pos = element[12] + "," + "exon" + "," + stt + "," + edd
					exon_dic_out[exon_pos] = 1
	if len(gene_dict_out) >= 1:
		gene_annot = ",".join(gene_dict_out.keys())
	elif len(gene_dict_out) == 0:
		gene_annot = "-"
	if len(exon_dic_out) >= 1:
		exon_annot = ",".join(exon_dic_out.keys())
	elif len(exon_dic_out) == 0:
		exon_annot = "-"
	for element in centelo_dict[chrm]:
		if int(element[0]) <= int(line[1]) <= int(element[1]):
			centelo_annot = element[2]
			centelo_dict_out[centelo_annot] = 1
	if len(centelo_dict_out) > 0:
		centelo_annotation = ";".join(centelo_dict_out.keys())
	else:
		centelo_annotation = "-"
	
	for element in simrep_dict[chrm]:
		rear = int(line[1]) + int(flanking_range)
		front = int(line[1]) - int(flanking_range)
		if int(element[0]) <= int(line[1]) <= int(element[1]):
			simrep_annot = "simple_repeat" + "," + element[2] + ":" + element[0] + ":" + element[1]
			simrep_dict_out[simrep_annot] = 1
		if int(element[0]) >= front and int(element[1]) <= int(line[1]):
			simrep_fr_flank_prop = str(round((int(element[1]) - int(element[0])) / (int(line[1]) - front), 2))
			simrep_fr_flank = "fr_flank" + "," + "covers_simrep" + "," + simrep_fr_flank_prop
			simrep_fr_flank_dict_out[simrep_fr_flank] = 1
		elif int(element[0]) < front and int(line[1]) < int(element[1]):
			simrep_fr_flank_prop =str(round(((int(line[1]) - front) / (int(element[1]) - int(element[0]))), 2))
			simrep_fr_flank = "fr_flank" + "," + "within_simrep" + "," + simrep_fr_flank_prop
			simrep_fr_flank_dict_out[simrep_fr_flank] = 1
		elif int(element[0]) <= front and front < int(element[1]) < int(line[1]):
			simrep_fr_flank_prop = str(round((int(element[1]) - front) / (int(line[1]) - front), 2))
			simrep_fr_flank = "fr_flank" + "," + "partial_simrep" + "," + simrep_fr_flank_prop
			simrep_fr_flank_dict_out[simrep_fr_flank] = 1
		elif front < int(element[0]) < int(line[1]) and int(element[1]) >= int(line[1]):
			simrep_fr_flank_prop = str(round((int(line[1]) - int(element[0])) / (int(line[1]) - front), 2))
			simrep_fr_flank = "fr_flank" + "," + "partial_simrep" + "," + simrep_fr_flank_prop
			simrep_fr_flank_dict_out[simrep_fr_flank] = 1
		if rear >= int(element[1]) and int(line[1]) <= int(element[0]):
			simrep_rv_flank_prop = str(round((int(element[1]) - int(element[0])) / (rear - int(line[1])), 2)) 
			simrep_rv_flank = "rv_flank" + "," + "covers_simrep" + "," + simrep_rv_flank_prop
			simrep_rv_flank_dict_out[simrep_rv_flank] = 1
		elif int(element[1]) > rear and int(element[0]) < int(line[1]):
			simrep_rv_flank_prop = str(round((rear - int(line[1])) / (int(element[1]) - int(element[0])), 2))
			simrep_rv_flank = "rv_flank" + "," + "within_simrep" + "," + simrep_rv_flank_prop 
			simrep_rv_flank_dict_out[simrep_rv_flank] = 1
		elif int(element[0]) <= int(line[1]) and int(line[1]) < int(element[1]) < rear:
			simrep_rv_flank_prop = str(round((int(element[1]) - int(line[1])) / (rear - int(line[1])), 2))
			simrep_rv_flank = "rv_flank" + "," + "partial_simrep" + "," + simrep_rv_flank_prop
			simrep_rv_flank_dict_out[simrep_rv_flank] = 1
		elif int(line[1]) < int(element[0]) < rear and int(element[1]) >= rear:
			simrep_rv_flank_prop = str(round((rear - int(element[0])) / (rear - int(line[1])), 2))
			simrep_rv_flank = "rv_flank" + "," + "partiall_simrep" + "," + simrep_rv_flank_prop
			simrep_rv_flank_dict_out[simrep_rv_flank] = 1
	if len(simrep_dict_out) > 0:
		simrep_annotation = ";".join(simrep_dict_out.keys())
	else:
		simrep_annotation = "-"
	if len(simrep_fr_flank_dict_out) > 0:
		simrep_fr_flank_annotation = ";".join(simrep_fr_flank_dict_out.keys())
	else:
		simrep_fr_flank_annotation = "-"
	if len(simrep_rv_flank_dict_out) > 0:
		simrep_rv_flank_annotation = ";".join(simrep_rv_flank_dict_out.keys())
	else:
		simrep_rv_flank_annotation = "-"
	for element in repmask_dict[chrm]:
		rear = int(line[1]) + int(flanking_range)
		front = int(line[1]) - int(flanking_range)
		if int(element[0]) <= int(line[1]) <= int(element[1]):
			repmask_annot = element[2] + "," + element[3]
			repmask_dict_out[repmask_annot] = 1
		if int(element[0]) >= front and int(element[1]) <= int(line[1]):
			fr_flank_prop = str(round((int(element[1]) - int(element[0])) / (int(line[1]) - front), 2))
			fr_flank = "fr_flank" + "," + "covers_repmask" + "," + element[-1] + "," + fr_flank_prop
			fr_flank_dict_out[fr_flank] = 1
		elif int(element[0]) < front and int(line[1]) < int(element[1]):
			fr_flank_prop =str(round(((int(line[1]) - front) / (int(element[1]) - int(element[0]))), 2))
			fr_flank = "fr_flank" + "," + "within_repmask" + "," + element[-1] + "," +  fr_flank_prop
			fr_flank_dict_out[fr_flank] = 1
		elif int(element[0]) <= front and front < int(element[1]) < int(line[1]):
			fr_flank_prop = str(round((int(element[1]) - front) / (int(line[1]) - front), 2))
			fr_flank = "fr_flank" + "," + "partial_repmask" + "," + element[-1] + "," +  fr_flank_prop
			fr_flank_dict_out[fr_flank] = 1
		elif front < int(element[0]) < int(line[1]) and int(element[1]) >= int(line[1]):
			fr_flank_prop = str(round((int(line[1]) - int(element[0])) / (int(line[1]) - front), 2))
			fr_flank = "fr_flank" + "," + "partial_repmask" + "," + element[-1] + "," +  fr_flank_prop
			fr_flank_dict_out[fr_flank] = 1
		if rear >= int(element[1]) and int(line[1]) <= int(element[0]):
			rv_flank_prop = str(round((int(element[1]) - int(element[0])) / (rear - int(line[1])), 2)) 
			rv_flank = "rv_flank" + "," + "covers_repmask" + "," + element[-1] + "," + rv_flank_prop
			rv_flank_dict_out[rv_flank] = 1
		elif int(element[1]) > rear and int(element[0]) < int(line[1]):
			rv_flank_prop = str(round((rear - int(line[1])) / (int(element[1]) - int(element[0])), 2))
			rv_flank = "rv_flank" + "," + "within_repmask" + "," + element[-1] + "," + rv_flank_prop 
			rv_flank_dict_out[rv_flank] = 1
		elif int(element[0]) <= int(line[1]) and int(line[1]) < int(element[1]) < rear:
			rv_flank_prop = str(round((int(element[1]) - int(line[1])) / (rear - int(line[1])), 2))
			rv_flank = "rv_flank" + "," + "partial_repmask" + "," + element[-1] + ","  + rv_flank_prop
			rv_flank_dict_out[rv_flank] = 1
		elif int(line[1]) < int(element[0]) < rear and int(element[1]) >= rear:
			rv_flank_prop = str(round((rear - int(element[0])) / (rear - int(line[1])), 2))
			rv_flank = "rv_flank" + "," + "partial_repmask" + "," + element[-1] + "," + rv_flank_prop
			rv_flank_dict_out[rv_flank] = 1
	if len(repmask_dict_out) > 0:
		repmask_annotation = ";".join(repmask_dict_out.keys())
	else:
		repmask_annotation = "-"
	if len(fr_flank_dict_out) > 0:
		fr_flank_annotation = ";".join(fr_flank_dict_out.keys())
	else:
		fr_flank_annotation = "-"
	if len(rv_flank_dict_out) > 0:
		rv_flank_annotation = ";".join(rv_flank_dict_out.keys())
	else:
		rv_flank_annotation = "-"
	
	print("\t".join(line[0:3]), gene_annot, exon_annot, centelo_annotation, simrep_annotation, repmask_annotation, simrep_fr_flank_annotation, simrep_rv_flank_annotation, fr_flank_annotation, rv_flank_annotation, *line[3:], sep="\t")

