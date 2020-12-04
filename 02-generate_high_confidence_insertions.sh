#!/bin/bash
#!/usr/bin/r
path=$0
if [ "$path" == "${path%/*}" ]; then src=.; else src=${path%/*}; fi
input_dir=$1
out_dir=$2
gene_file=$src/required_files/hg19_genes_ucsc.txt
acen_file=$src/required_files/hg19_telomere_centromere.txt
simplerep_file=$src/required_files/hg19_simple_repeats_ucsc.txt
repmask_file=$src/required_files/hg19_repeatmasker_ucsc.txt
microsatellites=$src/required_files/hg19_genome_microsatellites
merge_insertions_positions_difference=`python $src/bin/read_config_file.py $src/config merge_insertions_positions_difference`
annotation_flank=`python $src/bin/read_config_file.py $src/config annotation_flank`
confident_ins_num_threshold=`python $src/bin/read_config_file.py $src/config confident_ins_num_threshold`
ins_sup_reads_threshold=`python $src/bin/read_config_file.py $src/config ins_sup_reads_threshold`
ins_len_filter_threshold=`python $src/bin/read_config_file.py $src/config ins_len_filter_threshold`
total_reads=`python $src/bin/read_config_file.py $src/config total_reads`
variant_allele_frequency=`python $src/bin/read_config_file.py $src/config variant_allele_frequency`
HWE_exclusion_threshold=`python $src/bin/read_config_file.py $src/config HWE_exclusion_threshold`
allele_frequency_exclusion_threshold=`python $src/bin/read_config_file.py $src/config allele_frequency_exclusion_threshold`
reference=`python $src/bin/read_config_file.py $src/config reference`
assembly=`python $src/bin/read_config_file.py $src/config assembly`
if [ ! -d $out_dir ]; then mkdir $out_dir; fi

#echo "Concatenating insertions lists from all samples... "
#cat $input_dir/*.overall.insertions > $out_dir/01-overall_concatenated_insertions
#python $src/bin/04-remove-extra-headers-from-concatenated-insertions.py $out_dir/01-overall_concatenated_insertions > $out_dir/02-concatenated-insertions-extra-headers-removed
#awk 'NR==1; NR > 1 {print $0 | "sort -k7,7V -k8,8n"}' $out_dir/02-concatenated-insertions-extra-headers-removed > $out_dir/03-concatenated-insertions-chromosomes-sorted
#exit_value=$?; if [ $exit_value != 0 ]; then echo "<< Error >>"; exit 1; else echo "<< Finished >>"; fi
#rm $out_dir/01-overall_concatenated_insertions
#rm $out_dir/02-concatenated-insertions-extra-headers-removed

#echo "Merging insertion calls... "
#python $src/bin/05-merge-insertions.py $out_dir/03-concatenated-insertions-chromosomes-sorted $merge_insertions_positions_difference > $out_dir/04-IMSindel.insertions.merged
#exit_value=$?; if [ $exit_value != 0 ]; then echo "<< Error >>"; exit 1; else echo "<< Finished >>"; fi

#echo "Annotating insertions... "
#python $src/bin/06-annotation-gene-repeats.py $gene_file $acen_file $simplerep_file $repmask_file $out_dir/04-IMSindel.insertions.merged $annotation_flank > $out_dir/05-IMSindel.insertions.annotated
#python $src/bin/07-annotation-microsatellite.py $microsatellites $out_dir/05-IMSindel.insertions.annotated > $out_dir/06-IMSindel.insertions.overall.annotation
#exit_value=$?; if [ $exit_value != 0 ]; then echo "<< Error >>"; exit 1; else echo "<< Finished >>"; fi

echo "Filtering insertions and conducting joint call recovery... "
python $src/bin/08-size-filter.py $out_dir/06-IMSindel.insertions.overall.annotation $ins_len_filter_threshold > $out_dir/07-IMSindel.insertions-filtered-for-size
python $src/bin/09-annotation-filter.py $out_dir/07-IMSindel.insertions-filtered-for-size > $out_dir/08-IMSindel.insertions-filtered-for-annotation
python $src/bin/10-filter-for-depth-of-coverage.py $out_dir/08-IMSindel.insertions-filtered-for-annotation $total_reads $variant_allele_frequency > $out_dir/09-IMSindel.insertions-filtered-for-VAF
python $src/bin/11-joint-call-recovery.py $out_dir/09-IMSindel.insertions-filtered-for-VAF $confident_ins_num_threshold $ins_sup_reads_threshold > $out_dir/10-IMSindel.insertions-JCR
python $src/bin/12-make-HWE-dataframe.py $out_dir/10-IMSindel.insertions-JCR > $out_dir/11-IMSindel.insertions-HWE-dataframe
R --slave --vanilla $out_dir/11-IMSindel.insertions-HWE-dataframe < ./bin/13-HWE-test.R
mv 14-IMSindel.insertions-HWE-results $out_dir/
python $src/bin/14-write-HWE-results-into-insertions-list.py $out_dir/14-IMSindel.insertions-HWE-results $out_dir/10-IMSindel.insertions-JCR > $out_dir/15-IMSindel.insertions-HWE-inserted
python $src/bin/15-HWE-filter.py $out_dir/15-IMSindel.insertions-HWE-inserted $HWE_exclusion_threshold > $out_dir/16-IMSindel.insertions-HWE-filtered
python $src/bin/16-calculate-insertions-allele-frequency.py $out_dir/16-IMSindel.insertions-HWE-filtered > $out_dir/17-IMSindel.insertions-allele-frequency-inserted
python $src/bin/17-insertion-allele-frequency-filter.py $out_dir/17-IMSindel.insertions-allele-frequency-inserted $allele_frequency_exclusion_threshold > $out_dir/18-IMSindel.insertions-allele-frequency-filtered
exit_value=$?; if [ $exit_value != 0 ]; then echo "<< Error >>"; exit 1; else echo "<< Finished >>"; fi
echo "Converting high-confidence insertion call set to VCF file... "
python $src/bin/18-convert-insertion-calls-to-vcf-file.py $out_dir/18-IMSindel.insertions-allele-frequency-filtered $reference $assembly > $out_dir/intermediate-sized-insertions.vcf
exit_value=$?; if [ $exit_value != 0 ]; then echo "<< Error >>"; exit 1; fi
echo "<< Complete >>"
