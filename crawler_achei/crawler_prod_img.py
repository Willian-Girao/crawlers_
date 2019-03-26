#!/usr/bin/python

class ProdImageCrawler:
    def __init__(self, requests, bs, prods_list, candidate_webpages):
        self.requests = requests
        self.bs = bs
        self.prods_list = prods_list
        self.candidate_webpages = candidate_webpages

    # Returns an url indexd by 'index' from the objects webpage list.
    def getCandidatePage(self, index):
        return self.candidate_webpages[index]

    # Returns 'url's html content as plaintext.
    def pageToPlaintext(self, url):
        code = self.requests.get(url)
        plain = code.text
        return plain

    # Returns a BeautifulSoup object to be 'crawled' (parsed).
    def urlToBeautifulSoup(self, url_index):
        plain = self.pageToPlaintext(self.getCandidatePage(url_index))
        s = self.bs(plain, "html.parser")
        return s
