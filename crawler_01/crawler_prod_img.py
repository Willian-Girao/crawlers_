#!/usr/bin/python

class ProdImageCrawler:
    def __init__(self, datetime, urllib, os, requests, bs, prods_list, candidate_webpages, names_to_avoid):
        self.datetime = datetime
        self.urllib = urllib
        self.os = os
        self.requests = requests
        self.bs = bs
        self.prods_list = prods_list
        self.candidate_webpages = candidate_webpages
        self.names_to_avoid = names_to_avoid

    @staticmethod
    def checkShouldBeIncluded(list_splited, prod_name):
        if prod_name in list_splited:
            return True
        else:
            return False

    # Retrieves the name of an image from its url.
    @staticmethod
    def getImageNameFromUrl(img_url):
        img_name = []
        string_img_name = ''
        range_ = len(img_url)
        for i in range(0, range_):
            if img_url[((range_-1)-i)] == '/':
                break
            else:
                img_name = [img_url[((range_-1)-i)]] + img_name
        for char in img_name:
            string_img_name += char

        return string_img_name

    # Returns an url indexd by 'index' from the objects webpage list.
    def getCandidatePage(self, index):
        return self.candidate_webpages[index][0]

    # Returns the goal url 1st target tag.
    def getPageTagsInfo(self, index):
        hyperlink_tag = self.candidate_webpages[index][1] # tag outside the 'img' tag.
        hyperlink_tag_prop = self.candidate_webpages[index][2] # class associated to the 'main_tag' tag.
        hyperlink_tag_prop_val = self.candidate_webpages[index][3] # class associated to the 'main_tag' tag.
        hyperlink_link = self.candidate_webpages[index][4] # class associated to the 'main_tag' tag.

        img_tag = self.candidate_webpages[index][5] # tag where the image is located.
        img_tag_identifier = self.candidate_webpages[index][6] # class associated to the tag associated with the image.
        img_tag_identifier_val = self.candidate_webpages[index][7]
        img_tag_content = self.candidate_webpages[index][8]

        name_tag = self.candidate_webpages[index][9]
        name_tag_ident = self.candidate_webpages[index][10]
        name_tag_ident_val = self.candidate_webpages[index][11]
        name_tag_ident_val_content = self.candidate_webpages[index][12]

        remove_from_final_url = self.candidate_webpages[index][13]

        return [hyperlink_tag, hyperlink_tag_prop, hyperlink_tag_prop_val, hyperlink_link, img_tag,
        img_tag_identifier, img_tag_identifier_val, img_tag_content, name_tag, name_tag_ident,
        name_tag_ident_val, name_tag_ident_val_content, remove_from_final_url]

    # Returns 'url's html content as plaintext.
    def pageToPlaintext(self, url):
        code = self.requests.get(url)
        plain = code.text
        return plain

    # Returns a BeautifulSoup object to be 'crawled' (parsed).
    def urlToBeautifulSoup(self, url):
        plain = self.pageToPlaintext(url)
        s = self.bs(plain, "html.parser")
        return s

    # Appends links found to the product processed.
    def saveFoundLink(self, img_links, prod_index, url_index):
        prod_name = self.prods_list[prod_index][1].replace("%20", "_")
        script_dir = self.os.path.dirname(__file__)

        if not self.os.path.exists("product_images"):
            self.os.makedirs("product_images")

        if not self.os.path.exists(("product_images/" + prod_name)):
            self.os.makedirs(("product_images/" + prod_name))

        if len(img_links) > 0:
            self.prods_list[prod_index][2] = 1
            count_aux = 0
            for img_url in img_links:
                self.urllib.request.urlretrieve(img_url, ("product_images/" + prod_name + "/" +
                prod_name + "_" + str(url_index) + "_" + str(count_aux) + '.jpg'))
                count_aux += 1


    # Check whether the found link is a valid one.
    def checkIsValidLink(self, url):
        if str(url) == 'None':
            return False
        else:
            for name_to_avoid in self.names_to_avoid:
                if (name_to_avoid in str(url)):
                    return False
            return True
        return False

    # Craws through the url searching for the specified tag's related info.
    def crawPage(self, url_index, url, prod_index):
        t_info = self.getPageTagsInfo(url_index)
        s = self.urlToBeautifulSoup(url)
        imgs_hyperlinks = []

        for wrapper_tag in s.findAll(t_info[0], {t_info[1]:t_info[2]}):
            if str(wrapper_tag.get(t_info[3])) != 'None':
                imgs_hyperlinks.append(wrapper_tag.get(t_info[3]))

        final_img_links = []

        for link in imgs_hyperlinks:
            plain = self.pageToPlaintext(link)
            b = self.bs(plain, "html.parser")
            for name in b.findAll(t_info[8], {t_info[9]:t_info[10]}):
                cur_name = (name.get(t_info[11])).split()
                if cur_name[0].lower() == ('Doril').lower():
                    for target in b.findAll(t_info[4], {t_info[5]:t_info[6]}):
                        if self.checkIsValidLink(target.get(t_info[7])):
                            final_img_links.append(str(target.get(t_info[7])).replace(t_info[12], ''))

        self.saveFoundLink(final_img_links, prod_index, url_index)

    # Accesses the product list and, for each one, craws through the webpages known to the crawler.
    def crawThroughPages(self):
        url_index = 0
        for page in self.candidate_webpages:
            print("\nCrawling page: " + str(page[0]), end = '')
            prod_index = 0
            for prod_name in self.prods_list:
                self.crawPage(url_index, (page[0] + prod_name[1]), prod_index)
                prod_index += 1
            url_index += 1
        print("\n\n[ PROCESSING FINISHED ]")
        return

    # Generates a log file (inside log folder) containing all products with no image results.
    def generateMissingProdsList(self):
        script_dir = self.os.path.dirname(__file__)
        if not self.os.path.exists("logs"):
            self.os.makedirs("logs")

        current_time = (str(self.datetime.datetime.now().time()).replace(":", "_")).replace(".", "-")
        final_path = 'logs/missing_prods_' + current_time + ".txt"

        abs_file_path = self.os.path.join(script_dir, final_path)
        log_file = open(abs_file_path, "a+")

        for prod in self.prods_list:
            if prod[2] == 0:
                log_file.write(prod[0] + " " + prod[1].replace("%20", " ") + "\n")
