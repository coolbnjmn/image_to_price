### image_to_price

This is a simple script that leverages Google's Cloud Vision API to take images and reverse image search them, crawling the returned URLs to extract price information. Currently, two types of eBay pages (collection of results, individual item) are supported by the crawler, creating a CSV with the average price per input image. 

This is currently formatted to receive an input PDF of images, which are in my personal use case coming from ScanSnap, where trading cards are being scanned to be catalogued and valued.

You will need Google Cloud Vision API credentials. 

Note that a lot of this code was written with the help of ChatGPT!

#### Installation

Python v3.9.7

brew install poppler

python3 -m pip install --upgrade tensorboard

python3 -m pip install --upgrade setuptools

python3 -m pip install --upgrade google-api-python-client

python3 -m pip install --upgrade google-cloud-vision

python3 -m pip install pdf2image

python3 -m pip install bs4

#### Usage

Example:

python3 image_to_price.py pdfs/sports_pdf_test_1.pdf 


