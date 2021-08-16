from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.ext.automap import automap_base

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

def get_tags(body):
    schema = body['hospital_id'].lower()
    engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
    metadata = MetaData(bind=engine, schema=schema)
    metadata.reflect(engine)
    Base = automap_base(metadata=metadata)
    Base.prepare()
    try:
        tags_table = metadata.tables[f'{schema}.tags']
        stmt = (select ([tags_table.c.tags]))
        tags = engine.execute(stmt).fetchone()
        translate_tags_table = metadata.tables[f'{schema}.translated_tags']
        stmt = (select([translate_tags_table.c.tags]))
        translate_tags = engine.execute(stmt).fetchone()
        results = {}
        results['tags'] = tags[0]
        results['translated'] = translate_tags[0]
        engine.dispose()
        return results
    except Exception as e:
        print(e)
        engine.dispose()
        return {"error": str(e)}