# Imports and setup

from sqlalchemy import create_engine, MetaData, inspect, select
import sqlalchemy
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
from sources.search_details.zmc import zmc_patient_details
from sources.search_details.ustan import ustan_patient_details

# Helper functions

def hospital_picker(hospital):
    """Returns a lowercased hospital id, the table name holding the searchable fields, and a dictionary that maps the search fields to their native names within a hospital's system
    
            Parameters:

                hospital (str): The internal reference for the hospitals within the Serums system

            Returns: 

                hospital_id (str): The hospital id is used throughout during schema selection in the database\n
                table_name (str): The name of the table within the source system which contains the searchable fields\n
                patient_details (dict): A dictionary that maps the search terms to their native values within a hospital's system

    """
    if hospital == 'FCRB':
        return 'fcrb', 'fcrb.patient', fcrb_patient_details
    elif hospital == 'ZMC':
        return 'zmc', 'zmc.patient_details', zmc_patient_details
    elif hospital == 'USTAN':
        return 'ustan', 'ustan.general', ustan_patient_details


def setup_connection(schema):
    """Creates a connection to the database.

            Parameters:
                
                schema (str): The schema for the use case partner's data within the database

            Returns:

                connection (dict): This contains most of the important elements of the connection allowing for many different types of operations within the database
    """
    engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
    metadata = MetaData(schema=schema, bind=engine)
    metadata.reflect(engine)
    Base = automap_base(metadata=metadata)
    Base.prepare()
    Session = sessionmaker(bind=engine)
    session = Session()
    return {"metadata": metadata, "base": Base, "engine": engine, "session": session, 'schema': schema}


def get_class_by_name(patient_table, base):
    """A very useful helper function for searches the SQLAlchemy class definitions within the database for a particular table by its name
    
            Parameters:

                patient_table (str): The full name of the table within the source system\n
                base (Base): The SQLAlchemy Base instance that contains the relevant metadata to enable the search

            Returns:

                table (SQLAlchemy Table): An SQLAlchemy Table class that contains the relevant columns for searching

    """
    for class_name in base._decl_class_registry.values():
        if hasattr(class_name, '__table__') and class_name.__table__.fullname == patient_table:
            return class_name


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


def convert_tuples_to_dict(result, fields):
    """Converts tuples to dictionaries allowing dynamically selected rows from the database to be stored as JSON
    
            Parameters:

                row (tuple): Data is returned from SQLAlchemy as a generator of tuples. This is a single row from within it\n
                fields (list): The list of fields from the tags definition that is used as part of the query function

            Returns:

                row (dict): A dictionary version of the row that uses the fields as the keys and the tuple elements as the values
    """
    result_dict = {}
    for index, column in enumerate(fields):
        result_dict[column] = result[index]
    return result_dict


# Selecting the serums id based on the fields


def get_serums_id(connection, patient_id, key_name):
    """Searches the system for a particular user's Serums id based on their native patient id number
    
            Parameters:

                connection (dict): This contains most of the important elements of the connection allowing for many different types of operations within the database\n
                patient_id (int): The native patient id within the hospital's system\n
                key_name (str): The name of the patient id column within a hospital's system

            Returns:

                serums_id (int): The id used throughout the serums network linking a single patient across multiple hospitals
    """
    id_class = connection['base'].classes.serums_ids
    serums_id_column = id_class.serums_id
    results = connection['session'].query(id_class).with_entities(serums_id_column).filter_by(**{key_name: int(patient_id)}).all()
    print(results)
    return results

def search_for_serums_id(body):
    """Search function to find a patient's Serums id based on information provided such as: name, dob, gender, native patient id, etc.

            Parameters:

                body (dict): The request body from the api call

            Returns:

                serums_ids (list): A list of patients who match the search criteria
    """
    schema, tablename, search_fields = hospital_picker(body['hospital_id'])
    connection = setup_connection(schema)
    table_class = get_class_by_name(tablename, connection['base'])
    
    filters = {search_fields['fields'][key]: body[key] for key in body if key in search_fields['fields'] and body[key] not in ["", None]} 
    if len(filters) > 0:
        fields = [*search_fields['fields'].values()]
        entities = [getattr(table_class, field) for field in fields]
        try:
            ids = []
            results = connection['session'].query(table_class).with_entities(*entities).filter_by(**filters)
            for result in results:
                data = {field: result[index]for index, field in enumerate(fields)}
                df = pd.DataFrame(data, index=[0])
                df = convert_dates_to_string(df)
                df = convert_decimal_to_float(df)
                print(df[search_fields['fields']['patient_id']][0])
                serums_ids = get_serums_id(connection, df[search_fields['fields']['patient_id']][0], search_fields['fields']['patient_id']) 
                for serums_id in serums_ids:
                    df_copy = df.copy()
                    df_copy['serums_id'] = serums_id[0]
                    print(df_copy)
                    connection['engine'].dispose()
                    ids.append(df_copy.to_dict('index')[0])
            if len(ids) > 1:
                return ids, 200
            else:
                return {"message": "No patient found with those details"}, 500
        except sqlalchemy.orm.exc.NoResultFound:
            connection['engine'].dispose()
            return {"message": "No patient found with those details"}, 500
        except Exception as e:
            connection['engine'].dispose()
            return {"message": str(e)}, 500
    else:
        connection['engine'].dispose()
        return {"message": "Please include at least one search term"}, 500