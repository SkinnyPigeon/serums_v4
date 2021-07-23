from cryptography.fernet import Fernet

import os
import json
import base64
import binascii
from datetime import datetime

secret = os.environ.get('BCPASSWORD')

data = {
    'type': 'data_vault_created',
    'hospital_id': 'zmc',
    'status': 'success',
    'content': {
        'schema': '_abc92039'
    },
    'date': str(datetime.today())
}

def encrypt_data(data):
    encryption = Fernet(secret)
    encrypted_data = encryption.encrypt(json.dumps(data).encode())
    return encrypted_data.decode()

encrypted_data = encrypt_data(data)
print(encrypted_data)

def decrypt_data(data):
    decryption = Fernet(secret)
    decrypted_data = decryption.decrypt(data.encode())
    return decrypted_data.decode()

decrypted_data = decrypt_data(encrypted_data)
print(decrypted_data)