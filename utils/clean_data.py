import itertools
import re
import csv
from bs4 import BeautifulSoup

#cleaning data
def clean_lines(line):    
    """clean the data

    Args:
        line (_type_): string

    Returns:
        _type_: cleaned line
    """
    #Escaping HTML characters
    line = BeautifulSoup(line, features = "html.parser").get_text()
    line = line.replace('\x92',"'")
    
    #Removal of hastags/account
    line = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", line).split())
    
    #Removal of address
    line = ' '.join(re.sub("(\w+:\/\/\S+)", " ", line).split())
    
    #Removal of Punctuation
    line = ' '.join(re.sub("[\.\,\!\?\:\;\-\=\\\]", " ", line).split())
    
    #Lower case
    line = line.lower()

    #remove new line chars
    line = line.replace('\n', '')
    
    # Standardizing words
    line = ''.join(''.join(s)[:2] for _, s in itertools.groupby(line))
    
    #Removal of extra spaces
    line = line.replace(":"," ")
    line = ' '.join(line.split())

    return line