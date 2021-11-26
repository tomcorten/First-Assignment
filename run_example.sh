#!/bin/sh
start=`date +%s`

echo "Running command ..."
python3 main.py data/sample.warc.gz
echo "Computing the scores ..."
python3 score.py data/sample_annotations.tsv sample_predictions.tsv

end=`date +%s`

runtime=$((end-start))

echo "Total time: ${runtime} seconds"