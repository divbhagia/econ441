#!/bin/bash
# This script converts the .qmd files to pdf files using quarto
# Run this script from the Project directory using the command: bash pdf-version.sh
quarto render overview.qmd --to pdf --output overview.pdf
quarto render tutorial1.qmd --to pdf --output tutorial1.pdf
quarto render tutorial2.qmd --to pdf --output tutorial2.pdf
quarto render exercise.qmd --to pdf --output exercise.pdf

# .ipynb file to pdf conversion
jupyter nbconvert --to pdf solution.ipynb
