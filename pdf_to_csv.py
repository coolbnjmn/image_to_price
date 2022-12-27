import os
import sys
import base64
import csv
import io

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pdf2image import convert_from_path
from google.oauth2 import service_account
from google.cloud import vision

## annotate & report functions from this Tutorial:
## https://cloud.google.com/vision/docs/internet-detection?_gl=1*q4g24p*_ga*MTQ5NjY0OTc5NC4xNjcxOTkyNTYx*_ga_WH2QY8WWF5*MTY3MjA2OTI5NS4yLjEuMTY3MjA2OTM4MS4wLjAuMA..&_ga=2.101522433.-1496649794.1671992561

def annotate(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = vision.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection

    return web_detection


def report(annotations):
    """Prints detected features in the provided web annotations."""
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if annotations.full_matching_images:
        print('\n{} Full Matches found: '.format(
              len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:
        print('\n{} Partial Matches found: '.format(
              len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
              len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))


def extract_and_annotate(pdf_file):
    pdf_name, _ = os.path.splitext(pdf_file)
    pages = convert_from_path(pdf_file)
    with open(f'{pdf_name}_results.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['page', 'url', 'score', 'source'])
        writer.writeheader()

        for i, page in enumerate(pages):
            png_file = f'{pdf_name}_page_{i+1}.png'
            page.save(png_file, 'PNG')
            result = annotate(png_file)
            if result is None:
                continue
            report(result)

            for image in result.full_matching_images:
                writer.writerow({'page':i, 'url':image.url, 'score':1, 'source': pdf_name})
            for image in result.pages_with_matching_images:
                writer.writerow({'page':i, 'url':image.url, 'score':0.5, 'source': pdf_name})
    print(f'Results saved to {pdf_name}_results.csv')
    scrape_for_price(f'{pdf_name}_results.csv')

def scrape_for_price(csv):
    # TODO
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python pdf_web_detection.py <PDF file>")
        sys.exit()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='credentials/fantasyfootball-337700-deea52633b6d.json'
    extract_and_annotate(sys.argv[1])
    