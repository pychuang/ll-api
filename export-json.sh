#!/bin/bash

# Create binary BSON dump from current database
echo "Creating database dump, enter the MongoDB admin password."
mongodump -u ll -p -d ll

# Convert BSON file to JSON files
files=$(ls --format=horizontal dump/ll/*.bson)
for file in $files
do
    base=$(echo ${file} | cut -f1 -d'.')
    bsondump "$file" > "${base}.json"
done
