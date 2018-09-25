#!/bin/bash

#wiki_dump_file=/home/cgfth/TaxoRL_Datasets/corpus/wiki/enwiki-20180701-pages-articles-multistream.xm;
wiki_dump_file=/home/cgfth/TaxoRL_Datasets/corpus/wiki/enwiki_10000.xml
vocabulary_file=/home/cgfth/TaxoRL_Datasets/corpus/wiki/resource_prefix/wikiEntities.txt
resource_prefix=/home/cgfth/TaxoRL_Datasets/corpus/wiki/resource_prefix/



parsed_dump_file=/home/cgfth/TaxoRL_Datasets/corpus/wiki/parsed_wikipedia
count_paths=/home/cgfth/TaxoRL_Datasets/corpus/wiki/count_paths

path_support=2
file_prefix="enwiki_10000.xml_a"

echo '*****************************'
echo $wiki_dump_file
echo $vocabulary_file
echo $resource_prefix
echo $path_support
echo 'parsing wikipedia...'
#split -nl/10 $wiki_dump_file $wiki_dump_file"_"


#for x in {a..j}
#do
#	curr_filename=${wiki_dump_file##*/}"_a"$x
#   echo "Paese Wikipedia. Current parse file: "$curr_filename
#    ( python3 parse_wikipedia.py $wiki_dump_file"_a"$x $vocabulary_file $parsed_dump_file"/"$curr_filename"_parsed" ) &
#done
#wait


#for x in {a..j}
#do	curr_filename=${wiki_dump_file##*/}"_a"$x
#	echo "Count paths. Current count file: "$curr_filename
#	(awk -v OFS='\t' '{i[$3]++} END{for(x in i){print x, i[x]}}' $parsed_dump_file"/"$curr_filename"_parsed" > $count_paths"/"paths"_a"$x ) &
#done
#wait


#echo "Select path"
#cat $count_paths"/"paths_a* > $count_paths"/"paths_temp
#cat $count_paths"/"paths_temp | grep -v "$(printf '\t1$')" > $count_paths"/"frequent_paths_temp
#awk -F$'\t' '{i[$1]+=$2} END {for(x in i){print x"\t"i[x]}}' $count_paths"/"frequent_paths_temp > $count_paths"/"paths
#awk -v var="$path_support" -F$'\t' '$2 >= var {print $1}' $count_paths"/"paths > $count_paths"/"frequent_paths
#rm $count_paths"/"paths_temp $count_paths"/"frequent_paths_temp $count_paths"/"paths_a*


#echo 'Creating the resource from the triplets file...'
#python3 create_resource_from_corpus1.py $count_path"/"frequent_paths $vocabulary_file $resource_prefix
#for x in {a..j}
#do
#	( python3 create_resource_from_corpus2.py $parsed_dump_file"/"$file_prefix$x"_parsed" $resource_prefix) &
#done
#wait

for x in {a..j}
do
( awk -v OFS='\t' '{i[$0]++} END{for (x in i){print x, i[x]}}' $parsed_dump_file"/"$file_prefix$x"_parsed_id"  > $parsed_dump_file"/"id_triplet_file"_a"$x) &
done
wait

cat $parsed_dump_file"/"id_triplet_file_a* > $parsed_dump_file"/"id_triplet_file_temp
rm $parsed_dump_file"/"id_triplet_file_a*

awk -F $'\t' 'BEGIN {OFS=FS} {if ($1 % 5 == 0 ) {a[$1][$2][$3] += $4}} END {for (i in a) for (j in a[i]) for (k in a[i][j]) print i, j, k, a[i][j][k]}' $parsed_dump_file"/"id_triplet_file_temp > $parsed_dump_file"/"id_triplet_file_0 & 
awk -F $'\t' 'BEGIN {OFS=FS} {if( $1 % 5 == 1 ) {a[$1][$2][$3] += $4}} END {for (i in a) for (j in a[i]) for (k in a[i][j]) print i, j, k, a[i][j][k]}' $parsed_dump_file"/"id_triplet_file_temp > $parsed_dump_file"/"id_triplet_file_1 &
awk -F $'\t' 'BEGIN {OFS=FS} {if( $1 % 5 == 2 ) {a[$1][$2][$3] += $4}} END {for (i in a) for (j in a[i]) for (k in a[i][j]) print i, j, k, a[i][j][k]}' $parsed_dump_file"/"id_triplet_file_temp > $parsed_dump_file"/"id_triplet_file_2 &
awk -F $'\t' 'BEGIN {OFS=FS} {if( $1 % 5 == 3 ) {a[$1][$2][$3] += $4}} END {for (i in a) for (j in a[i]) for (k in a[i][j]) print i, j, k, a[i][j][k]}' $parsed_dump_file"/"id_triplet_file_temp > $parsed_dump_file"/"id_triplet_file_3 &
awk -F $'\t' 'BEGIN {OFS=FS} {if( $1 % 5 == 4 ) {a[$1][$2][$3] += $4}} END {for (i in a) for (j in a[i]) for (k in a[i][j]) print i, j, k, a[i][j][k]}' $parsed_dump_file"/"id_triplet_file_temp > $parsed_dump_file"/"id_triplet_file_4 &

wait
cat $parsed_dump_file"/"id_triplet_file_* > $parsed_dump_file"/"id_triplet_file
python3 create_resource_from_copus3.py $parsed_dump_file"/"id_triplet_file $resource_prefix

#mkdir $resource_prefix
#mv $resource_prefix&.db $resource_prefix
#mv -t $resource_prefix paths_id_triplet_file frequent_paths wiki_parsed
