# Imports and setup

from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError

import os
from dotenv import load_dotenv
import subprocess

from pandas import DataFrame

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')

from sources.tags.fcrb import fcrb_tags
from sources.tags.ustan import ustan_tags
from sources.tags.zmc import zmc_tags
from functions.lineage import create_record, update_record, schema_string
from functions.rules import validate_rules
from functions.jwt import validate_jwt


# Helper functions

def hospital_picker(hospital):
    """Returns a lowercased hospital id and tag definitions.
    
            Parameters:

                hospital (str): The internal reference for the hospitals within the Serums system

            Returns: 

                hospital_id (str): The hospital id is used throughout during schema selection in the database\n
                hospital_tags (list): A list of tag definitions. These are designed by the hospitals to subset their data in ways that the patients can intuitively understand when they create rules. These definitions show:\n
                \t\t - The source table that holds the data
                \t\t - The columns within the source table that are governed by the tag

    """
    if hospital == 'FCRB':
        return 'fcrb', fcrb_tags
    elif hospital == 'USTAN':
        return 'ustan', ustan_tags
    elif hospital == 'ZMC':
        return 'zmc', zmc_tags


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


def object_as_dict(obj):
    """Returns an object as a dictionary by list comprehension
    
            Parameters:

                obj (obj): The object to be converted into a dictionary

            Returns:

                dict (dict): A dictionary based on the object
    """
    return {column.key: getattr(obj, column.key) for column in inspect(obj).mapper.column_attrs}


def select_tags(tags_list, request_tags):
    """Selects the relevant tag definition(s) based on the tags field in the request body
    
            Parameters:

                tags_list (list): The tag definitions as selected by hospital_picker()\n
                request_tags (list): The list of tags that are to be used as selected by the request body

            Returns:

                selected_tags (list): A list of the tag definitions that is based on the tags field in the request body
    """
    selected_tags = []
    for request_tag in request_tags:
        for tag_definition in tags_list:
            try:
                if tag_definition['tag'] == request_tag:
                    selected_tags.append(tag_definition)
            except:
                pass
    return selected_tags


def get_classes(schema, base):
    """A very useful helper function for selecting the all of the SQLAlchemy class definitions within the database
    
            Parameters:

                schema (str): The schema within the database to search through\n
                base (Base): The SQLAlchemy Base instance that contains the relevant metadata to enable the search

            Returns:

                tables (dict): A dictionary that uses the table names as the keys and SQLAlchemy table classes as the values

    """
    tables = {}
    for class_name in base._decl_class_registry.values():
        if hasattr(class_name, '__table__') and class_name.__table__.fullname not in ['{schema}.serums_ids'.format(schema=schema), '{schema}.hospital_doctors'.format(schema=schema)]:
            tables.update({class_name.__table__.fullname: class_name})
    return tables


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

def convert_tuples_to_dict(row, fields):
    """Converts tuples to dictionaries allowing dynamically selected rows from the database to be stored as JSON
    
            Parameters:

                row (tuple): Data is returned from SQLAlchemy as a generator of tuples. This is a single row from within it\n
                fields (list): The list of fields from the tags definition that is used as part of the query function

            Returns:

                row (dict): A dictionary version of the row that uses the fields as the keys and the tuple elements as the values
    """
    row_dict = {}
    if len(row) == len(fields):
        for index, column in enumerate(fields):
            row_dict[column] = row[index]
    return row_dict


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



# Selecting tabular data:

def select_tabular_patient_data(connection, tables, tag_definition, patient_id, key_name):
    """Selects the tabular data within from a hospital's source system
    
            Parameters:

                connection (dict): The connection dictionary that contains all of the aspects to work with SQLAlchemy\n
                tables (dict): A dictionary that uses the table names as the keys and SQLAlchemy table classes as the values\n
                tag_definition (dict): A tag definition that is based on the tags field in the request body\n
                patient_id (int): The native patient id within the hospital's system\n
                key_name (str): The name of the patient id column within a hospital's system

            Returns:

                smart_patient_health_record (DataFrame): A DataFrame containing the selected patient data

    """
    data = []
    table_class = tables[tag_definition['source']]
    fields = tag_definition['fields']
    entities = []
    for field in fields:
        entities.append(getattr(table_class, field))
    try:
        result = connection['session'].query(table_class).with_entities(*entities).filter_by(**{key_name: patient_id}).all()
        for row in result:
            data.append(convert_tuples_to_dict(row, fields))
    except InvalidRequestError as i:
        foreign_key_table_class = tables[tag_definition['key_lookup']['table']]
        foreign_key = tag_definition['key_lookup']['key']
        key_entities = []
        key_entities.append(getattr(foreign_key_table_class, foreign_key))
        key_result = connection['session'].query(foreign_key_table_class).with_entities(*key_entities).filter_by(**{key_name: patient_id}).all()
        for row in key_result:
            result = connection['session'].query(table_class).with_entities(*entities).filter_by(**{foreign_key: row[0]}).all()
            for row in result:
                data.append(convert_tuples_to_dict(row, fields))
    return data

