ustan_wearable = {}

ustan_diagnostic = {}

ustan_medication = {}

ustan_patient_details = {}

ustan_patient_address = {}

ustan_patient_appointment = {}

ustan_operations = {}

ustan_documents = {}

ustan_healthcare_providers = {}

ustan_drugs_and_alcohol = {}

ustan_allergies = {}

ustan_additional_information = {}

ustan_treatments = {'tag': 'treatments', 'source': 'ustan.cycles', 'fields': ['chi',
                                                               'regime_id',
                                                               'intention_id',
                                                               'cycle_id',
                                                               'drug_names',
                                                               'diagnosis',
                                                               'init_appointment_date',
                                                               'elapsed_days',
                                                               'interval_days',
                                                               'appointment_date',
                                                               'intention',
                                                               'regime',
                                                               'cycle',
                                                               'p_ps',
                                                               'ps',
                                                               'nausea',
                                                               'vomiting',
                                                               'diarrhoea',
                                                               'constipation',
                                                               'oralMucositis',
                                                               'oesophagitis',
                                                               'neurotoxicity',
                                                               'handFoot',
                                                               'skin',
                                                               'hypersensitivity',
                                                               'fatigue',
                                                               'required_doses'
                                                               ], 'key_lookup': {},
                                                               'table': True, 'graph': False, 'image': False}

ustan_personal = {}

ustan_all_1 = {'tag': 'all', 'source': 'ustan.cycles', 'fields': ['chi',
                                                               'regime_id',
                                                               'intention_id',
                                                               'cycle_id',
                                                               'drug_names',
                                                               'diagnosis',
                                                               'init_appointment_date',
                                                               'elapsed_days',
                                                               'interval_days',
                                                               'appointment_date',
                                                               'intention',
                                                               'regime',
                                                               'cycle',
                                                               'p_ps',
                                                               'ps',
                                                               'nausea',
                                                               'vomiting',
                                                               'diarrhoea',
                                                               'constipation',
                                                               'oralMucositis',
                                                               'oesophagitis',
                                                               'neurotoxicity',
                                                               'handFoot',
                                                               'skin',
                                                               'hypersensitivity',
                                                               'fatigue',
                                                               'required_doses'
                                                               ], 'key_lookup': {},
                                                               'table': True, 'graph': False, 'image': False}
ustan_all_2 = {'tag': 'all', 'source': 'ustan.general', 'fields': ['chi',
                                                                'incidence_date',
                                                                'site_icd_10',
                                                                'name',
                                                                'date_of_birth',
                                                                'first_seen_date',
                                                                'site',
                                                                'histology',
                                                                'primary',
                                                                'metastasis1',
                                                                'metastasis2',
                                                                'metastasis3',
                                                                'smid',
                                                                'smid1',
                                                                'cong_heart_fail_flag',
                                                                'con_tiss_disease_rheum_flag',
                                                                'dementia_flag',
                                                                'pulmonary_flag',
                                                                'con_tiss_flag',
                                                                'diabetes_flag',
                                                                'para_hemiplegia_flag',
                                                                'renal_flag',
                                                                'liver_flag',
                                                                'aids_hiv_flag',
                                                                'cancer_flag',
                                                                'charlson_score',
                                                                'dob',
                                                                'age',
                                                                'simd',
                                                                'simd1',
                                                                'side',
                                                                'gender',
                                                                'age_at_diagnosis',
                                                                'weight',
                                                                'bmi',
                                                                'height',
                                                                'religion',
                                                                'civil_st',
                                                                'ref_hospital',
                                                                'postcode_pre',
                                                                'postcode_suf',
                                                                'stage',
                                                                'stage_detail',
                                                                'tnm_t',
                                                                'tnm_t_detail',
                                                                'tnm_n',
                                                                'tnm_n_detail',
                                                                'tnm_m',
                                                                'perf_stat',
                                                                'smr01_flag',
                                                                'postcode',
                                                                'gp_name',
                                                                'death_flag',
                                                                'survival_days',
                                                                'dat_death',
                                                                'gp_id'
                                                                ], 'key_lookup': {},
                                                                'table': True, 'graph': False, 'image': False}
ustan_all_3 = {'tag': 'all', 'source': 'ustan.intentions', 'fields': ['chi',
                                                                   'patient_id',
                                                                   'intention_id',
                                                                   'intention_seq',
                                                                   'first_intention',
                                                                   'regime_ratio',
                                                                   'cycle_ratio',
                                                                   'intention',
                                                                   'first_regime',
                                                                   'init_appointment_date',
                                                                   'elapsed_days',
                                                                   'appointment_date'
                                                                   ], 'key_lookup': {},
                                                                   'table': True, 'graph': False, 'image': False}
ustan_all_4 = {'tag': 'all', 'source': 'ustan.regimes', 'fields': ['chi',
                                                                'intention_id',
                                                                'regime_id',
                                                                'regime_seq',
                                                                'regime_ratio',
                                                                'cycle_ratio',
                                                                'intention',
                                                                'prev_regime',
                                                                'first_regime',
                                                                'regime',
                                                                'interval_days',
                                                                'elapsed_days',
                                                                'init_appointment_date',
                                                                'appointment_date'
                                                                ], 'key_lookup': {},
                                                                'table': True, 'graph': False, 'image': False}
ustan_all_5 = {'tag': 'all', 'source': 'ustan.patients', 'fields': ['chi',
                                                                 'patient_id',
                                                                 'first_intention',
                                                                 'appointment_date'
                                                                 ], 'key_lookup': {},
                                                                 'table': True, 'graph': False, 'image': False}

ustan_tags = [ustan_diagnostic,
              ustan_medication,
              ustan_patient_details,
              ustan_patient_address,
              ustan_patient_appointment,
              ustan_operations,
              ustan_documents,
              ustan_healthcare_providers,
              ustan_drugs_and_alcohol,
              ustan_allergies,
              ustan_additional_information,
              ustan_treatments,
              ustan_personal,
              ustan_all_1,
              ustan_all_2,
              ustan_all_3,
              ustan_all_4,
              ustan_all_5
              ]
