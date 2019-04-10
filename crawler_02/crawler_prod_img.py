#!/usr/bin/python

class ProdImageCrawler:
    def __init__(self, datetime, urllib, os, requests, bs, json, prods_list, candidate_webpages, names_to_avoid, tags_info):
        self.datetime = datetime
        self.urllib = urllib
        self.os = os
        self.requests = requests
        self.bs = bs
        self.tags_info = json
        self.prods_list = prods_list
        self.candidate_webpages = candidate_webpages
        self.names_to_avoid = names_to_avoid
        self.tags_info = tags_info

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
    def saveFoundLink(self, img_link, prod_index, url_index, prod_metadata):
        prod_name = ((self.prods_list[prod_index][1].replace("%20", "_")).replace("%2C", "_")).replace("%2F", "_")
        prod_name_aux = self.prods_list[prod_index][1].replace("%2F", "/").replace("%2C", ",").replace("%20", " ")
        barcode = self.prods_list[prod_index][0]
        script_dir = self.os.path.dirname(__file__)

        if not self.os.path.exists("product_images"):
            self.os.makedirs("product_images")

        self.prods_list[prod_index][2] = 1
        self.urllib.request.urlretrieve(img_link, ("product_images/" + str(barcode) + '.jpg'))

        json_out = open("prods_json_metadata.txt", "a+")
        json_out.write(prod_metadata + "\n")


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
        try:
            print("Barcode: " + str(self.prods_list[prod_index][0]))
            s = self.urlToBeautifulSoup(url)

            imgs_hyperlinks = []

            for wrapper_tag in s.findAll(self.tags_info['tag_1'], {self.tags_info['tag_property_1']:self.tags_info['tag_property_value_1']}):
                if str(wrapper_tag.get(self.tags_info['property_page_img_link_1'])) != 'None':
                    imgs_hyperlinks.append(wrapper_tag.get(self.tags_info['property_page_img_link_1']))

            final_img_links = []

            for link in imgs_hyperlinks:
                plain = self.pageToPlaintext(link)
                b = self.bs(plain, "html.parser")

                fields = []
                values = []

                for field in b.findAll(self.tags_info['target_tag_1'], {self.tags_info['target_tag_property']:self.tags_info['target_tag_property_value_1']}):
                    fields.append(field.contents[0])

                for content in b.findAll(self.tags_info['target_tag_2'], {self.tags_info['target_tag_property']:self.tags_info['target_tag_property_value_2']}):
                    values.append(content.contents[0])

                if values[1] == self.prods_list[prod_index][0]:
                    x = '"' + str(values[1]) + '": {'
                    for i in range(len(fields)):
                        if i == 0:
                            pass
                        elif i == 6:
                            x += '"' + str(fields[i]).replace(" ", "_").lower() + '": "' + str(values[i]['href'].replace(" ", "")) + '", '
                        elif i == (len(fields)-1):
                            x += '"' + str(fields[i]).replace(" ", "_").lower() + '": "' + str(values[i]) + '" },'
                        else:
                            x += '"' + str(fields[i]).replace(" ", "_").lower() + '": "' + str(values[i]) + '", '

                    for target in b.findAll(self.tags_info['tag_2'], {self.tags_info['tag_property_2']:self.tags_info['tag_property_value_2']}):
                        if self.checkIsValidLink(target.get(self.tags_info['property_page_img_link_2'])):
                            final_img_links.append(str(target.get(self.tags_info['property_page_img_link_2'])).replace(self.tags_info['expurge'], ''))

                    if len(final_img_links) > 0:
                        self.saveFoundLink(final_img_links[0], prod_index, url_index, x)
                    else:
                        not_found = open("prods_not_found.txt", "a+")
                        not_found.write(str(self.prods_list[prod_index][0]) + " " + str(self.prods_list[prod_index][1]) + "\n")
        except Exception as e:
            fail = True
            count = 0
            while (fail and (count < 3)):
                try:
                        s = self.urlToBeautifulSoup(url)

                        imgs_hyperlinks = []

                        for wrapper_tag in s.findAll(self.tags_info['tag_1'], {self.tags_info['tag_property_1']:self.tags_info['tag_property_value_1']}):
                            if str(wrapper_tag.get(self.tags_info['property_page_img_link_1'])) != 'None':
                                imgs_hyperlinks.append(wrapper_tag.get(self.tags_info['property_page_img_link_1']))

                        final_img_links = []

                        for link in imgs_hyperlinks:
                            plain = self.pageToPlaintext(link)
                            b = self.bs(plain, "html.parser")

                            fields = []
                            values = []

                            for field in b.findAll(self.tags_info['target_tag_1'], {self.tags_info['target_tag_property']:self.tags_info['target_tag_property_value_1']}):
                                fields.append(field.contents[0])

                            for content in b.findAll(self.tags_info['target_tag_2'], {self.tags_info['target_tag_property']:self.tags_info['target_tag_property_value_2']}):
                                values.append(content.contents[0])

                            if values[1] == self.prods_list[prod_index][0]:
                                x = '"' + str(values[1]) + '": {'
                                for i in range(len(fields)):
                                    if i == 0:
                                        pass
                                    elif i == 6:
                                        x += '"' + str(fields[i]).replace(" ", "_").lower() + '": "' + str(values[i]['href'].replace(" ", "")) + '", '
                                    elif i == (len(fields)-1):
                                        x += '"' + str(fields[i]).replace(" ", "_").lower() + '": "' + str(values[i]) + '" },'
                                    else:
                                        x += '"' + str(fields[i]).replace(" ", "_").lower() + '": "' + str(values[i]) + '", '

                                for target in b.findAll(self.tags_info['tag_2'], {self.tags_info['tag_property_2']:self.tags_info['tag_property_value_2']}):
                                    if self.checkIsValidLink(target.get(self.tags_info['property_page_img_link_2'])):
                                        final_img_links.append(str(target.get(self.tags_info['property_page_img_link_2'])).replace(self.tags_info['expurge'], ''))

                                if len(final_img_links) > 0:
                                    self.saveFoundLink(final_img_links[0], prod_index, url_index, x)
                                else:
                                    not_found = open("prods_not_found.txt", "a+")
                                    not_found.write(str(self.prods_list[prod_index][0]) + " " + str(self.prods_list[prod_index][1]) + "\n")
                except Exception as e:
                    print("Trying again: " + str(count))
                    count += 1

    # Accesses the product list and, for each one, craws through the webpages known to the crawler.
    def crawThroughPages(self):
        url_index = 0
        for page in self.candidate_webpages:
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
