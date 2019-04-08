# Web Crawlers
Web crawlers utilized for data structuring and retrieval.

# Lista

## crawler_01
Crawler for search and retrieval of products images.

The script works by pre-processing tree main files text files with _.txt_ extension: producst_list, webpages_list and strings_to_avoid. **producst_list** is a list containing both the product's barcode and name; **webpages_list** is the list of possible webpages to be crawled in order to try to find the product's image, each line contains the webpage's url and the html tags utilized to parse the page; **strings_to_avois** is a list of possible strings that, if found within the image's url, invalidates the (currently) found image's url.

#### Producst List
```txt
7896862912024 DORIL
7897076911575 CLORIDRATO DE AMIODARONA
...
```
#### Webpages List
```txt
https://www.target1/search?w= a data-sli-test resultlink title meta property og:image content meta property og:title content ?width=135&height=135
https://www.target2/ a class productPrateleira href meta property og:image content meta property og:title content none*
...
```
The structure of the above file is as follows: a b c d e f g h i j k l m n. **a** website's url; **b** tag identifying the target image's link within **a**; **c** property within **b**; **d** value associated to **c**; **e** property containing the link the a page containing the target image; **f** tag containing the image's link; **g** property within **f**; **h** value associated to **g**; **i** property containing the actual image's url; **j** tag utilized to decide if a url is feasible; **k** property whitin **j**; **l** value associated to **k**; **m** property within **j** containing the products name; **n** string to be removed from the images's url (should none be remove, replace it with 'none*').

#### Strings to Avoid
```txt
VSPMp.jpg?
C1p.jpg?
VSPM-Gp.jpg?
B1p.jpg?
B1-Gp.jpg?
...
```
#### Execution
```py
python main.py <producst_list.txt> <webpages_list.txt> <strings_to_avoid.txt>
```
For each of the target webpages in _webpages_list_, the crawler will send a request to search for each of the products in _products_list_ and, if it succeeds in fiding a feasible url, it will create a folder under _.../crawler_folder/product_images_ with the name of the product containing all its associated images.

If the crawler is unable to find any image for any of the products, it will be logged in a text file under _.../crawler_folder/logs_.
