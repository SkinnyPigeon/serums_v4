# Imports

from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import CreateSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Time, Text, ForeignKey, BigInteger


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

class_registry = {}
metadata = MetaData()
Base = declarative_base()
base = Base()
engine = create_engine('postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
session = Session()
connection = {'base': base, 'metadata': metadata, 'engine': engine, 'session': session}

# USTAN

class USTAN_Serums_IDs(Base):
    __tablename__ = 'serums_ids'
    __table_args__ = {'schema': 'ustan'}
    id = Column(BigInteger, primary_key=True)
    serums_id = Column(Integer)
    chi = Column(BigInteger)

class USTAN_Hospital_Doctors(Base):
    __tablename__ = 'hospital_doctors'
    __table_args__ = {'schema': 'ustan'}
    id = Column(Integer, primary_key=True)
    serums_id = Column(Integer)
    staff_id = Column(Integer)
    name = Column(String)
    department_id = Column(Integer)
    department_name = Column(String)


class USTAN_Cycles(Base):
    __tablename__ = 'cycles'
    __table_args__ = {'schema': 'ustan'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    regime_id = Column(Integer)
    intention_id = Column(Integer)
    cycle_id = Column(BigInteger)
    drug_names = Column(String(length=30))
    diagnosis = Column(String(length=30))
    init_appointment_date = Column(DateTime(timezone=False))
    elapsed_days = Column(Integer)
    interval_days = Column(Integer)
    appointment_date = Column(DateTime(timezone=False))
    intention = Column(String(length=30))
    regime = Column(String(length=30))
    cycle = Column(Integer)
    p_ps = Column(Integer)
    ps = Column(Integer)
    nausea = Column(Integer)
    vomiting = Column(Integer)
    diarrhoea = Column(Integer)
    constipation = Column(Integer)
    oralMucositis = Column(Integer)
    oesophagitis = Column(Integer)
    cycle = Column(Integer)
    neurotoxicity = Column(Integer)
    handFoot = Column(Integer)
    skin = Column(Integer)
    hypersensitivity = Column(Integer)
    fatigue = Column(Integer)
    required_doses = Column(Numeric(10, 6))

class USTAN_General(Base):
    __tablename__ = 'general'
    __table_args__ = {'schema': 'ustan'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    incidence_date = Column(DateTime(timezone=False))
    site_icd_10 = Column(String(5))
    name = Column(String(30))
    date_of_birth = Column(DateTime(timezone=False))
    first_seen_date = Column(DateTime(timezone=False))
    site = Column(String(5))
    histology = Column(Integer)
    primary = Column(Integer)
    metastasis1 = Column(String(5))
    metastasis2 = Column(String(5))
    metastasis3 = Column(String(5))
    smid = Column(Integer)
    smid1 = Column(Integer)
    cong_heart_fail_flag = Column(Integer)
    con_tiss_disease_rheum_flag = Column(Integer)
    dementia_flag = Column(Integer)
    pulmonary_flag = Column(Integer)
    con_tiss_flag = Column(Integer)
    diabetes_flag = Column(Integer)
    para_hemiplegia_flag = Column(Integer)
    renal_flag = Column(Integer)
    liver_flag = Column(Integer)
    aids_hiv_flag = Column(Integer)
    cancer_flag = Column(Integer)
    charlson_score = Column(Integer)
    dob = Column(DateTime(timezone=False))
    age = Column(Integer)
    simd = Column(Numeric(5, 2))
    simd1 = Column(Numeric(5, 2))
    side = Column(Integer)
    gender = Column(Integer)
    age_at_diagnosis = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    bmi = Column(Numeric(5, 2))
    height = Column(Numeric(5, 2))
    religion = Column(Integer)
    civil_st = Column(Integer)
    ref_hospital = Column(Integer)
    postcode_pre = Column(String(2))
    postcode_suf = Column(String(5))
    stage = Column(Integer)
    stage_detail = Column(String(2))
    tnm_t = Column(Integer)
    tnm_t_detail = Column(String(2))
    tnm_n = Column(Integer)
    tnm_n_detail = Column(String(2))
    tnm_m = Column(Integer)
    perf_stat = Column(Integer)
    smr01_flag = Column(Integer)
    postcode = Column(String(7))
    gp_name = Column(String(30))
    death_flag = Column(Integer)
    survival_days = Column(Integer)
    dat_death = Column(DateTime(timezone=False))
    gp_id = Column(Integer)

class USTAN_Intentions(Base):
    __tablename__ = 'intentions'
    __table_args__ = {'schema': 'ustan'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    patient_id = Column(Integer)
    intention_id = Column(Integer)
    intention_seq = Column(Integer)
    first_intention = Column(String(12))
    regime_ratio = Column(Integer)
    cycle_ratio = Column(Integer)
    intention = Column(String(12))
    first_regime = Column(String(16))
    init_appointment_date = Column(DateTime(timezone=False))
    elapsed_days = Column(Integer)
    appointment_date = Column(DateTime(timezone=False))
    

class USTAN_Patients(Base):
    __tablename__ = 'patients'
    __table_args__ = {'schema': 'ustan'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    patient_id = Column(Integer)
    first_intention = Column(String(12))
    appointment_date = Column(DateTime(timezone=False))


class USTAN_Regimes(Base):
    __tablename__ = 'regimes'
    __table_args__ = {'schema': 'ustan'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    intention_id = Column(Integer)
    regime_id = Column(Integer)
    regime_seq = Column(Integer)
    regime_ratio = Column(Integer)
    cycle_ratio = Column(Integer)
    intention = Column(String(12))
    prev_regime = Column(String(16))
    first_regime = Column(String(16))
    regime = Column(String(16))
    interval_days = Column(Integer)
    elapsed_days = Column(Integer)
    init_appointment_date = Column(DateTime(timezone=False))
    appointment_date = Column(DateTime(timezone=False))


# USTAN MACHINE LEARNING

class USTAN_ML_Serums_IDs(Base):
    __tablename__ = 'serums_ids'
    __table_args__ = {'schema': 'ustan_ml'}
    id = Column(BigInteger, primary_key=True)
    serums_id = Column(Integer)
    chi = Column(BigInteger)


class USTAN_ML_Cycles(Base):
    __tablename__ = 'cycles'
    __table_args__ = {'schema': 'ustan_ml'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    regime_id = Column(Integer)
    intention_id = Column(Integer)
    cycle_id = Column(BigInteger)
    drug_names = Column(String(length=30))
    diagnosis = Column(String(length=30))
    init_appointment_date = Column(DateTime(timezone=False))
    elapsed_days = Column(Integer)
    interval_days = Column(Integer)
    appointment_date = Column(DateTime(timezone=False))
    intention = Column(String(length=30))
    regime = Column(String(length=30))
    cycle = Column(Integer)
    p_ps = Column(Integer)
    ps = Column(Integer)
    nausea = Column(Integer)
    vomiting = Column(Integer)
    diarrhoea = Column(Integer)
    constipation = Column(Integer)
    oralMucositis = Column(Integer)
    oesophagitis = Column(Integer)
    cycle = Column(Integer)
    neurotoxicity = Column(Integer)
    handFoot = Column(Integer)
    skin = Column(Integer)
    hypersensitivity = Column(Integer)
    fatigue = Column(Integer)
    required_doses = Column(Numeric(10, 6))

class USTAN_ML_General(Base):
    __tablename__ = 'general'
    __table_args__ = {'schema': 'ustan_ml'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    incidence_date = Column(DateTime(timezone=False))
    site_icd_10 = Column(String(5))
    name = Column(String(30))
    date_of_birth = Column(DateTime(timezone=False))
    first_seen_date = Column(DateTime(timezone=False))
    site = Column(String(5))
    histology = Column(Integer)
    primary = Column(Integer)
    metastasis1 = Column(String(5))
    metastasis2 = Column(String(5))
    metastasis3 = Column(String(5))
    smid = Column(Integer)
    smid1 = Column(Integer)
    cong_heart_fail_flag = Column(Integer)
    con_tiss_disease_rheum_flag = Column(Integer)
    dementia_flag = Column(Integer)
    pulmonary_flag = Column(Integer)
    con_tiss_flag = Column(Integer)
    diabetes_flag = Column(Integer)
    para_hemiplegia_flag = Column(Integer)
    renal_flag = Column(Integer)
    liver_flag = Column(Integer)
    aids_hiv_flag = Column(Integer)
    cancer_flag = Column(Integer)
    charlson_score = Column(Integer)
    dob = Column(DateTime(timezone=False))
    age = Column(Integer)
    simd = Column(Numeric(5, 2))
    simd1 = Column(Numeric(5, 2))
    side = Column(Integer)
    gender = Column(Integer)
    age_at_diagnosis = Column(Numeric(5, 2))
    weight = Column(Numeric(5, 2))
    bmi = Column(Numeric(5, 2))
    height = Column(Numeric(5, 2))
    religion = Column(Integer)
    civil_st = Column(Integer)
    ref_hospital = Column(Integer)
    postcode_pre = Column(String(2))
    postcode_suf = Column(String(5))
    stage = Column(Integer)
    stage_detail = Column(String(2))
    tnm_t = Column(Integer)
    tnm_t_detail = Column(String(2))
    tnm_n = Column(Integer)
    tnm_n_detail = Column(String(2))
    tnm_m = Column(Integer)
    perf_stat = Column(Integer)
    smr01_flag = Column(Integer)
    postcode = Column(String(7))
    gp_name = Column(String(30))
    death_flag = Column(Integer)
    survival_days = Column(Integer)
    dat_death = Column(DateTime(timezone=False))
    gp_id = Column(Integer)

class USTAN_ML_Intentions(Base):
    __tablename__ = 'intentions'
    __table_args__ = {'schema': 'ustan_ml'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    patient_id = Column(Integer)
    intention_id = Column(Integer)
    intention_seq = Column(Integer)
    first_intention = Column(String(12))
    regime_ratio = Column(Integer)
    cycle_ratio = Column(Integer)
    intention = Column(String(12))
    first_regime = Column(String(16))
    init_appointment_date = Column(DateTime(timezone=False))
    elapsed_days = Column(Integer)
    appointment_date = Column(DateTime(timezone=False))
    

class USTAN_ML_Patients(Base):
    __tablename__ = 'patients'
    __table_args__ = {'schema': 'ustan_ml'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    patient_id = Column(Integer)
    first_intention = Column(String(12))
    appointment_date = Column(DateTime(timezone=False))


class USTAN_ML_Regimes(Base):
    __tablename__ = 'regimes'
    __table_args__ = {'schema': 'ustan_ml'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    intention_id = Column(Integer)
    regime_id = Column(Integer)
    regime_seq = Column(Integer)
    regime_ratio = Column(Integer)
    cycle_ratio = Column(Integer)
    intention = Column(String(12))
    prev_regime = Column(String(16))
    first_regime = Column(String(16))
    regime = Column(String(16))
    interval_days = Column(Integer)
    elapsed_days = Column(Integer)
    init_appointment_date = Column(DateTime(timezone=False))
    appointment_date = Column(DateTime(timezone=False))


# FCRB

class FCRB_Serums_IDs(Base):
    __tablename__ = 'serums_ids'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(BigInteger, primary_key=True)
    serums_id = Column(Integer)
    patnr = Column(BigInteger)

class FCRB_Hospital_Doctors(Base):
    __tablename__ = 'hospital_doctors'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    serums_id = Column(Integer)
    staff_id = Column(Integer)
    name = Column(String)
    department_id = Column(Integer)
    department_name = Column(String)



# # ZMC

class ZMC_Serums_IDs(Base):
    __tablename__ = 'serums_ids'
    __table_args__ = {'schema': 'zmc'}
    id = Column(BigInteger, primary_key=True)
    serums_id = Column(Integer)
    patnr = Column(BigInteger)

class ZMC_Hospital_Doctors(Base):
    __tablename__ = 'hospital_doctors'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    serums_id = Column(Integer)
    staff_id = Column(Integer)
    name = Column(String)
    department_id = Column(Integer)
    department_name = Column(String)


Base.metadata.create_all(engine)
engine.dispose()