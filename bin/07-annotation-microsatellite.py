import sys

misa = open(sys.argv[1])
insertions = open(sys.argv[2])
misa_dict = {}
for line in misa:
	line = line.rstrip("\n").split("\t")
	if line[0] == "ID":
		continue
	chrom = line[0]
	annot = [line[5], line[6], line[2], line[3]]
	misa_dict.setdefault(chrom, []).append(annot)

for line in insertions:
	line = line.rstrip("\n").split("\t")
	if line[0] == "chr":
		print("\t".join(line[0:7]), "microsatellite", *line[7:], sep="\t")
		continue
	line_dict = {}
	if "chr"+line[0] in misa_dict.keys():
		for element in misa_dict["chr"+line[0]]:
			if int(element[0]) <= int(line[1]) <= int(element[1]):
				misa_in = ",".join(element)+","+"in"
				line_dict[misa_in] = 1
			elif (abs(int(line[1])-int(element[0])) <= 10) and (abs(int(line[1])-int(element[1])) <= 10):
				if abs(int(line[1])-int(element[0])) < abs(int(line[1])-int(element[1])):
					misa_10_1 = ",".join(element)+","+str(abs(int(line[1])-int(element[0])))
					line_dict[misa_10_1]=1
				elif abs(int(line[1])-int(element[1])) < abs(int(line[1])-int(element[0])):
					misa_10_2 = ",".join(element)+","+str(abs(int(line[1])-int(element[1])))
					line_dict[misa_10_2]=1
			elif abs(int(line[1])-int(element[0])) <= 10:
				misa_10_1 = ",".join(element)+","+str(abs(int(line[1])-int(element[0])))
				line_dict[misa_10_1]=1
			elif abs(int(line[1])-int(element[1])) <= 10:
				misa_10_2 = ",".join(element)+","+str(abs(int(line[1])-int(element[1])))
				line_dict[misa_10_2]=1
	if len(line_dict):
		misa_annot = ";".join(line_dict.keys())
	else:
		misa_annot = "-"
	print("\t".join(line[0:7]), misa_annot, *line[7:], sep="\t")
