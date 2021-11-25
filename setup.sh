#!/bin/sh
echo "Running Setup ..."

# Depdencies to download (including flags)
declare -a arr=(
    "pip3 install --user -U nltk"
    "pip3 install beautifulsoup4" 
    "pip3 install --user flair" 
    "pip3 install spacy"
    "python3 -m spacy download en"
)

echo "Upgrading pip ..."
pip3 install --upgrade pip 

echo "Installing libraries ..."
# pip3 install nltk && pip3 install beautifulsoup4 && pip3 install spacy && python3 -m spacy download en

for (( i=0; i<${#arr[@]}; i++ ));
do
    echo "Installing ${i} / ${#arr[@]}"
    ${arr[i]}
done

echo "Starting Elastic Search ..."
./assets/elasticsearch-7.9.2/bin/elasticsearch -d

echo "Setup Complete!"
