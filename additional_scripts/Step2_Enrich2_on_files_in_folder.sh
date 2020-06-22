#!/bin/sh
#cd /Users/kmatreyek/Desktop/km017_Nextseq_spike_170208/Split

for filename in ./*.json
do
    enrich_cmd "${filename}" counts wt
done