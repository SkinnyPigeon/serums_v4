from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import load_only, sessionmaker, defer
import pandas as pd
from tabulate import tabulate

import os
from dotenv import load_dotenv
from pathlib import Path

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')

def hospital_picker(hospital_id):
    if hospital_id == 'FCRB':
        return 'fcrb', fcrb_tags
    elif hospital_id == 'USTAN':
        return 'ustan', ustan_tags
    elif hospital_id == 'ZMC':
        return 'zmc', zmc_tags

def get_departments(hospital):
    metadata = MetaData(schema=hospital)
    Base = automap_base(metadata=metadata)
    engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
    Base.prepare(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return {'base': Base, 'metadata': metadata, 'engine': engine, 'session': session}


