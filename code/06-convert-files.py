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

doc1 = convert_from_path("{document_path}/2020.02.14 Resultaten verwijzing orthopedisch onderzoek.pdf".format(document_path=document_path), 500)
print(doc1)
for i in range(len(doc1)):
    doc1[i].save('{document_path}/converted/page'.format(document_path=document_path) + str(i) +'.png', 'PNG')
    page_img = Image.open('{document_path}/converted/page'.format(document_path=document_path) + str(i) + '.png')
    if i == 0:
        img = Image.new('RGB', (page_img.width, page_img.height * len(doc1)))
    img.paste(page_img, (0, page_img.height * i))
    os.remove('{document_path}/converted/page'.format(document_path=document_path) + str(i) +'.png')

img.save('{document_path}/converted/concat.png'.format(document_path=document_path), 'PNG')
with open('{document_path}/converted/concat.png'.format(document_path=document_path), "rb") as image_file:
    document1 = str(base64.b64encode(image_file.read())).replace("b'", "").replace("'", "")

doc2 = convert_from_path("{document_path}/2020.03.16 Operatieraport vervanging rechter heupgewricht.pdf".format(document_path=document_path), 500)
print(doc2)
for i in range(len(doc2)):
    doc2[i].save('{document_path}/converted/page'.format(document_path=document_path) + str(i) +'.png', 'PNG')
    page_img = Image.open('{document_path}/converted/page'.format(document_path=document_path) + str(i) + '.png')
    if i == 0:
        img = Image.new('RGB', (page_img.width, page_img.height * len(doc2)))
    img.paste(page_img, (0, page_img.height * i))
    os.remove('{document_path}/converted/page'.format(document_path=document_path) + str(i) +'.png')

img.save('{document_path}/converted/concat.png'.format(document_path=document_path), 'PNG')
with open('{document_path}/converted/concat.png'.format(document_path=document_path), "rb") as image_file:
    document2 = str(base64.b64encode(image_file.read())).replace("b'", "").replace("'", "")

# Saving to database

patient_details = pd.read_csv(f"{project_folder}/code/api/reset_sql/data/zmc/patient_details.csv")

patnr_list = list(set(patient_details['patnr']))
patnr_count = len(patnr_list)
full_patnr_list = patnr_list + patnr_list

rhx = ['Right hip x-ray' for i in range(patnr_count)]
rpx = ['Right pelvis x-ray' for i in range(patnr_count)]
x_ray_list = rhx + rpx
x_types = ['x-ray' for i in range(2 * patnr_count)]
x_ray_dates = ['2020-09-01' for i in range(2 * patnr_count)]
rhi = [image_1 for i in range(patnr_count)]
rpi = [image_2 for i in range(patnr_count)]
x_ray_images = rhi + rpi

dt1 = ['Resultaten verwijzing orthopedisch onderzoek' for i in range(patnr_count)]
dt2 = ['Operatieraport vervanging rechter heupgewricht' for i in range(patnr_count)]
document_list = dt1 + dt2
d_types = ['orthopedics' for i in range(2 * patnr_count)]
dd1 = ['2020.02.14' for i in range(patnr_count)]
dd2 = ['2020.03.16' for i in range(patnr_count)]
document_dates = dd1 + dd2
doc1 = [document1 for i in range(patnr_count)]
doc2 = [document2 for i in range(patnr_count)]
document_list = doc1 + doc2

images = {'patnr': full_patnr_list, 'image_title': x_ray_list, 'type': x_types, 'date': x_ray_dates, 'image': x_ray_images}
documents = {'patnr': full_patnr_list, 'document_title': document_list, 'type': d_types, 'date': document_dates,'document': document_list}

# images = {'patnr': [1075835, 1075835], 'image_title': ['Right hip x-ray', 'Right pelvis x-ray'], 'type': ['x-ray', 'x-ray'], 'date': ['2020-09-01', '2020-09-01'], 'image': [image_1, image_2]}
# document = {'patnr': [1075835, 1075835], 'document_title': ['Resultaten verwijzing orthopedisch onderzoek', 'Operatieraport vervanging rechter heupgewricht'], 'type': ['orthopedics', 'orthopedics'], 'date': ['2020.02.14', '2020.03.16'],'document': [document1, document1]}
image_df = pd.DataFrame.from_dict(images)
document_df = pd.DataFrame.from_dict(documents)

image_df.to_sql('images', con=engine, if_exists='append', index=False, schema='zmc')
document_df.to_sql('documents', con=engine, if_exists='append', index=False, schema='zmc')

engine.dispose()