from sqlalchemy import create_engine, MetaData, select, delete
from sqlalchemy.ext.automap import automap_base
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


def remove_user(serums_id, hospital_ids):
    """Deletes a user from one or more hospital's serums_ids table. This instantly severs the system's ability to access the patient's records even before their medical data is removed during the next nightly ETL process
    
            Parameters:

                serums_id (int): The Serums ID of the patient who is to be removed from the system\n
                hospital_ids (list): A list of hospital IDs from which to remove the patient's link to. This can be one of more, and does not have to be all of the hospitals they have linked

            Response:

                response (tup): A response message based on whether or not the action was successful plus a response status code e.g. 200
    """
    for hospital_id in hospital_ids:
        schema = hospital_id.lower()
        connection = setup_connection(schema)
        try:
            serums_ids_table = connection['metadata'].tables[f'{schema}.serums_ids']
            print(serums_ids_table)
            stmt = serums_ids_table.delete().where(serums_ids_table.c.serums_id == serums_id)
            connection['engine'].execute(stmt)
            connection['engine'].dispose()
        except:
            return {"message": f"Error removing user from {hospital_id}"}, 500


    return {"message": f"User successfully removed from {hospital_ids}"}, 200


def add_user(serums_id, patient_id, hospital_id):
    pass