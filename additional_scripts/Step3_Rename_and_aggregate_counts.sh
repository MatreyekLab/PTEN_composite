#!/bin/sh

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