from json import load

from Data_Extraction import Extract
from Data_Scraper import Scarper


with open('../Data_Extraction/raw.json') as json_file:
    r = load(json_file)