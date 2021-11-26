# Assignment 1a
Alex Antonides - 2693298 - a.m.antonides@student.vu.nl
Eoan O'Dea - 2732791 - e.odea@student.vu.nl
Tom Corten - 2618068 - t.a.corten@student.vu.nl
Max Wassenberg - 2579797 - m.n.wassenberg@student.vu.nl

## Design Choices and Rationale
We started the assignment by focusing on the problems described in the starter code file. We found two solutions to clean the html, the first and simple one was to remove all the HTML tags with a regular expression, however, this left us with CSS/JS code. The second solution, the one we uses now, was to use the library BeautifulSoup to parse the HTML and to read only the `<p>` and `<h1>` tags. We could have read anchor links as well, but most of the times theses anchor links were wrapped in paragraph tags, causing duplicate results.

We found many different solutions for the second problem of the starter code, to recognize the entities within the text. We used the following packages: NLTK, Spacy, Stanza, BERT, and Flair. However, we didn't like the processing time of Flair, furthermore, BERT only returned unigrams, and Stanza returned faulty results. 
We decided to use <x> in the end, due to <y>. 

The solution to the final problem, we used ElasticSearch and Trident to refine the results. To improve the processing, we decided to add multithreading to the program.

## Getting Started

These instructions will get you a copy up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
##### 1. Install the following software:
- [ ] [Python 3](https://www.python.corg/)
- [ ] [PIP](https://pip.pypa.io/en/stable/cli/pip_install/)

### Installing
A step by step series of examples that tell you how to get a development environment running.

##### 1. Update submodules
After cloning the repository, navigate to the project folder and run the following command [Mac and Linux only]: 
```console   
sh setup.sh
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
Once the packages have been installed, the project will be ready for deployment. 

#### Local

##### 1. Execute the shell script
```console
sh run_example.sh
```
