#!/usr/bin/python

# Native imports
import sys, os, random, requests, datetime
from bs4 import BeautifulSoup
import urllib

# User-defined imports
import preprocessing
from crawler_prod_img import ProdImageCrawler

def main(prods_file, webpages_file, names_to_avoid):
    # Parse input files.
    prod_page_genericNames_lists = preprocessing.parseInputeFiles(prods_file, webpages_file, names_to_avoid)
    # Creates a crawler instance.
    crawler = ProdImageCrawler(datetime, urllib, os, requests, BeautifulSoup, prod_page_genericNames_lists[0], prod_page_genericNames_lists[1], prod_page_genericNames_lists[2])
    # Crawling through single page.
    crawler.crawThroughPages()
    # Generates a log file (inside log folder) containing all products with no image results.
    crawler.generateMissingProdsList()

if __name__ == '__main__':
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
