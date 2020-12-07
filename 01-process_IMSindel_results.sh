#!/bin/bash

path=$0
if [ "$path" == "${path%/*}" ]; then src=.; else src=${path%/*}; fi
in_dir=$1
out_dir=$2
sample_list=$3
overall_suffix="_all.IMSindel.results"
clean_suffix="_all.IMSindel.results.ins.extracted"
samplename_suffix=".insertions"
chromosome_suffix=".chromosomes"
sort_suffix=".overall.insertions"
if [ ! -d $out_dir ]; then mkdir $out_dir; fi

while IFS='' read -r line || [[ -n "$line" ]];
do echo $line;
samplename=$line

echo "Merging IMSindel outputs..."
cat $in_dir/$samplename/*.out > $out_dir/$samplename$overall_suffix
echo "Extracting insertions..."
python $src/bin/01-extract_insertions.py $out_dir/$samplename$overall_suffix > $out_dir/$samplename$clean_suffix
echo "Attaching sample names"
python $src/bin/02-insert-samples-names.py $out_dir/$samplename$clean_suffix $samplename > $out_dir/$samplename$samplename_suffix
echo "Adding chromosomal locations..."
python $src/bin/03-add-chromosome-positions.py $src/required_files/seq_contig.md $out_dir/$samplename$samplename_suffix > $out_dir/$samplename$chromosome_suffix
awk 'NR==1; NR > 1 {print $0 | "sort -k7,7V -k8,8n"}' $out_dir/$samplename$chromosome_suffix > $out_dir/$samplename$sort_suffix
rm $out_dir/$samplename$overall_suffix
rm $out_dir/$samplename$clean_suffix
rm $out_dir/$samplename$samplename_suffix
rm $out_dir/$samplename$chromosome_suffix

echo "<< Complete >>"
echo ""
done < $sample_list
