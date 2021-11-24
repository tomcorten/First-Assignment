#!/bin/sh
pip3 install --upgrade pip 
pip3 install nltk && pip3 install beautifulsoup4 && pip3 install spacy && python3 -m spacy download en

sh start_elasticsearch_server.sh