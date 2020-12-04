import sys
from operator import itemgetter
def merge_insertions(ins_list):
	ins_dict = {}
	all_samples = []
	ins_list.sort(key=itemgetter(7))
	for sample in samples:
		sample_overall = ""
		for element in ins_list:
			if sample in element:
				sample_info = ";".join(element[0:3])+";"+";".join(element[6:10])+";"+";".join(element[11:14])
				if sample_overall:
					sample_overall = sample_overall + "," + sample_info
				else:
					sample_overall = sample_info
		if not sample_overall:
			sample_overall = "-"
		all_samples.append(sample_overall)
	print("\t".join(ins_list[0][6:9]), "\t".join(ins_list[0][3:6]), "\t".join(all_samples), sep="\t")
concatenated_ins = open(sys.argv[1])
bp_diff = int(sys.argv[2])
samples = []
for line in concatenated_ins:
	line = line.rstrip("\n").split("\t")
	if line[0] == "Sample_name":
		continue
	if line[0] not in samples:
		samples.append(line[0])
samples = sorted(samples)

print("chr", "stt", "edd", "contig", "contig_stt", "contig_edd", "\t".join(samples), sep="\t")
concatenated_ins = open(sys.argv[1])
ins_list = []
previous = []
for line in concatenated_ins:
	line = line.rstrip("\n").split("\t")
	if line[0] == "Sample_name":
		continue
	chromosome = line[6]
	position = int(line[7])
	if len(previous) > 0:
		if chromosome != previous[6] or (chromosome == previous[6] and abs(position - int(previous[7])) > bp_diff):
			merge_insertions(ins_list)
			ins_list = []	
	ins_list.append(line)
	previous = line
merge_insertions(ins_list)
