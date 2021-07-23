#!/usr/bin/env python3

from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import load_only, sessionmaker, defer


import pandas as pd
import os
import subprocess

from dotenv import load_dotenv


# project_folder = subprocess.check_output("pwd", shell=True).decode("utf-8").rstrip()

from sources.tags.fcrb import fcrb_tags
from sources.tags.ustan import ustan_tags
from sources.tags.zmc import zmc_tags

print(ustan_tags)

PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')

# engine = create_engine("postgresql://postgres:{}@localhost:{}/source".format(PASSWORD, PORT))

def check():
    print("CHECKING")