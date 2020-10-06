#!/bin/bash
# Your task is to write a command that recursively finds all HTML
# files in the folder and makes a zip with them. Note that your command
# should work even if the files have spaces (hint: check `-d` flag for `xargs`)

mkdir folder && cd folder
for i in {1..5}; do touch file$i.html; done
mkdir folder2 && cd folder2
for i in {6..8}; do touch file$i.html; done
cd ..
find . -name "*.html" -print0 | xargs -0 tar -cavf my_html_files.tar

# cleanup
rm -rf ./folder
rm -rf my_html_files.tar
