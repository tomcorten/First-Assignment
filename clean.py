# Dependencies
from bs4 import BeautifulSoup
import re

def clean(data):
    """
    Iterates over HTML files and returns cleaned 
    text using Beautiful Soup and Regular expressions

    @param: data: The HTML to be cleaned

    @returns string - the cleaned HTML
    """

    # Initialise Beautiful Soup
    soup = BeautifulSoup(data, 'html.parser')
    # The resulting string to be returned
    clean = ""

    # Tags we want to extract text from in the HTML
    options = [
            "h1",
            "p",
    ]

    # Loop through every specified tag within the payload  
    for paragraph in soup.find_all(options):
        # Remove any left over HTML tags
        stripped = re.sub('<[^>]*>', '', str(paragraph))
            
        # Number of \n tags in the stripped string
        nLength = len(stripped.split('\n'))
                
        # The length of the string
        strLength = len(stripped)

        # If the string has a length of more than 100
        # and contains less than 3 \n tags, 
        # add it to the final result
        if strLength > 50 and nLength < 4:
            clean += stripped + '\n'

    return clean.replace('\n', ' ')   