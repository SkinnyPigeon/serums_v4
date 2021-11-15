from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
import subprocess
from functions.jwt import validate_jwt

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')

def get_department_of_staff_member(body):
    """Returns the details about a single staff member for a healthcare provider.

            Parameters:

                body (dict): The response body of the validate_jwt function

            Returns:

                department_ids (list):  A list of dictionaries containing the details of a single staff member for a particular healthcare provider
    """
    try:
        metadata = MetaData(schema=body['hospital_id'].lower())
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
        ], department_table.serums_id == body['serums_id'] )

        department_ids = []
        for serums_id, staff_id, name, department_id, department_name in session.execute(query):
            department_ids.append({
                "serums_id": serums_id,
                "staff_id": staff_id,
                "name": name.replace("'", ""),
                "department_id": department_id,
                "department_name": department_name.replace("'", "").strip()
            })
        session.close()
        return department_ids
    except Exception as e:
        return {"error": str(e)}
        # This needs to be better handled


def get_departments(body):
    """Returns the details about all of the staff members for a healthcare provider.

            Parameters:

                body (dict): The request body that must include 'hospital_id'

            Returns:

                department_ids (list):  A list of dictionaries containing the details of staff members for a particular healthcare provider
    """
    try:
        metadata = MetaData(schema=body['hospital_id'].lower())
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
        ])

        department_ids = []
        for serums_id, staff_id, name, department_id, department_name in session.execute(query):
            department_ids.append({
                "serums_id": serums_id,
                "staff_id": staff_id,
                "name": name.replace("'", ""),
                "department_id": department_id,
                "department_name": department_name.replace("'", "").strip()
            })
        session.close()
        return department_ids
    except Exception as e:
        return {"error": str(e)}


def check_staff_member(jwt):
    id_and_department = {}
    jwt_response = validate_jwt(jwt)
    print(jwt_response)
    if jwt_response['status_code'] == 200 and 'PATIENT' not in jwt_response['groupIDs']:
        staff_response = get_departments(jwt_response)
        if staff_response:
            for staff_member in staff_response:
                if jwt_response['serums_id'] == staff_member['serums_id']:
                    id_and_department['id'] = jwt_response['serums_id']
                    id_and_department['department'] = staff_member['department_id']
    else:
        print(jwt_response['groupIDs'])
    return id_and_department