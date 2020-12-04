import sys

concatenated_file = open(sys.argv[1])
get_header = concatenated_file.readlines()
print(get_header[0], sep = "\t", end = "")

concatenated_file = open(sys.argv[1])
for line in concatenated_file:
        line = line.rstrip("\n").split("\t")
        if line[0] == "Sample_name":
                continue
        else:
                print(*line, sep="\t")




