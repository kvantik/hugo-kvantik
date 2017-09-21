#!/bin/bash

# Script to convert PDF file to JPG images
#
# Dependencies:
# * pdftk
# * imagemagick

PDF=$1

echo "Processing $PDF"
DIR=local/`basename "$1" .pdf`

mkdir "$DIR"
mkdir "$DIR"/gallery
mkdir "$DIR"/thumbnails

echo '  Splitting PDF file to pages...'
pdftk "$PDF" burst output "$DIR"/%02d.pdf
#pdftk "$PDF" dump_data output "$DIR"/metadata.txt

echo '  Converting pages to JPEG files...'
convert -density 40 "$DIR"/01.pdf -quality 80 -background white -alpha remove "$DIR"/cover.jpg
for i in "$DIR"/*.pdf; do
#  convert -colorspace RGB -interlace none -density 300x300 -quality 90 "$i" "$DIR"/`basename "$i" .pdf`.jpg
  convert -density 200 "$i" -quality 90 -background white -alpha remove "$DIR"/gallery/`basename "$i" .pdf`.jpg
  convert -density 20 "$i" -quality 80 -background white -alpha remove "$DIR"/thumbnails/`basename "$i" .pdf`.jpg
  rm "$i"
done

rm "$DIR"/doc_data.txt

echo 'All done'