def hash_columns(columns):
    """Used to hash the columns of the Smart Patient Health Records. This allows for verification that the data selection has taken place correctly based on the rule definition

            Parameters:

                columns (list): A list of the columns that are to be hashed

            Returns:

                column_hash (str): A string hash that allows verification the correct columns have been selected without revealing the details of what those columns are

    """
    column_hash = schema_string(columns)
    return column_hash

def select_patient_data(connection, tags_definitions, patient_id, key_name, proof_id):
    """Used to determine the type of data selection to be used i.e. image, tabular, or graph. Calls the relevant function.
    
            Parameters:

                connection (dict): This contains most of the important elements of the connection allowing for many different types of operations within the database\n
                tag_definitions (list): A list of tag definitions. These are designed by the hospitals to subset their data in ways that the patients can intuitively understand when they create rules. These definitions show:\n
                patient_id (int): The native patient id within the hospital's system\n
                key_name (str): The name of the patient id column within a hospital's system

            Returns:

                smart_patient_health_record (DataFrame): A DataFrame containing the selected patient data

    """
    session = connection['session']
    results = {}
    column_hashes = []
    tables = get_classes(connection['schema'], connection['base'])
    for tag_definition in tags_definitions:
        if tag_definition['table']:
            results[tag_definition['source']] = select_tabular_patient_data(connection, tables, tag_definition, patient_id, key_name)
            columns_to_hash = hash_columns(list(results[tag_definition['source']][0].keys()))
            column_hashes.append(columns_to_hash)
    sorted_hashes = sorted(column_hashes)
    # try:
    #     update_record(proof_id, 'data_selected', 'success', {'columns_hash': "".join(sorted_hashes)}, hospital_id=connection['schema'].upper())
    # except:
    #     print("FAILED TO UPDATE LINEAGE BLOCKCHAIN")
    return results


def parse_sphr(patient_data):
    """Parses the data of the standard Smart Patient Health Record. This converts dates to strings and decimals to floats allowing them to be sent as JSON.

            Parameters:

                patient_data (dict): The patient data that has been selected by the API call

            Returns:

                result (dict): The parsed data that is ready for transmission as JSON
    
    """
    result = {}
    for hospital in patient_data:
        result[hospital] = {}
        for table in patient_data[hospital]['data']:
            df = DataFrame([x for x in patient_data[hospital]['data'][table]])
            df = convert_dates_to_string(df)
            df = convert_decimal_to_float(df)
            result[hospital][table] = df.to_dict('index')
    return result


def get_patient_data(body, jwt):
    """The main function for generating the Smart Patient Health Record
    
            Parameters:

                body (dict): The request body from the API call

            Returns:

                smart_patient_health_record (DataFrame): A DataFrame containing the selected patient data
    """
    results = {}
    jwt_response = validate_jwt(jwt)
    if 'PATIENT' in jwt_response['groupIDs']:
        print("YEAH IT's A PATIENT")
        valid_tags = body['tags']
        print(f"VALID TAGS: {valid_tags}")
        print(f"HOSPITAL IDS: {body['hospital_ids']}")
        rule_ids = 'PATIENT-ACCESSING-OWN-RECORD'
    else:
        valid_tags, rule_ids = validate_rules(body, jwt)
        valid_tags = list(set(valid_tags).intersection(body['tags']))
    if valid_tags != None:
        print("CALLING LINEAGE BLOCKCHAIN")
        # try:
        #     proof_id = create_record(body['serums_id'], rule_ids, body['hospital_ids'])
        # except:
        #     print("UNABLE TO CREATE LINEAGE BLOCKCHAIN")
        proof_id = "TEMP FIX"
        print(f"PROOF ID: {proof_id}")
        for hospital_id in body['hospital_ids']:
            results[hospital_id.upper()] = {}
            hospital, tags_list = hospital_picker(hospital_id)
            tags = select_tags(tags_list, valid_tags)
            connection = setup_connection(hospital)
            id_class = connection['base'].classes.serums_ids
            key_name = select_source_patient_id_name(hospital)
            patient_id = select_source_patient_id_value(connection['session'], 
                                                            id_class, 
                                                            body['serums_id'], key_name)
            data = select_patient_data(connection, tags, patient_id, key_name, proof_id)
            connection['engine'].dispose()
            if len(data) > 0:
                results[hospital_id.upper()]['data'] = data
            elif len(data) <= 0:
                results[hospital_id.upper()]['data'] = {}
            results[hospital_id.upper()]['tags'] = tags
        return results, proof_id
    else:
        return False, None