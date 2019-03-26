#!/usr/bin/python

# Native imports
import sys, os, random, requests
from bs4 import BeautifulSoup

# User-defined imports
import preprocessing
from crawler_prod_img import ProdImageCrawler

def main():
    # Parse products input file.
    if preprocessing.validInputFile(str(sys.argv[1])):
        parsed_prods_list = preprocessing.openAndParseProdInputFile(str(sys.argv[1]))
    else:
        print("\nProducts input file does not have '.txt' extension.")
        return

    # Parse webpages input file.
    if preprocessing.validInputFile(str(sys.argv[2])):
        parsed_urls_list = preprocessing.openAndParseWebpagesInputFile(str(sys.argv[2]))
    else:
        print("\nWebpages input file does not have '.txt' extension.")
        return

    # Creates a crawler instance.
    crawler = ProdImageCrawler(requests, BeautifulSoup, parsed_prods_list, parsed_urls_list)

    s = crawler.urlToBeautifulSoup(0)
    for link in s.findAll('a', {'class':'a-link-normal a-text-normal'}):
        for img_tag in link.findAll('img'):
            print('\nProd name: ' + img_tag.get('alt'))
            print('Prod link: ' + img_tag.get('src'))

if __name__ == '__main__':
    main()
