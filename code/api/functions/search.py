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


def convert_dates_to_string(df):
    for column in df:
        if df.dtypes[column] in ['datetime64[ns]', 'object']:
            df[column] = df[column].astype(str)
    return df


def convert_decimal_to_float(df):
    for column in df:
        if df.dtypes[column] in ['object']:
            try:
                df[column] = df[column].astype(float)
            except:
                pass
    return df


def convert_tuples_to_dict(result, fields):
    result_dict = {}
    for index, column in enumerate(fields):
        result_dict[column] = result[index]
    return result_dict


# Selecting the serums id based on the fields


def get_serums_id(connection, patient_id, key_name):
    id_class = connection['base'].classes.serums_ids
    serums_id_column = id_class.serums_id
    result = connection['session'].query(id_class).with_entities(serums_id_column).filter_by(**{key_name: int(patient_id)}).all()

    return result[0][0]

def search_for_serums_id(body):
    schema, tablename, search_fields = hospital_picker(body['hospital_id'])
    connection = setup_connection(schema)
    table_class = get_class_by_name(tablename, connection['base'])
    filters = {search_fields['fields'][key]: body[key] for key in body if key in search_fields['fields']}
    fields = [*search_fields['fields'].values()]
    entities = [getattr(table_class, field) for field in fields]
    result = connection['session'].query(table_class).with_entities(*entities).filter_by(**filters).one()
    data = {field: result[index]for index, field in enumerate(fields)}
    df = pd.DataFrame(data, index=[0])

    df = convert_dates_to_string(df)
    df = convert_decimal_to_float(df)
    print(df[search_fields['fields']['patient_id']][0])
    serums_id = get_serums_id(connection, df[search_fields['fields']['patient_id']][0], search_fields['fields']['patient_id']) 
    df['serums_id'] = serums_id
    print(df)
    connection['engine'].dispose()
    return df.to_dict('index')[0]