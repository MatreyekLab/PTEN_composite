#!/bin/sh
#cd /Users/kmatreyek/Desktop/km017_Nextseq_spike_170208/Split

mkdir Renamed_tsv_files
cwd=$(pwd)
cd Output/tsv/

for folder in *
do
	cd $folder
	tempname=$folder
	finalname="${cwd}/Renamed_tsv_files/${tempname}.tsv"
	cp main_barcodes_counts.tsv "${finalname//_lib/}"
	cd "${cwd}/Output/tsv/"
done