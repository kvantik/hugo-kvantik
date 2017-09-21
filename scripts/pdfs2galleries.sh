#!/bin/bash

# bulk converts pdf files to image galleries. Needs: pdf2jpg.sh

names=( $@ )
for file in "${names[@]}"
do
    ./pdf2jpg.sh "$file"
done