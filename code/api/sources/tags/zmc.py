zmc_wearable_1 = {'tag': 'wearable', 'source': 'zmc.wearable', 'fields': ['patnr', 'date', 'w_time', 'w_steps', 'w_cad', 'sst', 'sst_time', 'cyc_time', 'cyc_steps', 'cyc_cad'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_wearable_2 = {'tag': 'wearable', 'source': 'zmc.medical_aids_and_tools', 'fields': ['patnr', 'product_description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_diagnostic_1 = {'tag': 'diagnostic', 'source': 'zmc.complaints_and_diagnosis', 'fields': ['patnr', 'complaints_and_diagnosis', 'status', 'specialism', 'type', 'name_of_diagnosis_or_complaint', 'anatomical_location', 'laterality', 'begin_date', 'end_date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_diagnostic_2 = {'tag': 'diagnostic', 'source': 'zmc.bloodpressure', 'fields': ['patnr', 'value', 'position', 'description', 'date', 'systolic_bloodpressure', 'diastolic_bloodpressure', 'measurement_method', 'manchette_type', 'measurement_location', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_diagnostic_3 = {'tag': 'diagnostic', 'source': 'zmc.weights', 'fields': ['patnr', 'measurement', 'clothes', 'description', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_diagnostic_4 = {'tag': 'diagnostic', 'source': 'zmc.length', 'fields': ['patnr', 'measurement', 'description', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_diagnostic_5 = {'tag': 'diagnostic', 'source': 'zmc.registered_events', 'fields': ['patnr', 'type', 'method', 'anatomical_location', 'laterality', 'start_date', 'end_date', 'indication', 'requested_by', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}        
zmc_diagnostic_6 = {'tag': 'diagnostic', 'source': 'zmc.functional_or_mental_state', 'fields': ['patnr', 'name', 'value', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_medication_1 = {'tag': 'medication', 'source': 'zmc.complaints_and_diagnosis', 'fields': ['patnr', 'complaints_and_diagnosis', 'status', 'specialism', 'type', 'name_of_diagnosis_or_complaint', 'begin_date', 'end_date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_medication_2 = {'tag': 'medication', 'source': 'zmc.medication_agreements', 'fields': ['patnr', 'medicines', 'prescribed_by', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_medication_3 = {'tag': 'medication', 'source': 'zmc.medication_use', 'fields': ['patnr', 'product', 'use', 'reason'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_medication_4 = {'tag': 'medication', 'source': 'zmc.medical_aids_and_tools', 'fields': ['patnr', 'product_description', 'anatomical_location', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_medication_5 = {'tag': 'medication', 'source': 'zmc.functional_or_mental_state', 'fields': ['patnr', 'name', 'value', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_medication_6 = {'tag': 'medication', 'source': 'zmc.allergies', 'fields': ['patnr', 'caustive_substance', 'critical', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_operations_1 = {'tag': 'operations', 'source': 'zmc.complaints_and_diagnosis', 'fields': ['patnr', 'complaints_and_diagnosis', 'status', 'specialism', 'type', 'name_of_diagnosis_or_complaint', 'anatomical_location', 'laterality', 'begin_date', 'end_date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_operations_2 = {'tag': 'operations', 'source': 'zmc.medical_aids_and_tools', 'fields': ['patnr', 'product_description', 'anatomical_location'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_operations_3 = {'tag': 'operations', 'source': 'zmc.registered_events', 'fields': ['patnr', 'type'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_operations_4 = {'tag': 'operations', 'source': 'zmc.warning', 'fields': ['patnr', 'alerts', 'begindate', 'type'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_documents_1 = {'tag': 'documents', 'source': 'zmc.complaints_and_diagnosis', 'fields': ['patnr', 'complaints_and_diagnosis', 'status', 'specialism', 'type', 'name_of_diagnosis_or_complaint', 'anatomical_location', 'laterality', 'begin_date', 'end_date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_documents_2 = {'tag': 'documents', 'source': 'zmc.medical_aids_and_tools', 'fields': ['patnr', 'product_description', 'anatomical_location', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_documents_3 = {'tag': 'documents', 'source': 'zmc.registered_events', 'fields': ['type', 'method', 'anatomical_location', 'laterality', 'start_date', 'end_date', 'indication', 'executor', 'requested_by', 'location', 'description', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_documents_4 = {'tag': 'documents', 'source': 'zmc.warning', 'fields': ['alerts', 'begindate', 'type'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_treatments_1 = {'tag': 'treatments', 'source': 'zmc.complaints_and_diagnosis', 'fields': ['complaints_and_diagnosis', 'status', 'specialism', 'type', 'name_of_diagnosis_or_complaint', 'anatomical_location', 'laterality', 'begin_date', 'end_date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_treatments_2 = {'tag': 'treatments', 'source': 'zmc.medication_agreements', 'fields': ['medicines', 'prescribed_by'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_treatments_3 = {'tag': 'treatments', 'source': 'zmc.medical_aids_and_tools', 'fields': ['product_description', 'anatomical_location', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_treatments_4 = {'tag': 'treatments', 'source': 'zmc.warning', 'fields': ['alerts', 'begindate', 'type'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_treatments_5 = {'tag': 'treatments', 'source': 'zmc.functional_or_mental_state', 'fields': ['name', 'value', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_treatments_6 = {'tag': 'treatments', 'source': 'zmc.living_situation', 'fields': ['house_type', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_treatments_7 = {'tag': 'treatments', 'source': 'zmc.drug_use', 'fields': ['substance', 'quantity'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_treatments_8 = {'tag': 'treatments', 'source': 'zmc.alcohol_use', 'fields': ['usage_status', 'quantity'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_treatments_9 = {'tag': 'treatments', 'source': 'zmc.tobacco_use', 'fields': ['substance', 'quantity'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_treatments_10 = {'tag': 'treatments', 'source': 'zmc.allergies', 'fields': ['caustive_substance', 'critical', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_healthcare_providers_1 = {'tag': 'healthcare_providers', 'source': 'zmc.medication_agreements', 'fields': ['prescribed_by'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_healthcare_providers_2 = {'tag': 'healthcare_providers', 'source': 'zmc.registered_events', 'fields': ['executor'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_allergies_1 = {'tag': 'allergies', 'source': 'zmc.medication_agreements', 'fields': ['medicines'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_allergies_2 = {'tag': 'allergies', 'source': 'zmc.allergies', 'fields': ['caustive_substance', 'critical', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_personal_1 = {'tag': 'personal', 'source': 'zmc.weights', 'fields': ['measurement', 'clothes', 'description', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_personal_2 = {'tag': 'personal', 'source': 'zmc.length', 'fields': ['measurement', 'description', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_personal_3 = {'tag': 'personal', 'source': 'zmc.functional_or_mental_state', 'fields': ['name', 'value', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_personal_4 = {'tag': 'personal', 'source': 'zmc.living_situation', 'fields': ['house_type', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_personal_5 = {'tag': 'personal', 'source': 'zmc.drug_use', 'fields': ['substance', 'quantity', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_personal_6 = {'tag': 'personal', 'source': 'zmc.alcohol_use', 'fields': ['usage_status', 'quantity', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_personal_7 = {'tag': 'personal', 'source': 'zmc.tobacco_use', 'fields': ['substance', 'quantity', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_personal_8 = {'tag': 'personal', 'source': 'zmc.allergies', 'fields': ['caustive_substance', 'critical', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_patient_appointments_ = {'tag': 'patient_appointments', 'source': 'zmc.registered_events', 'fields': ['type', 'executor', 'location', 'date'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_drugs_and_alcohol_1 = {'tag': 'drugs_and_alcohol', 'source': 'zmc.drug_use', 'fields': ['substance', 'quantity', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_drugs_and_alcohol_2 = {'tag': 'drugs_and_alcohol', 'source': 'zmc.alcohol_use', 'fields': ['usage_status', 'quantity', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}
zmc_drugs_and_alcohol_3 = {'tag': 'drugs_and_alcohol', 'source': 'zmc.tobacco_use', 'fields': ['substance', 'quantity', 'description'], 'key_lookup': {}, 'table': True, 'graph': False, 'image': False}

zmc_tags = [

]
