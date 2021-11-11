from sources.keys_and_sats.zmc_keys_and_sats import zmc_sats, zmc_keys
from sources.keys_and_sats.fcrb_keys_and_sats import fcrb_sats, fcrb_keys
from sources.keys_and_sats.ustan_keys_and_sats import ustan_sats, ustan_keys
import datetime
import decimal

def hospital_picker(hospital):
    if hospital == 'ZMC':
        return zmc_sats, zmc_keys
    elif hospital == 'FCRB':
        return fcrb_sats, fcrb_keys
    elif hospital == 'USTAN':
        return ustan_sats, ustan_keys

def process_value(value):
    if isinstance(value, datetime.datetime):
        return value.strftime("%d/%m/%Y %H:%M:%S")
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, datetime.time):
        return value.strftime("%H:%M:%S")
    if isinstance(value, decimal.Decimal):
        return float(value)
    return value

def process_satellites(data):
    results = {}
    for hospital in data:
        results[hospital] = {}
        satellite_definitions, keys = hospital_picker(hospital)
        for table_name in data[hospital]['data']:
            source_data = data[hospital]['data'][table_name]
            results[hospital][table_name] = {}
            results[hospital][table_name]['links'] = satellite_definitions[table_name]['links']
            for satellite_name in satellite_definitions[table_name]:
                if satellite_name != 'links':
                    columns = satellite_definitions[table_name][satellite_name]['columns']
                    results[hospital][table_name][satellite_name] = {}
                    results[hospital][table_name][satellite_name]['hub'] = satellite_definitions[table_name][satellite_name]['hub']
                    results[hospital][table_name][satellite_name]['data'] = [{k: process_value(row[k]) for k in row if k in columns} for row in source_data]
                    results[hospital][table_name][satellite_name]['keys'] = [{k: row[k] for k in row if k in keys} for row in source_data]
    return results

            
