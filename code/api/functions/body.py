def validate_body(body, encrypted=False):
    expected_fields = {
        'serums_id': int,
        'tags': list,
        'hospital_ids': list
    }

    errors = []

    for field in expected_fields:
        if field not in body:
            errors.append(f"Missing required field: {field.upper()}")
        if field in body and type(body[field]) != expected_fields[field]:
            errors.append(f"Incorrect data type for {field.upper()}. Expected {str(expected_fields[field])}. Received {str(type(body[field]))}")
    if encrypted:
        if 'public_key' not in body:
            errors.append(f"Missing required field: PUBLIC_KEY")
        if 'public_key' in body and type(body['public_key']) != str:
            errors.append(f"Incorrect data type for PUBLIC_KEY. Expected str. Received {str(type(body['public_key']))}")

    return errors