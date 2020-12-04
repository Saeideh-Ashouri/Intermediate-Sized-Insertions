import sys
imsindel_overall = open(sys.argv[1])
get_header = imsindel_overall.readlines()
print(get_header[0], sep="\t", end="")

imsindel_overall = open(sys.argv[1])
for line in imsindel_overall:
	line=line.rstrip("\n").split("\t")
	status_lst = []
	if line[0] == ">indel_type":
		continue
	length = line[5].split(",")
	for ele in length:
		if int(ele) > 10:
			status = "include"
			status_lst.append(status)
	if (line[0] == "INS" or line[0] == "INS,INS") and "include" in status_lst:
		print(*line, sep="\t")
