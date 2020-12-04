#chr     stt     edd     length_min      length_max      length_average  Gene    Exon    UTR     centromere/telomere     micro-satellite Simple_Repeats  Repeat_masker
#simrep_fr       simrep_rv       repmasker_fr    repmasker_rv    contig  contig_stt      contig_edd

import sys

insertions = open(sys.argv[1])

for line in insertions:
	line = line.rstrip("\n").split("\t")
	if line[0] == "chr":
		print(*line, sep="\t")
		continue
	status = ""
	status_lst = []
	centello = line[9]
	if centello == "-":
		status = "include"
		status_lst.append(status)
	else:
		status = "exclude"
		status_lst.append(status)
	average_len = int(line[5])
	misa = line[10]
	if misa == "-":
		status = "include"
		status_lst.append(status)
	elif misa != "-":
		if average_len > 50:
			status = "include"
			status_lst.append(status)
		else:
			misaa = misa.split(";")
			for element in misaa:
				seq = element.split(",")[3]
				distance = element.split(",")[4]
				complexity = seq.count(")")
				new_lst = []
				if complexity == 1:
					misaaa = seq.split(")")
					nucleotide = misaaa[0][1:]
					repeat = misaaa[1]
					if len(nucleotide) == 1 and (distance == "in" or distance == "1") and int(repeat) >= 10:
						status = "exclude"
						status_lst.append(status)
					elif len(nucleotide) > 1 and (distance == "in" or distance == "1") and int(repeat) >= 5:
						status = "exclude"
						status_lst.append(status)
					else:
						status = "include"
						status_lst.append(status)
				elif complexity > 1:
					comp_dict = {}
					if distance == "in" or distance == "1":
						misaaa = seq.split(")")
						new_ele = ""
						for element in misaaa:
							element = element.split("(")
							for ele in element:
								if ele == '':
									continue
								elif ele.isdigit() or ele.isalpha():
									new_lst.append(ele)
								else:
									new_ele = "".join(i for i in ele if i.isdigit())
									new_lst.append(new_ele)
						for i in range(0, len(new_lst), 2):
							comp_dict[i] = len(new_lst[i]) * int(new_lst[i+1])
						for element in comp_dict.values():
							if int(element) < 10:
								status = "include"
								status_lst.append(status)
							elif int(element) >= 10:
								status = "exclude"
								status_lst.append(status)
					else:
						status = "include"
						status_lst.append(status)
	simrep = line[11]
	if simrep == "-":
		status = "include"
		status_lst.append(status)
	elif simrep != "-":
		if average_len < 100:
			status = "exclude"
			status_lst.append(status)
		else:
			status = "include"
			status_lst.append(status)
	repmask = line[12]
	if "Simple_repeat" in repmask or "Satellite" in repmask or "centr" in repmask or "Low_complexity" in repmask:
		if average_len < 100:
			status = "exclude"
			status_lst.append(status)
		else:
			status = "include"
			status_lst.append(status)
	else:
		status = "include"
		status_lst.append(status)
	#print(*line)
	#print(status_lst)
	if "exclude" in status_lst:
		continue
	if "exclude" not in status_lst:
		print(*line, sep="\t")
