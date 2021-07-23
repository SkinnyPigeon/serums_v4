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


# Helper functions

def setup_connection(body):
    engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
    schema = body['orgID'].lower() + "_ml"
    metadata = MetaData(schema=schema, bind=engine)
    metadata.reflect(engine)
    Base = automap_base(metadata=metadata)
    Base.prepare()
    Session = sessionmaker(bind=engine)
    session = Session()
    return {"metadata": metadata, "base": Base, "engine": engine, "session": session, 'schema': schema}


def select_table_classes(schema, base):
    tables = {}
    for class_name in base._decl_class_registry.values():
        if hasattr(class_name, '__table__'):
            tables.update({class_name.__table__.fullname: class_name})
    return tables


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def convert_dates_to_string(df):
    for column in df:
        print(df[column].dtypes)
        if df.dtypes[column] in ['datetime64[ns]']:
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



# Converting Serums ID into source system ID    


def select_source_patient_id_name(body):
    connection = setup_connection(body)
    metadata = connection['metadata']
    table_dict = dict.fromkeys(metadata.sorted_tables)
    connection['engine'].dispose()
    for keys, values in table_dict.items():
        if keys.name == 'serums_ids':
            for column in keys.columns:
                if ".serums_id" not in str(column) and '.id' not in str(column):
                    return str(column).split(".")[1]


def select_source_patient_id_value(session, id_class, serums_id, key_name):
    result = session.query(id_class).filter_by(serums_id=serums_id).one()
    res = object_as_dict(result)
    return res[key_name]


def select_patient_data(session, table_class, patient_id, key_name):
    results = session.query(table_class).filter_by(**{key_name: patient_id}).all()
    data = []    
    for row in results:
        data.append(object_as_dict(row))

    df = pd.DataFrame([x for x in data]) 
    df = convert_dates_to_string(df)
    df = convert_decimal_to_float(df)
    return df.to_dict('index')


def get_patient_data(body):
    tables = ['cycles', 'general', 'intentions', 'patients', 'regimes']
    try:
        connection = setup_connection(body)
        classes = select_table_classes(connection['schema'], connection['base'])
        id_class = connection['base'].classes.serums_ids
        key_name = select_source_patient_id_name(body)
        patient_id = select_source_patient_id_value(connection['session'], 
                                                    id_class, 
                                                    body['userID'], key_name)
        results = {}
        for table in tables:
            print(table)
            table_class = connection['base'].classes[table]
            data = select_patient_data(connection['session'], table_class, patient_id, key_name)
            results[table] = data
        connection['engine'].dispose()
        return results
    except Exception as e:
        connection['engine'].dispose()
        return {"error": str(e)}