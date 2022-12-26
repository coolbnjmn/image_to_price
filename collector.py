import sys
import os
from pdf2image import convert_from_path

import os
import sys
import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def convert_pdf_to_pngs(pdf):
    # Get the PDF file name from the command line
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_png.py <PDF file>")
        sys.exit()

    pdf_file = sys.argv[1]

    # Get the file name and extension of the PDF
    pdf_name, pdf_ext = os.path.splitext(pdf_file)

    # Convert the PDF to a series of PNG images
    pages = convert_from_path(pdf_file)

    # Save each page as a separate PNG image
    for i, page in enumerate(pages):
        png_file = f'{pdf_name}_page_{i+1}.png'
        page.save(png_file, 'PNG')

def detect_web(png_file):
    """
    Run web detection on the provided PNG file using the Google Cloud Vision API.

    Args:
        png_file: the path to the PNG file to be analyzed.

    Returns:
        A dictionary containing the web detection results, or None if the API call fails.
    """
    # Replace this with your own API key
    API_KEY = 'YOUR_API_KEY'

    # Create the API client
    vision_client = build('vision', 'v1', credentials=Credentials.from_service_account_info({
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "your-private-key",
        "client_email": "your-client-email",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "your-cert-url"
    }))

    # Read the PNG file and convert it to base64 encoding
    with open(png_file, 'rb') as f:
        image_content = f.read()
        image_content = base64.b64encode(image_content).decode('utf-8')

    # Create the request object
    request = {
        'image': {
            'content': image_content
        },
        'features': [
            {
                'type': 'WEB_DETECTION'
            }
        ]
    }

    # Call the API
    try:
        response = vision_client.images().annotate(body=request).execute()
        return response
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


if __name__ == '__main__':
    # Get the PNG file name from the command line
    if len(sys.argv) < 2:
        print("Usage: python web_detection.py <PNG file>")
        sys.exit()

    png_file = sys.argv[1]

    # Run web detection on the PNG file
    result = detect_web(png_file)
    if result is None:
        sys.exit()

    # Print the web detection results
    web_entities = result['webDetection']['webEntities']
    for entity in web_entities:
        print(f'Description: {entity["description"]}')
        print(f'Score: {entity["score"]}')
        print()