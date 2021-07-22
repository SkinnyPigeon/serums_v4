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

def get_patient_data(body):
    try:
        metadata = MetaData(schema=body['orgID'].lower() + "_ml")
        Base = automap_base(metadata=metadata)
        engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
        Base.prepare(engine, reflect=True)
        Session = sessionmaker(bind=engine)
        session = Session()
    except Exception as e:
        return {"error": str(e)}