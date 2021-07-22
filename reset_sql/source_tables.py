# Imports

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Time, Text, Numeric, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY, JSON

from dotenv import load_dotenv
from pathlib import Path

import os
import subprocess

project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')


engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT), echo='debug')

# USTAN

class USTAN_Serums_IDs(Base):
    __tablename__ = 'serums_ids'
    __table_args__ = {'schema': 'ustan'}
    serums_id = Column(Integer, primary_key=True)
    chi = Column(BigInteger, primary_key=True)

class USTAN_Hospital_Doctors(Base):
    __tablename__ = 'hospital_doctors'
    __table_args__ = {'schema': 'ustan'}
    id = Column(Integer, primary_key=True)
    serums_id = Column(Integer)
    staff_id = Column(Integer)
    name = Column(String)
    department_id = Column(Integer)
    department_name = Column(String)


# USTAN MACHINE LEARNING


Base.metadata.create_all(engine)