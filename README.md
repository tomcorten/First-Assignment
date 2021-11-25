# Assignment 1a
By us

## Getting Started

These instructions will get you a copy up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
##### 1. Install the following software:
- [ ] [Python 3](https://www.python.corg/)
- [ ] [PIP](https://pip.pypa.io/en/stable/cli/pip_install/)

### Installing
A step by step series of examples that tell you how to get a development environment running.

##### 1. Update submodules
After cloning the repository, navigate to the project folder and run the following command: 
```console   
sh setup.sh
```

or run the following command:
```console   
python -m pip install -r requirements.txt
```

or run the following command:
```console
pip3 install --upgrade pip && pip3 install --user -U nltk && pip3 install beautifulsoup4 && pip3 install spacy && python3 -m spacy download en && pip3 install stanza
```

##### 2. Start the ElasticSearch server
Run the following command:
```console
sh start_elasticsearch_server.sh
```

### Deployment
Once the packagess have been installed, the project will be ready for deployment. 

#### Local

##### 1. Execute the shell script
```console
sh run_example.sh
```
