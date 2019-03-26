#!/usr/bin/python

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

#   Open an input file containing 'prod_barcode prod_name' on each line
# and returns and array containing [[barcode, name, status]].
def openAndParseProdInputFile(input_file):
    prods_list = open(input_file, "r")
    result = []
    for line in prods_list:
        line_split = line.split()
        prod_barcode = line_split[0]
        prod_name = ''
        for i in range(len(line_split)):
            if i != 0:
                prod_name += (line_split[i] + "_")
        result.append([prod_barcode, prod_name, 0])
    return result

#   Open an input file containing 'webpage_url' on each line
# and returns it as a list.
def openAndParseWebpagesInputFile(input_file):
    webpages_list = open(input_file, "r")
    result = []
    for webpage in webpages_list:
        result.append(webpage)
    return result
