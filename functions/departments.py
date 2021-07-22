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

def get_departments(body):
    try:
        metadata = MetaData(schema=body['orgID'].lower())
        Base = automap_base(metadata=metadata)
        engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
        Base.prepare(engine, reflect=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        department_table = Base.classes['hospital_doctors']
        query = select([
            department_table.serums_id, 
            department_table.staff_id,
            department_table.name,
            department_table.department_id,
            department_table.department_name
        ], department_table.serums_id == body['userID'] )

        print(query)

        department_ids = []
        for serums_id, staff_id, name, department_id, department_name in session.execute(query):
            department_ids.append({
                "serums_id": serums_id,
                "staff_id": staff_id,
                "name": name.replace("'", ""),
                "department_id": department_id,
                "department_name": department_name.replace("'", "")
            })
        session.close()
        print(department_ids)
        return department_ids
    except Exception as e:
        return {"error": str(e)}
        # This needs to be better handled



