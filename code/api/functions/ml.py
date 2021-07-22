# Imports and setup

from sqlalchemy import create_engine, MetaData, inspect, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import load_only, sessionmaker, defer

import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')


# Helper functions

def setup_connection(body):
    schema = body['orgID'].lower() + "_ml"
    metadata = MetaData(schema=schema)
    engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
    metadata.reflect(engine)
    Base = automap_base(metadata=metadata)
    Base.prepare()
    Session = sessionmaker(bind=engine)
    session = Session()
    return {"metadata": metadata, "base": Base, "engine": engine, "session": session, 'schema': schema}


def select_table_classes(schema, base):
    tables = {}
    for class_name in base._decl_class_registry.values():
        if hasattr(class_name, '__table__') and class_name.__table__.fullname not in ['{schema}.serums_ids'.format(schema=schema), '{schema}.patient_rules'.format(schema=schema), '{schema}.hospital_tags'.format(schema=schema), '{schema}.hospital_doctors'.format(schema=schema)]:
            tables.update({class_name.__table__.fullname: class_name})
    return tables


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


# Converting Serums ID into source system ID    


def select_source_patient_id_name(body):
    connection = setup_connection(body)
    metadata = connection['metadata']
    table_dict = dict.fromkeys(metadata.sorted_tables)
    connection['engine'].dispose()
    for keys, values in table_dict.items():
        if keys.name == 'serums_ids':
            for column in keys.columns:
                if ".serums_id" not in str(column):
                    return str(column).split(".")[1]


def select_source_patient_id_value(source_session, id_class, serums_id, key_name):
    result = source_session.query(id_class).filter_by(serums_id=serums_id).one()
    res = object_as_dict(result)
    return res[key_name]


def get_patient_data(body):
    tables = ['cycles', 'general', 'intentions', 'patients', 'regimes']
    connection = setup_connection(body)
    # print(connection['base'].classes.USTAN_ML_Serums_IDs)
    classes = select_table_classes(connection['schema'], connection['base'])
    for base_class in classes:
        print(base_class)
    try:
        # print("SERUMS ID: {}".format(connection['base'].classes.serums_ids))
        # id_class = connection['base'].classes.serums_ids
        # key_name = select_source_patient_id_name(body)
        # patient_id = select_source_patient_id_value(connection['session'], 
        #                                             connection['base'].classes.serums_ids, 
        #                                             body['serums_id'], key_name)

        # print(patient_id)

        print(dir(connection['base'].classes))

        
        connection['engine'].dispose()
        results = {}
        for table in tables:
            results[table] = 'meh'
        return results

    except Exception as e:
        connection['engine'].dispose()
        return {"error": str(e)}