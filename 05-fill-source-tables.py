# Setup
from sqlalchemy import create_engine, text

import os
import subprocess
import pandas as pd

from dotenv import load_dotenv

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
print(project_folder)
csv_path = "{project_folder}/code/api/reset_sql/data/zmc/".format(project_folder=project_folder)


PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')

engine = create_engine("postgresql://postgres:{}@localhost:{}/source".format(PASSWORD, PORT))

# Creating source tables

directories = ['fcrb', 'ustan', 'zmc', 'ustan_ml']

fcrb_tables = ['hospital_doctors', 'serums_ids']
ustan_tables = ['hospital_doctors', 'serums_ids', 'cycles', 'general', 'intentions', 'patients', 'regimes']
ustan_ml_tables = ['serums_ids', 'cycles', 'general', 'intentions', 'patients', 'regimes']
zmc_tables = ['hospital_doctors', 'serums_ids']

for directory in directories:
    schema = ''
    tables = []
    csv_path = "{project_folder}/code/api/reset_sql/data/{directory}/".format(project_folder=project_folder, directory=directory)

    if directory == 'fcrb':
        tables = fcrb_tables
    elif directory == 'ustan':
        tables = ustan_tables
    elif directory == 'ustan_ml':
        tables = ustan_ml_tables
    elif directory == 'zmc':
        tables = zmc_tables

    for table in tables:
        with open("{csv_path}{table}.csv".format(csv_path=csv_path, table=table), 'r') as csv:
            df = pd.read_csv(csv)
            print(df)
        df.to_sql(table, con=engine, if_exists='append', index=False, schema=directory)

engine.dispose()