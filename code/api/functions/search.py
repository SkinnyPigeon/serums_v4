# Imports and setup

from sqlalchemy import create_engine, MetaData, inspect, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import load_only, sessionmaker, defer

import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess

import json
import pandas as pd

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')

from sources.search_details.fcrb import fcrb_patient_details

# Helper functions

def hospital_picker(hospital):
    if hospital == 'FCRB':
        return 'fcrb', 'fcrb.patient', fcrb_patient_details


def setup_connection(schema):
    engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
    metadata = MetaData(schema=schema, bind=engine)
    metadata.reflect(engine)
    Base = automap_base(metadata=metadata)
    Base.prepare()
    Session = sessionmaker(bind=engine)
    session = Session()
    return {"metadata": metadata, "base": Base, "engine": engine, "session": session, 'schema': schema}


def get_class_by_name(patient_table, base):
    for class_name in base._decl_class_registry.values():
        if hasattr(class_name, '__table__') and class_name.__table__.fullname == patient_table:
            return class_name


# Selecting data


def search_for_serums_id(body):
    schema, tablename, search_fields = hospital_picker(body['hospital_id'])
    connection = setup_connection(schema)
    table_class = get_class_by_name(tablename, connection['base'])



    connection['engine'].dispose()
    return {'hey': 'you'}