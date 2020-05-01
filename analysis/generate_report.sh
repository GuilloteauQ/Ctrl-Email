FILENAME=INP.csv
Rscript -e "rmarkdown::render('analysis.Rmd', 'pdf_document', params=list(filename = '${FILENAME}'))"
