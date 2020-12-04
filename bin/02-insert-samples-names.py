import sys
ins_extracted = open(sys.argv[1])
samplename = sys.argv[2]

for line in ins_extracted:
	line = line.rstrip("\n").split("\t")
	if line[0] == ">indel_type":
		print("Sample_name", *line, sep="\t")
		continue
	print(samplename, *line, sep="\t")


