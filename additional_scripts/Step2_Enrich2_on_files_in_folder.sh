#!/bin/sh

for filename in ./*.json
do
    enrich_cmd "${filename}" counts wt
done