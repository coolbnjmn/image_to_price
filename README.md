# collector

### pdf_to_csv

Code originally started by ChatGPT!
Changes that had to be made though:
- Use updated Vision API syntax
- Use credential file instead of saving full credentials to python file


#### Installation

Python v3.9.7

brew install poppler

python3 -m pip install --upgrade tensorboard
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade google-api-python-client
python3 -m pip install --upgrade google-cloud-vision
python3 -m pip install pdf2image

#### Usage

Example:

python3 pdf_to_csv.py pdfs/sports_pdf_test_1.pdf 
