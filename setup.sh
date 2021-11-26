<<<<<<< HEAD
#!/bin/sh
echo "Running Setup ..."
echo "Upgrading pip ..."
pip3 install --upgrade pip 
echo "Installing libraries ..."
pip3 install --user -U nltk 
pip3 install beautifulsoup4 
pip3 install spacy 
python3 -m spacy download en 
pip3 install stanza 
echo "Starting Elastic Search ..."
./assets/elasticsearch-7.9.2/bin/elasticsearch -d
echo "Setup Complete!"
=======
#!/bin/sh
echo "Running Setup ..."

echo "Upgrading pip ..."
pip3 install --upgrade pip 

echo "Installing libraries ..."
pip3 install --user -U nltk 
pip3 install beautifulsoup4 
pip3 install spacy 
python3 -m spacy download en 
pip3 install stanza 

echo "Starting Elastic Search ..."
./assets/elasticsearch-7.9.2/bin/elasticsearch -d

echo "Setup Complete!"
>>>>>>> 827d2532075ce6efd2d3a2b72891a641f99db6f5
