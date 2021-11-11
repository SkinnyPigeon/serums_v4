# Imports

from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import CreateSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Time, Text, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import ARRAY, JSON

from dotenv import load_dotenv
from pathlib import Path

import os
import subprocess

project_folder = subprocess.check_output(
    "pwd", shell=True).decode("utf-8").rstrip()
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
engine = create_engine(
    'postgresql://postgres:{}@localhost:{}/source'.format(PASSWORD, PORT))
Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
session = Session()
connection = {'base': base, 'metadata': metadata,
              'engine': engine, 'session': session}

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

class USTAN_Smr01(Base):
    __tablename__ = 'smr01'
    __table_args__ = {'schema': 'ustan'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    incidence_date = Column(DateTime(timezone=False))
    admission_date = Column(DateTime(timezone=False))
    length_of_stay = Column(Integer)
    other_condition1 = Column(String(5))
    other_condition2 = Column(String(5))
    other_condition3 = Column(String(5))
    main_operation_b = Column(String(5))
    discharge_date = Column(DateTime(timezone=False))
    waiting_list_type = Column(Integer)
    main_condition = Column(String(4))
    main_operation_a = Column(String(4))
    marital_status = Column(String(1))
    ethnic_group = Column(String(2))

class USTAN_Smr06(Base):
    __tablename__ = 'smr06'
    __table_args__ = {'schema': 'ustan'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    incidence_date = Column(DateTime(timezone=False))
    er_status = Column(Integer)
    her2_status = Column(Integer)
    stage_clinical_t = Column(String(2))
    stage_clinical_n = Column(String(2))
    stage_clinical_m = Column(String(2))
    num_positive = Column(Integer)
    pathological_tum_size = Column(Integer)

class USTAN_TAGS(Base):
    __tablename__ = 'tags'
    __table_args__ = {'schema': 'ustan'}
    id = Column(Integer, primary_key=True)
    tags = Column(ARRAY(String)) 

class USTAN_Translated_TAGS(Base):
    __tablename__ = 'translated_tags'
    __table_args__ = {'schema': 'ustan'}
    id = Column(Integer, primary_key=True)
    tags = Column(JSON) 


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

class USTAN_ML_Smr01(Base):
    __tablename__ = 'smr01'
    __table_args__ = {'schema': 'ustan_ml'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    incidence_date = Column(DateTime(timezone=False))
    admission_date = Column(DateTime(timezone=False))
    length_of_stay = Column(Integer)
    other_condition1 = Column(String(5))
    other_condition2 = Column(String(5))
    other_condition3 = Column(String(5))
    main_operation_b = Column(String(5))
    discharge_date = Column(DateTime(timezone=False))
    waiting_list_type = Column(Integer)
    main_condition = Column(String(4))
    main_operation_a = Column(String(4))
    marital_status = Column(String(1))
    ethnic_group = Column(String(2))

class USTAN_ML_Smr06(Base):
    __tablename__ = 'smr06'
    __table_args__ = {'schema': 'ustan_ml'}
    id = Column(BigInteger, primary_key=True)
    chi = Column(BigInteger)
    incidence_date = Column(DateTime(timezone=False))
    er_status = Column(Integer)
    her2_status = Column(Integer)
    stage_clinical_t = Column(String(2))
    stage_clinical_n = Column(String(2))
    stage_clinical_m = Column(String(2))
    num_positive = Column(Integer)
    pathological_tum_size = Column(Integer)


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


class FCRB_Diagnostic(Base):
    __tablename__ = 'diagnostic'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    einri = Column(String(4))
    patnr = Column(BigInteger)
    falnr = Column(String(10))
    pernr = Column(String(12))
    lfdnr = Column(String(3))
    dkey1 = Column(String(30))


class FCRB_Episode(Base):
    __tablename__ = 'episode'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    falnr = Column(String(10))
    pernr = Column(String(12))
    einri = Column(String(4))
    falar = Column(String(1))
    patnr = Column(BigInteger)
    bekat = Column(String(40))
    einzg = Column(String(9))
    statu = Column(String(1))
    krzan = Column(String(1))
    enddt = Column(DateTime(timezone=False))
    erdat = Column(DateTime(timezone=False))
    storn = Column(String(1))
    begdt = Column(DateTime(timezone=False))
    casetx = Column(String(20))
    fatxt = Column(String(40))
    enddtx = Column(String(20))


class FCRB_Medical_Specialty(Base):
    __tablename__ = 'medical_specialty'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    orgid = Column(String(8))
    orgna = Column(String(40))

class FCRB_Medication(Base):
    __tablename__ = 'medication'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    einri = Column(String(4))
    patnr = Column(BigInteger)
    falnr = Column(String(10))
    motx = Column(String(60))
    mostx = Column(String(80))
    mpresnr = Column(String(10))
    motypid = Column(String(2))
    pernr = Column(String(10))
    erdat = Column(DateTime(timezone=False))
    storn = Column(String(1))
    stusr = Column(String(10))
    stdat = Column(DateTime(timezone=False))
    stoid = Column(String(15))


class FCRB_Monitoring_Params(Base):
    __tablename__ = 'monitoring_params'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    falnr = Column(String(10))
    vppid = Column(String(15))
    pernr = Column(String(10))
    vbem = Column(String(150))
    datyp = Column(DateTime(timezone=False))
    wertogr = Column(String(20))
    wertugr = Column(String(20))
    wertmax = Column(String(20))
    wertmin = Column(String(20))


class FCRB_Order_Entry(Base):
    __tablename__ = 'order_entry'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    idodr = Column(String(10))
    einri = Column(String(10))
    falnr = Column(String(10))
    patnr = Column(BigInteger)
    pernr = Column(String(12))
    erdat = Column(DateTime(timezone=False))
    orgid = Column(String(8))


class FCRB_Patient_Address(Base):
    __tablename__ = 'patient_address'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    pstlz = Column(String(10))
    stras = Column(String(50))
    land = Column(String(15))
    ort = Column(String(20))
    deck = Column(String(15))
    adrnr = Column(String(5))


class FCRB_Patient(Base):
    __tablename__ = 'patient'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    gschl = Column(String(1))
    nname = Column(String(30))
    vname = Column(String(30))
    gbdat = Column(DateTime(timezone=False))
    gbnam = Column(String(30))
    namzu = Column(String(5))
    glrand = Column(String(20))
    famst = Column(String(10))
    telf1 = Column(String(15))
    rvnum = Column(String(20))


class FCRB_Professional(Base):
    __tablename__ = 'professional'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    pernr = Column(String(10))
    erusr = Column(String(12))
    orgid = Column(String(8))
    gbdat = Column(DateTime(timezone=False))
    begdt = Column(DateTime(timezone=False))
    enddt = Column(DateTime(timezone=False))
    erdat = Column(DateTime(timezone=False))
    rank = Column(String(3))


class FCRB_Vital_Signs(Base):
    __tablename__ = 'vital_signs'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    idvs = Column(String(10))
    patnr = Column(BigInteger)
    falnr = Column(String(10))
    vppid = Column(String(15))
    dttyp = Column(String(10))
    erdat = Column(DateTime(timezone=False))
    typevs = Column(String(9))
    vwert = Column(String(7))
    vbem = Column(String(150))


class FCRB_TAGS(Base):
    __tablename__ = 'tags'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    tags = Column(ARRAY(String))  

class FCRB_Translated_TAGS(Base):
    __tablename__ = 'translated_tags'
    __table_args__ = {'schema': 'fcrb'}
    id = Column(Integer, primary_key=True)
    tags = Column(JSON) 


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


class ZMC_Wearable(Base):
    __tablename__ = 'wearable'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    date = Column(DateTime(timezone=False))
    w_time = Column(Time)
    w_steps = Column(Integer)
    w_cad = Column(Integer)
    sst = Column(Integer)
    sst_time = Column(Numeric(3, 1))
    cyc_time = Column(Time)
    cyc_steps = Column(Integer)
    cyc_cad = Column(Integer)


class ZMC_Images(Base):
    __tablename__ = 'images'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    image_title = Column(String)
    type = Column(String(50))
    date = Column(DateTime(timezone=False))
    image = Column(String)


class ZMC_Documents(Base):
    __tablename__ = 'documents'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    document_title = Column(String)
    type = Column(String(50))
    date = Column(DateTime(timezone=False))
    document = Column(String)


class ZMC_Complaints(Base):
    __tablename__ = 'complaints_and_diagnosis'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    complaints_and_diagnosis = Column(String(50))
    status = Column(String(20))
    specialism = Column(String(20))
    type = Column(String(20))
    name_of_diagnosis_or_complaint = Column(String(30))
    anatomical_location = Column(String(20))
    laterality = Column(String(10))
    begin_date = Column(DateTime(timezone=False))
    end_date = Column(DateTime(timezone=False))


class ZMC_Medication_Agreements(Base):
    __tablename__ = 'medication_agreements'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    medicines = Column(String(30))
    prescribed_by = Column(String(40))
    description = Column(String(50))


class ZMC_Medication_Use(Base):
    __tablename__ = 'medication_use'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    product = Column(String(30))
    use = Column(String(40))
    reason = Column(String(50))


class ZMC_Medical_Aids(Base):
    __tablename__ = 'medical_aids_and_tools'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    product_description = Column(String(50))
    anatomical_location = Column(String(40))
    description = Column(String(50))


class ZMC_Blood_Pressure(Base):
    __tablename__ = 'bloodpressure'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    value  = Column(String(20))
    date = Column(DateTime(timezone=False))
    systolic_bloodpressure = Column(Integer)
    diastolic_bloodpressure = Column(Integer)
    position = Column(String(40))
    measurement_method = Column(String(40))
    manchette_type = Column(String(40))
    measurement_location = Column(String(40))
    description = Column(String(40))


class ZMC_Weight(Base):
    __tablename__ = 'weight'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    measurement = Column(String(10))
    clothes = Column(String(20))
    description = Column(String(40))
    date = Column(DateTime(timezone=False))


class ZMC_Length(Base):
    __tablename__ = 'length'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    measurement = Column(String(10))
    description = Column(String(40))
    date = Column(DateTime(timezone=False))


class ZMC_Registered_Events(Base):
    __tablename__ = 'registered_events'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    type = Column(String(40))
    method = Column(String(40))
    anatomical_location = Column(String(40))
    description = Column(String(255))
    laterality = Column(String(40))
    start_date = Column(DateTime(timezone=False))
    end_date = Column(DateTime(timezone=False))
    indication = Column(String(40))
    executor = Column(String(40))
    requested_by = Column(String(40))
    location = Column(String(100))
    date = Column(DateTime(timezone=False))


class ZMC_Warning(Base):
    __tablename__ = 'warning'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    alerts = Column(String(40))
    begindate = Column(DateTime(timezone=False))
    type = Column(String(40))


class ZMC_Functional_State(Base):
    __tablename__ = 'functional_or_mental_state'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    name = Column(String(40))
    value = Column(String(40))
    date = Column(DateTime(timezone=False))


class ZMC_Living_Situation(Base):
    __tablename__ = 'living_situation'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    house_type = Column(String(40))
    description = Column(String(40))


class ZMC_Drug_Use(Base):
    __tablename__ = 'drug_use'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    substance = Column(String(40))
    quantity = Column(String(40))
    description = Column(String(40))


class ZMC_Alcohol_Use(Base):
    __tablename__ = 'alcohol_use'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    usage_status = Column(String(40))
    quantity = Column(String(40))
    description = Column(String(40))

class ZMC_Tobacco_Use(Base):
    __tablename__ = 'tobacco_use'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    substance = Column(String(40))
    quantity = Column(Integer)
    description = Column(String(40))

class ZMC_Allergies(Base):
    __tablename__ = 'allergies'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger)
    caustive_substance = Column(String(40))
    critical = Column(String(20))
    description = Column(String(40))

class ZMC_Patient_Details(Base):
    __tablename__ = 'patient_details'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    patnr = Column(BigInteger) 
    nname = Column(String(40))
    nnams = Column(String(40))
    vname = Column(String(6))
    titel = Column(String(6))
    gschl = Column(String(10))
    gbdat = Column(DateTime(timezone=False))
    natio = Column(String(3))

class ZMC_TAGS(Base):
    __tablename__ = 'tags'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    tags = Column(ARRAY(String)) 

class ZMC_Translated_TAGS(Base):
    __tablename__ = 'translated_tags'
    __table_args__ = {'schema': 'zmc'}
    id = Column(Integer, primary_key=True)
    tags = Column(JSON) 



Base.metadata.create_all(engine)
engine.dispose()
