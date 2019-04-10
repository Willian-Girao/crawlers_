#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, unicodedata

# Prints each element of a list line by line.
def printList(list):
    for data in list:
        print(data)

# Returns if input file ends with an '.txt' extension.
def validInputFile(input_file):
    a = input_file[len(input_file)-1]
    b = input_file[len(input_file)-2]
    c = input_file[len(input_file)-3]
    d = input_file[len(input_file)-4]
    if (d == '.' and c == 't' and b == 'x' and a == 't'):
        return True
    return False

def removeAccents(string):
    normal = unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore')
    nor = (str(normal).replace("b'", "")).replace("'", "")
    return nor

#   Open an input file containing 'prod_barcode prod_name' on each line
# and returns and array containing [[barcode, name, status]].
def openAndParseProdInputFile(input_file):
    prods_list = open(input_file, "r", encoding='utf-8')
    result = []
    for line in prods_list:
        line_split = line.split()
        prod_barcode = line_split[0]
        prod_name = ''
        for i in range(len(line_split)):
            if i != 0:
                if i != (len(line_split)-1):
                    prod_name += removeAccents(line_split[i].lower()) + "%20"
                else:
                    prod_name += removeAccents(line_split[i].lower())
        x = (prod_name.replace(",", "%2C")).replace("/", "%2F").replace(":", "").replace("*", "").replace("<", "").replace(">", "").replace("|", "").replace("\'", "")
        result.append([prod_barcode, x, 0])
    return result

#   Open an input file containing 'prod_barcode prod_name' on each line
# and returns and array containing [[barcode, name, status]].
def openAndParseAvoidGenericNamesListInputFile(input_file):
    generic_names = open(input_file, "r")
    result = []
    for line in generic_names:
        result.append(line.split()[0])
    return result

#   Open an input file containing 'webpage_url' on each line
# and returns it as a list.
def openAndParseWebpagesInputFile(input_file):
    webpages_list = open(input_file, "r")
    result = []
    for webpage in webpages_list:
        parsed_line = webpage.split() # -> [url, target_1, targe_2, tag, class]
        result.append(parsed_line)
    return result

# Parses input files and returns the products list as well as the webpages list.
def parseInputeFiles(prods_file, webpages_file, generic_names):
    # Parse products input file.
    if validInputFile(prods_file):
        parsed_prods_list = openAndParseProdInputFile(prods_file)
    else:
        sys.exit("\nProducts input file does not have '.txt' extension.")

    # Parse webpages input file.
    if validInputFile(webpages_file):
        parsed_urls_list = openAndParseWebpagesInputFile(webpages_file)
    else:
        sys.exit("\nWebpages input file does not have '.txt' extension.")

    # Parse forbiden generic names input file.
    if validInputFile(generic_names):
        parsed_generic_names_list = openAndParseAvoidGenericNamesListInputFile(generic_names)
    else:
        sys.exit("\nGeneric names input file does not have '.txt' extension.")

    return [parsed_prods_list, parsed_urls_list, parsed_generic_names_list]
