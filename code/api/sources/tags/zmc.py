#!/usr/bin/env python3

zmc_wearable = {'tag': 'wearable', 'source': 'zmc.wearable', 'fields': [
    'patnr', 'date', 'w_time', 'w_steps', 'w_cad', 'sst', 'sst_time', 'cyc_time', 'cyc_steps', 'cyc_cad'], 'key_lookup': {}, 'table': True, 'graph': True, 'image': False}

zmc_diagnostic = {}

zmc_medication = {}

zmc_patient_details = {}

zmc_patient_address = {}

zmc_patient_appointment = {}

zmc_operations = {}

zmc_documents_1 = {'tag': 'documents', 'source': 'zmc.images', 'fields': ['patnr', 'image_title', 'image'], 'key_lookup': {}, 'table': False, 'graph': False, 'image': True}
zmc_documents_2 = {'tag': 'documents', 'source': 'zmc.documents', 'fields': ['patnr', 'document_title', 'document'], 'key_lookup': {}, 'table': False, 'graph': False, 'image': True}

zmc_healthcare_providers = {}

zmc_drugs_and_alcohol = {}

zmc_allergies = {}

zmc_additional_information = {}

zmc_treatments = {}

zmc_personal = {}

zmc_all_1 = {'tag': 'all', 'source': 'zmc.wearable', 'fields': [
    'patnr', 'date', 'w_time', 'w_steps', 'w_cad', 'sst', 'sst_time', 'cyc_time', 'cyc_steps', 'cyc_cad'], 'key_lookup': {}, 'table': True, 'graph': True, 'image': False}
zmc_all_2 = zmc_diagnostic
zmc_all_3 = zmc_medication
zmc_all_4 = zmc_patient_details
zmc_all_5 = zmc_patient_address
zmc_all_6 = zmc_patient_appointment
zmc_all_7 = zmc_operations
# zmc_all_8 = zmc_documents
zmc_all_9 = zmc_healthcare_providers
zmc_all_10 = zmc_drugs_and_alcohol
zmc_all_12 = zmc_allergies
zmc_all_13 = zmc_additional_information
zmc_all_14 = zmc_treatments
zmc_all_15 = zmc_personal

zmc_tags = [zmc_diagnostic,
            zmc_medication,
            zmc_patient_details,
            zmc_patient_address,
            zmc_patient_appointment,
            zmc_operations,
            zmc_documents_1,
            zmc_documents_2,
            zmc_healthcare_providers,
            zmc_drugs_and_alcohol,
            zmc_allergies,
            zmc_additional_information,
            zmc_treatments,
            zmc_personal,
            zmc_wearable,
            zmc_all_1,
            zmc_all_2,
            zmc_all_3,
            zmc_all_4,
            zmc_all_5,
            zmc_all_6,
            zmc_all_7,
            # zmc_all_8,
            zmc_all_9,
            zmc_all_10,
            zmc_all_12,
            zmc_all_13,
            zmc_all_14,
            zmc_all_15]
