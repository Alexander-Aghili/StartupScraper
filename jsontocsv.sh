#!/bin/bash
echo "name,website,ycdc_status,location" > ./companies.csv

for file in ./companies_json/*; do
    echo $file
    name=$(jq -r '.name' "$file")
    website=$(jq -r '.website' "$file")
    ycdc_status=$(jq -r '.ycdc_status' "$file")
    location=$(jq -r '.location' "$file")

    echo "\"$name\",$website,$ycdc_status,\"$location\"" >> ./companies.csv
done