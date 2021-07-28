# Setup
from sqlalchemy import create_engine, text

import os
import subprocess
import pandas as pd


from pdf2image import convert_from_path
from PIL import Image

import os
import base64
import json
import time

from dotenv import load_dotenv

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
print(project_folder)

PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')

engine = create_engine("postgresql://postgres:{}@localhost:{}/source".format(PASSWORD, PORT))

# Creating image strings

image_path = "{project_folder}/code/api/reset_sql/data/zmc/images/".format(project_folder=project_folder)

with open("{image_path}/hip.png".format(image_path=image_path), "rb") as image_file:
    image_1 = str(base64.b64encode(image_file.read())).replace("b'", "").replace("'", "")
    
with open("{image_path}/pelvis.png".format(image_path=image_path), "rb") as image_file:
    image_2 = str(base64.b64encode(image_file.read())).replace("b'", "").replace("'", "")

# print(image_1)
# print(image_2)

# Converting PDF into image then transforming into string

document_path = "{project_folder}/code/api/reset_sql/data/zmc/documents/".format(project_folder=project_folder)

pages = convert_from_path("{document_path}/EFMI_STC_2020-JB_etal.pdf".format(document_path=document_path), 500)
print(pages)
for i in range(len(pages)):
    pages[i].save('{document_path}/converted/page'.format(document_path=document_path) + str(i) +'.png', 'PNG')
    page_img = Image.open('{document_path}/converted/page'.format(document_path=document_path) + str(i) + '.png')
    if i == 0:
        img = Image.new('RGB', (page_img.width, page_img.height * len(pages)))
    img.paste(page_img, (0, page_img.height * i))
    os.remove('{document_path}/converted/page'.format(document_path=document_path) + str(i) +'.png')

img.save('{document_path}/converted/concat.png'.format(document_path=document_path), 'PNG')
with open('{document_path}/converted/concat.png'.format(document_path=document_path), "rb") as image_file:
    document = str(base64.b64encode(image_file.read())).replace("b'", "").replace("'", "")

# Saving to database

images = {'patnr': [1075835, 1075835], 'image_title': ['Right hip x-ray', 'Right pelvis x-ray'], 'type': ['x-ray', 'x-ray'], 'date': ['2020-09-01', '2020-09-01'], 'image': [image_1, image_2]}
document = {'patnr': [1075835], 'document_title': ['Operation report'], 'type': ['orthopedics'], 'date': ['2020-09-20'],'document': [document]}
image_df = pd.DataFrame.from_dict(images)
document_df = pd.DataFrame.from_dict(document)

image_df.to_sql('images', con=engine, if_exists='append', index=False, schema='zmc')
document_df.to_sql('documents', con=engine, if_exists='append', index=False, schema='zmc')

engine.dispose()