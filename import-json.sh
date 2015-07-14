#!/bin/bash
#files=$(ls --format=horizontal dump/ll/*.json)
for base in doc feedback historical query run site system user
do
    #base=$(echo ${file} | cut -f1 -d'.')
    file="dump/ll/${base}.json"
    filemeta="dump/ll/${base}.metadata.json"
    mongoimport -u ll --authenticationDatabase ll -d ll -c $base -p USERSECRET < $file
    #mongoimport -u ll --authenticationDatabase ll -d ll -c $base -p USERSECRET < $filemeta
    python import-metadata.py $base
done


