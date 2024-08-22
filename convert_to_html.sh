#!/bin/bash

# Define file paths
FOLDER="Lectures/Lecture1/"
TEX_FILE=$FOLDER"Slides1.tex"
TEMP_TEX_FILE=$FOLDER"tmp.tex"
TEMP_MD_FILE=$FOLDER"tmp.qmd"
OUTPUT_MD=$FOLDER"slides_raw.qmd"

# Copy the tex file to a temporary file
cat $TEX_FILE > $TEMP_TEX_FILE

# Replace all witemize with itemize
perl -pi -e 's/witemize/itemize/g' $TEMP_TEX_FILE

# Replace all wenumerate with enumerate
perl -pi -e 's/wenumerate/enumerate/g' $TEMP_TEX_FILE

# Replace all $$ eq $$ with \[ eq \] (Not needed)
# perl -pi -e 's/\$\$(.*)\$\$/\\[$1\\]/g' $TEMP_TEX_FILE

# Remove any \pause commands
perl -pi -e 's/\\pause//g' $TEMP_TEX_FILE

# Remove any comments (start with % and end with a newline)
perl -pi -e 's/%.*\n//g' $TEMP_TEX_FILE

# Replace \begin{frame}{Title} with \begin{frame}\frametitle{Title}
perl -pi -e 's/\\begin{frame}{(.*)}/\\begin{frame}\n\\frametitle{$1}/g' $TEMP_TEX_FILE

# Remove any \vspace{}, \hspace{}, \\~\\ and \\ commands
perl -pi -e 's/\\vspace{\s*[\d\.\-]*\s*}//g' $TEMP_TEX_FILE
perl -pi -e 's/\\hspace{\s*[\d\.\-]*\s*}//g' $TEMP_TEX_FILE
perl -pi -e 's/\\~\\//g' $TEMP_TEX_FILE
perl -pi -e 's/\\\\//g' $TEMP_TEX_FILE

# Also remove hskip and vskip commands
perl -pi -e 's/\\vskip\s*[\-\+]?[\d\.]*\s*em//g' $TEMP_TEX_FILE
perl -pi -e 's/\\hskip\s*[\-\+]?[\d\.]*\s*em//g' $TEMP_TEX_FILE

# Convert to .qmd file using pandoc
pandoc $TEMP_TEX_FILE -t markdown -o $TEMP_MD_FILE --mathjax 

# Remove all extra empty lines
perl -i -pe 's/\n{3,}/\n\n/g' $TEMP_MD_FILE
#perl -i -pe 's/\s*\n\s*-\s*/-/g' $TEMP_MD_FILE

# # Add header to .qmd file
HEADER_FILE="header.txt"
echo "---" > $HEADER_FILE
echo "title: 'ECON 441'" >> $HEADER_FILE
echo "subtitle: 'Lecture 1: Preliminaries'" >> $HEADER_FILE
echo "author: 'Div Bhagia'" >> $HEADER_FILE
echo "format: revealjs" >> $HEADER_FILE
echo "---" >> $HEADER_FILE

# Combine the header and the .qmd file
cat $HEADER_FILE $TEMP_MD_FILE > $OUTPUT_MD

# Remove the temporary files
rm $TEMP_TEX_FILE
rm $TEMP_MD_FILE
rm $HEADER_FILE

# WILL NEED TO THEN MANUALLY EDIT THE .qmd FILE.