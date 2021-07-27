from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_der_public_key

from cryptography.fernet import Fernet

import os
import json
import base64
import binascii
from datetime import datetime

secret = os.environ.get('BCPASSWORD')

# data = {
#     'type': 'data_vault_created',
#     'hospital_id': 'zmc',
#     'status': 'success',
#     'content': {
#         'schema': '_abc92039'
#     },
#     'date': str(datetime.today())
# }

def encrypt_data(data):
    encryption = Fernet(secret)
    encrypted_data = encryption.encrypt(json.dumps(data).encode())
    return encrypted_data.decode(), encryption

def decrypt_data(data):
    decryption = Fernet(secret)
    decrypted_data = decryption.decrypt(data.encode())
    return decrypted_data.decode()


def encrypt_data_with_new_key(data, public_key):
    public_key = public_key.encode()
    public_key = load_pem_public_key(public_key, backend=default_backend())
    data = json.dumps(data).encode()
    encryption_key = Fernet.generate_key()
    encryption = Fernet(encryption_key)
    encrypted_data = encryption.encrypt(data).decode()

    return encrypted_data, encryption_key, public_key

def encrypt_key(key_to_encrypt, public_key):
    encrypted_key = public_key.encrypt(
        key_to_encrypt,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    key = binascii.b2a_base64(encrypted_key, newline=False)
    return key.decode()