# collector

### pdf_to_csv

Code originally started by ChatGPT!
Changes that had to be made though:
- Use updated Vision API syntax
- Use credential file instead of saving full credentials to python file

This is a simple script that leverages Google's Cloud Vision API to take images and reverse image search them, crawling the returned URLs to extract price information. Currently, two types of eBay pages (collection of results, individual item) are supported by the crawler, creating a CSV with the average price per input image. 

This is currently formatted to receive an input PDF of images, which are in my personal use case coming from ScanSnap, where trading cards are being scanned to be catalogued and valued.

You will need Google Cloud Vision API credentials. 

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

python3 pdf_to_csv.py pdfs/sports_pdf_test_1.pdf 


