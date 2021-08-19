# Imports and setup

from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
import subprocess

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
    """Creates a connection to the database.

            Parameters:
                
                schema (str): The schema for the use case partner's data within the database

            Returns:

                connection (dict): This contains most of the important elements of the connection allowing for many different types of operations within the database
    """
    engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
    schema = body['orgID'].lower() + "_ml"
    metadata = MetaData(schema=schema, bind=engine)
    metadata.reflect(engine)
    Base = automap_base(metadata=metadata)
    Base.prepare()
    Session = sessionmaker(bind=engine)
    session = Session()
    return {"metadata": metadata, "base": Base, "engine": engine, "session": session, 'schema': schema}


def object_as_dict(obj):
    """Returns an object as a dictionary by list comprehension
    
            Parameters:

                obj (obj): The object to be converted into a dictionary

            Returns:

                dict (dict): A dictionary based on the object
    """
    return {column.key: getattr(obj, column.key) for column in inspect(obj).mapper.column_attrs}


def convert_dates_to_string(df):
    """Converts dates to strings for ease of display in the front end
        
            Parameters:

                df (DataFrame): The Pandas DataFrame to have its dates converted

            Returns:

                df (DataFrame): The Pandas DataFrame with dates now held as strings
    
    """
    for column in df:
        if df.dtypes[column] in ['datetime64[ns]', 'object']:
            df[column] = df[column].astype(str)
    return df



def convert_decimal_to_float(df):
    """Converts decimals to floats so they can be transmitted within the JSON response
        
            Parameters:

                df (DataFrame): The Pandas DataFrame to have its decimals converted

            Returns:

                df (DataFrame): The Pandas DataFrame with decimals now held as floats
    
    """
    for column in df:
        if df.dtypes[column] in ['object']:
            try:
                df[column] = df[column].astype(float)
            except:
                pass
    return df



# Converting Serums ID into source system ID    


def select_source_patient_id_name(body):
    """Selects the correct column name for the patient id column. Different hospitals use different names for the patient id column within their systems. This allows the Serums API to retrive this value for use in querying multiple databases
    
            Parameters:
                
                body (dict): The request body passed from the frontend

            Returns:

                column_name (str): The correct name for the patient id column within a hospital's system
    
    """
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
    """Selects the patient id within the hospital's source system. Serums uses a generic id that can be used to link multiple hospitals' data, however, when searching a hospital's system we must use their internal patient id.
    
            Parameters:

                session (Session): The SQLAlchemy session to run the query with\n
                id_class (SQLAlchemy Table): The SQLAlchemy Table class to be queried\n
                serums_id (int): The id used throughout the serums network linking a single patient across multiple hospitals\n
                key_name (str): The name of the patient id column within a hospital's system

            Returns:

                patient_id (int): The native patient id within the hospital's system
    
    """
    result = session.query(id_class).filter_by(serums_id=serums_id).one()
    res = object_as_dict(result)
    return res[key_name]


# Selecting all the data

def select_patient_data(session, table_class, patient_id, key_name):
    """Selects the data within from a hospital's source system for use by the machine learning algorithm
    
            Parameters:

                session (Session): The SQLAlchemy session to run the query with\n
                tables (dict): A dictionary that uses the table names as the keys and SQLAlchemy table classes as the values\n
                tag_definition (dict): A tag definition that is based on the tags field in the request body\n
                patient_id (int): The native patient id within the hospital's system\n
                key_name (str): The name of the patient id column within a hospital's system

            Returns:

                smart_patient_health_record (DataFrame): A DataFrame containing the selected patient data

    """
    results = session.query(table_class).filter_by(**{key_name: patient_id}).all()
    data = []    
    for row in results:
        data.append(object_as_dict(row))

    df = pd.DataFrame([x for x in data]) 
    df = convert_dates_to_string(df)
    df = convert_decimal_to_float(df)
    return df.to_dict('index')


def get_patient_data_for_ml(body):
    """The main function for selecting the data for the machine learning algorithm
    
            Parameters:

                body (dict): The request body from the api call

            Returns:

                patient_data (dict): The complete dump of data for a single patient
    """
    results = {}
    tables = ['cycles', 'general', 'intentions', 'patients', 'regimes', 'smr01', 'smr06']
    try:
        connection = setup_connection(body)
        id_class = connection['base'].classes.serums_ids
        key_name = select_source_patient_id_name(body)
        patient_id = select_source_patient_id_value(connection['session'], 
                                                    id_class, 
                                                    body['userID'], key_name)
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