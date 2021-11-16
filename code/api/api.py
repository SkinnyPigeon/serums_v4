from flask import Flask, request
from flask_cors import CORS
from flask_restplus import Api, Resource, fields
from dotenv import load_dotenv
import jwt

import os
import subprocess


# Functions

from functions.jwt import validate_jwt
from functions.departments import get_department_of_staff_member, get_departments
from functions.ml import get_patient_data_for_ml
from functions.get_source_data import get_patient_data, parse_sphr
from functions.encryption import encrypt_data_with_new_key, encrypt_key
from functions.search import search_for_serums_id
from functions.tags import get_tags
from functions.add_and_remove_users import add_user, remove_user
from functions.lineage import create_record, update_record
from utils.jwt_functions import get_jwt, staff_emails, patient_emails, admin_emails
from data_vaults.satellites import process_satellites
from data_vaults.data_vault import create_data_vault
from data_vaults.hub_post_processing import hub_equalizer
from data_vaults.link_post_processing import add_id_values


# Setting up environment

FLASK_DEBUG = 1

project_folder = subprocess.check_output(
    "pwd", shell=True).decode("utf-8").rstrip()
load_dotenv(os.path.join(project_folder, '.env'))
PORT = os.getenv('PGPORT')
PASSWORD = os.getenv('PGPASSWORD')
BCPASSWORD=os.getenv('BCPASSWORD')

if PORT == None:
    PASSWORD = os.environ.get('PGPASSWORD')
    PORT = os.environ.get('PGPORT')
    BCPASSWORD=os.environ.get('BCPASSWORD')


app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
CORS(app)
api = Api(
    app,
    version='0.5.0',
    title='Smart Patient Health Record API',
    description='Return the encrypted Smart Patient Health Record from the Serums data lake',
)

default_jwt_response = get_jwt(staff_emails['zmc'])
jwt_value = default_jwt_response['body']['resource_obj']['access']
print(f"JWT: {jwt_value}")


default_jwt = "Bearer {jwt_value}".format(jwt_value=jwt_value)
jwt_response = validate_jwt(jwt_value)
print(f"JWT RESPONSE: {jwt_response}")

token = jwt.encode({}, BCPASSWORD, algorithm="HS256")
proof_header = {"Authorization": f"Bearer {token}"}
print(token)

# Models

hello = api.model('Server Check', {
    'hello': fields.String(required=True, description='Quick check that the server is on', example='Welcome to the API. The server is on')
})

parser = api.parser()


# Staff

staff_parser_token = api.parser()
staff_parser_token.add_argument('Authorization', help="The authorization token", location="headers",
                          default=default_jwt)

staff_parser_body = api.parser()
staff_parser_body.add_argument('Authorization', help="The authorization token", location="headers",
                          default=default_jwt)
staff_parser_body_fields = api.model('Return the staff tables', {
    'hospital_id': fields.String(required=True, description='The id of the organisation to return the staff tables for', example=jwt_response['hospital_id'])
})

# Tags

tags_parser = api.parser()
tags_parser.add_argument('Authorization', help="The authorization token", location="headers",
                          default=default_jwt)
tags_fields = api.model('Return the available tags for an institute', {
    'hospital_id': fields.String(required=True, description='The id of the organisation to return the tags tables for', example=jwt_response['hospital_id'])
})

multiple_tags_fields = api.model('Return the available tags for multiple institutes', {
    'hospital_ids': fields.String(required=True, description='The id of the organisation to return the tags tables for', example=['FCRB', 'USTAN', 'ZMC'])
})

# Users

user_parser = api.parser()
user_parser.add_argument('Authorization', help="The authorization token", location="headers",
                          default=default_jwt)
add_user_fields = api.model('Add a new user to the Serums network', {
    'serums_id': fields.Integer(required=True, description='The Serums ID for the patient to add to the network', example=118),
    'patient_id': fields.Integer(required=False, description="The patient\'s id within a hospital\'s internal systems to link to a Serums ID", example=4641202),
    'hospital_id': fields.String(required=True, description='The id of the organisation to add a user to', example='FCRB')
})

remove_user_fields = api.model('Remove a user from the Serums network', {
    'serums_id': fields.Integer(required=True, description='The Serums ID for the patient to add to the network', example=118),
    'hospital_ids': fields.String(required=True, description='A list of the ids of the organisations to remove a user from', example=['ZMC', 'FCRB'])
})


# Search

search_parser = api.parser()
search_parser.add_argument('Authorization', help="The authorization token", location="headers",
                          default=default_jwt)


search_fields = api.model("Search for a patient\'s SERUMS id", {
    'patient_id': fields.Integer(required=False, description="The patient\'s id within a hospital\'s internal systems", example=4641202),
    'first_name': fields.String(required=False, description="The patient\'s first name", example='Joana'),
    'first_surname': fields.String(required=False, description="The patient\'s first surname", example='Soler'),
    'family_name': fields.String(required=False, description="The patient\'s family name", example='Rodríguez'),
    'dob': fields.DateTime(required=False, description="The patient\'s date of birth", example='1935-05-12'),
    'gender': fields.String(required=False, description="The patient\'s gender", example='2'),
    'hospital_id': fields.String(required=False, description="The id of the hospital for the source data", example='FCRB'),
    'public_key': fields.String(required=False, description="The public key used as part of the API's encryption", example="""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDM+DNCybR7LdizOcK1gH2P7dD
sajGUEIoPFp7wjhgKykYkCGVQCvl55g/zdh6UI9Cd/i2IEf5wo+Ct9oihy9SnJSp
3sOp1KESV+ElwdK3vkaIo1AUuj+E8LTe7llyJ61JJdZaozyT0PxM8jB2vIaNEdbO
bURHcIsIDc64L0e1ZQIDAQAB
-----END PUBLIC KEY-----""")
})


# Machine learning

ml_parser = api.parser()
ml_parser.add_argument('Authorization', help="The authorization token", location="headers",
                       default=default_jwt)


# Smart Patient Health Record


sphr_parser = api.parser()
sphr_parser.add_argument('Authorization', help="The authorization token", location="headers",
                         default=default_jwt)

request_fields = api.model('Request Smart Patient Health Record', {
    'serums_id': fields.Integer(required=True, description='The Serums ID for the patient', example=118),
    # 'rule_id': fields.String(required=True, description='The rule id as stored in the blockchain', example='RULE_0df8eb8b-a469-46ae-8119-fbf98fa05b92'),
    # 'tags': fields.String(required=True, description='Rule to be executed', example=['patient_address', 'treatments', 'wearable']),
    'hospital_ids': fields.String(required=True, description='The id of the hospital for the source data', example=['FCRB', 'USTAN', 'ZMC']),
    'public_key': fields.String(required=True, description="The public key used as part of the API's encryption", example="""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDM+DNCybR7LdizOcK1gH2P7dD
sajGUEIoPFp7wjhgKykYkCGVQCvl55g/zdh6UI9Cd/i2IEf5wo+Ct9oihy9SnJSp
3sOp1KESV+ElwdK3vkaIo1AUuj+E8LTe7llyJ61JJdZaozyT0PxM8jB2vIaNEdbO
bURHcIsIDc64L0e1ZQIDAQAB
-----END PUBLIC KEY-----""")
})

reply_fields = api.model('Successful Response', {
    'key': fields.String(required=True, description='The encrypted Fernet key', example="BqKQKHWaCMOozw8U77Cvh0Mj8S+HnvkjuOYzZKrF9L4unP+S9xosAiBF0lJ1hOgZ5mfo0EfyxFdyuBh0ywNBNSUxJdCdnQ+ocwkd14IjsE54VmwTXdTFVcdepR1tjudcIyvVCy+Mxymt4vPh1P7pYTl92wYkEovEpHrs28l++EsaPOgZUiAD7LD5lZ0jZCW5fyFtyBwm8n+aAhNlb0YKnoYKDb88bg9DFyQxazX8SVBBwfmJEklSunVe5s9FULm50BeY1eDS87noQ4nM+so1EPsN5GuBM41KmeySwZZCVYiLh5NfwY+f5efMPbtV683pCL3YoJ89ojYeTlMLJEug=="),
    'data': fields.String(required=True, description='The encrypted patient record', example="gAAAAABeneOIy6q3QxfwmHTjxMjZdP5rxKaQFDbYT-KtJOzgsqZYdnct3qsRcNcAzIrmcnDluR-Q6RLLi8CUthGsa_-7b-VCZrkRO3cLcGKLNuPi2v109dSzXeQ27EazKf49oss4IE11khs6tLZt-yqYCZTz_R84gK6X0BMc0pzoYP-3Qr_h1rV_I6DD3oWHpnbRE4vn86HSR77YajYsi3BGbqPfh-_FJYlgaPWG5USiIXoQYTvJCtHj8kcM9jdhkNICGdlnLkuSZ2A60zx8XpcHImQYd5YzbxENMvWl0Q6SamziiZ5Kl5UXzlyY3IHGpTM-K9T-ycmZj6dkr0hzzqr8lAiWNSinZR2YZDM-diGM7tr8b10hGLF2D1_7-ArvuP12f_aznLgonn4kZtDpro2ImGmzsg-oz01B0pZjNkTvkmOaz32e1ntmvWHBD16yLLHPFdQDw--z0R4i7n_WNJB0Jn3M0sgyHsIkBIB53Pg8ZFKoAxnfACiKIaPJ26JtrVEQ9es6VupfDCT4nUM2WPIiegZ5LmQDXuGBwvw9NrfEW4pC5Sg7CoRv6RvTuT_ywSrhCnd2jePxpdIk0FqTdUsAqancd09IWEnFWQpLxTr348Qq3Dplk5L_dws2H2y8e--AAkBoy08Q-OpT5o8DFS1i9nO84r0KXgWIo4APcmH0UOL53INsgULZDSohzcT675zV8wWxfaja_b3CIVsj54iKs--XgdoSQHijhgasW1UqYgSRqGjW18BTPHUfA1uJ4397U3ZBjZTKCwzgzhr4YBVSBhxMGqEWw8sJCLBXLGxr0MUl1kDRmSptBsc2k7EerGm8JlKI4Xu6XbmXJy3Mjq4aa7Q0elayCnr5izbh9-VJoOEnXMkNgS4PcsEPm3yQdlyk1AlkXK71S4gfUW0DVzfh3NJxWS-xnHPGafu0WnvDdl42wUl-prt6A8AAHWQOQZW1hrGi3gxwCJqQ5vOcqmxXuMdGdCd7xEdBaeuzOFBZSLW5AF1i_0gvmMQAr7YYsV33ZKfX59UHuQG7-Ia9WNRhCRvm2N35jZBQz-F2uenNHd5RFB4h28OvJ5yIVKHVmDAVxrAfq2tf6liqdhECPwqV1BUf13TfF-LDwm93zp4Sp4Enbjur4egN1Pyl2lkGQNQKSWHgAgzq60uNPuzeS-DUm0OvnxmDGaJ-S966lBl7FmPOnoZCJZTk3uXB96m3N4qJ6dZddgqKQDfhBG_Zd87wVQbLjR4bYdBqcH3NY51s1mqjurRzy5RCEqsZCZQL7xCRh5uwyjWZC-oqIp9XBTyqvu7E_j6kWIGX4P0FispRPOxc-LJLoau6Fu1Fp1ZcxBLYBJyRfBAnwIaoRHpoM_zlWUVzkEx_ChUYFkxjCBEJMqf027087_aTB5rdFNxm7etW5RQBPcWwc5KtxTcWo9ae5XfE1aJmRVX17P2rlkXmYD9oiZdOxt21hUktNKM1Y3ZXmbfKLsgteFHv1G8KTN52xPz4y0AYmORD2U1jFn_e0DeQulYQrdgcTys9WLmteZZe1CE7VgBmj-Pd_U9zDMJ8OI8jj3Y7enuWa1TiIyCuHzwnNcT7wDnlcbrpxQfz3zztsdAw6qO1HfJm4VgA0K1UeCQzggySjMUaYMQa20euqLIko-TmdoWPjgIPG0BcVKXbbwyeW178M8ZOMZ32Y-zoZoWs26GwzrKZFolX4EHiNvZlKBa5FJmi4l6aGjT5r4Ipe68EYwsojCCNdtTVO4Ds1tfeNqDT3FmuBktg3aLAwQggQj_Jinjc9hLglTqfKm5TSUEl1iIvt3t9jxv5UKJ06LgXru2YZxX6f255wPmtHVxqqBggVLmhpRKTV2ifq6bQ0AWSexN3PKQ6XXIpsF2UWmtUJABiJmRuy4UOg85uZC4V56JjJFEwiAjw9VBYf5I0nbSOaBEQkSx7-qSF2fXOkYKw7fl09ur9Q40ZkvVDcCtJRemPMpult7sVB_lg3eINTwSq8tqN6AOrsBQpk4UjidQlXatgXKtXWahkINCruy_PHlQQSYCLL9UxUMhA9Xw1WDircweDeS_4IwoSWqrApu1FBRYQemHvGpWO1kGrdhJCph9V548iRIJd5-6q5lWDZiGGWVs5_drjS6LlBgWNOrkxV80Hv1EI0eKm_G9N08HvpEHhcOu1tpRZhLFzPP5PvWlEecXUTbrxJ6RJEJVBRxTDnzW2ngSoHSC10rZdAwcTV6nkeGYcUv_TH-TJxsBe6-3p8kMpJaGaGIJ83e9av0Uegonl0KGbv0XGcmI2MR2rAvgyPN4oSDtsCqu2pYVeIjF8JJq-WmJfKpP8TwiFGQgXRJSyAkOSDfQF3K4f3ucjW-Vca5YMX7q7b3jtV_YyVZDB-pUve6qaRFcgKw7ZDoQAVMY04yNMG61YWpjetPHl4sf3j39_CMinVq5UGHZgvlTErEqBIVaFksee5QDL5M552-ksp9XHuxOewK-QzpKqK7WalNnwI9YxlRJEu1utoOrp3y5ZO-HtLLTGjunL9bwSaFQ_M1MqqNqDHMOUEwuZuiF0zLq61UDT5Z00JXsYbMBRHFqYam6KkTrEub6Dx9pljsQW-J-S0LAJWO5pnsRSCQuoHu6tx3cTnPeCJQMMA1ThqFcrELxmM3EYv4pUZ6AiugwaTmq2Ym4f_UF9hgIr74O8M2xgTUOc2eoLaMuPInf55EzzKtWNuDrGvKsEJAgKzCDn7w==")
})


# Data Vault

dv_parser = api.parser()
dv_parser.add_argument('Authorization', help="The authorization token", location="headers",
                         default=default_jwt)

dv_request_fields = api.model('Request Smart Patient Health Record As Data Vault', {
    'serums_id': fields.Integer(required=True, description='The Serums ID for the patient', example=118),
    # 'rule_id': fields.String(required=True, description='The rule id as stored in the blockchain', example='RULE_0df8eb8b-a469-46ae-8119-fbf98fa05b92'),
    # 'tags': fields.String(required=True, description='Rule to be executed', example=['diagnostic']),
    'hospital_ids': fields.String(required=True, description='The id of the hospital for the source data', example=['FCRB', 'USTAN', 'ZMC']),
    'public_key': fields.String(required=True, description="The public key used as part of the API's encryption", example="""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDM+DNCybR7LdizOcK1gH2P7dD
sajGUEIoPFp7wjhgKykYkCGVQCvl55g/zdh6UI9Cd/i2IEf5wo+Ct9oihy9SnJSp
3sOp1KESV+ElwdK3vkaIo1AUuj+E8LTe7llyJ61JJdZaozyT0PxM8jB2vIaNEdbO
bURHcIsIDc64L0e1ZQIDAQAB
-----END PUBLIC KEY-----""")
})

dv_reply_fields = api.model('Successful Response', {
    'key': fields.String(required=True, description='The encrypted Fernet key', example="BqKQKHWaCMOozw8U77Cvh0Mj8S+HnvkjuOYzZKrF9L4unP+S9xosAiBF0lJ1hOgZ5mfo0EfyxFdyuBh0ywNBNSUxJdCdnQ+ocwkd14IjsE54VmwTXdTFVcdepR1tjudcIyvVCy+Mxymt4vPh1P7pYTl92wYkEovEpHrs28l++EsaPOgZUiAD7LD5lZ0jZCW5fyFtyBwm8n+aAhNlb0YKnoYKDb88bg9DFyQxazX8SVBBwfmJEklSunVe5s9FULm50BeY1eDS87noQ4nM+so1EPsN5GuBM41KmeySwZZCVYiLh5NfwY+f5efMPbtV683pCL3YoJ89ojYeTlMLJEug=="),
    'data': fields.String(required=True, description='The encrypted patient record data vault', example="gAAAAABeneOIy6q3QxfwmHTjxMjZdP5rxKaQFDbYT-KtJOzgsqZYdnct3qsRcNcAzIrmcnDluR-Q6RLLi8CUthGsa_-7b-VCZrkRO3cLcGKLNuPi2v109dSzXeQ27EazKf49oss4IE11khs6tLZt-yqYCZTz_R84gK6X0BMc0pzoYP-3Qr_h1rV_I6DD3oWHpnbRE4vn86HSR77YajYsi3BGbqPfh-_FJYlgaPWG5USiIXoQYTvJCtHj8kcM9jdhkNICGdlnLkuSZ2A60zx8XpcHImQYd5YzbxENMvWl0Q6SamziiZ5Kl5UXzlyY3IHGpTM-K9T-ycmZj6dkr0hzzqr8lAiWNSinZR2YZDM-diGM7tr8b10hGLF2D1_7-ArvuP12f_aznLgonn4kZtDpro2ImGmzsg-oz01B0pZjNkTvkmOaz32e1ntmvWHBD16yLLHPFdQDw--z0R4i7n_WNJB0Jn3M0sgyHsIkBIB53Pg8ZFKoAxnfACiKIaPJ26JtrVEQ9es6VupfDCT4nUM2WPIiegZ5LmQDXuGBwvw9NrfEW4pC5Sg7CoRv6RvTuT_ywSrhCnd2jePxpdIk0FqTdUsAqancd09IWEnFWQpLxTr348Qq3Dplk5L_dws2H2y8e--AAkBoy08Q-OpT5o8DFS1i9nO84r0KXgWIo4APcmH0UOL53INsgULZDSohzcT675zV8wWxfaja_b3CIVsj54iKs--XgdoSQHijhgasW1UqYgSRqGjW18BTPHUfA1uJ4397U3ZBjZTKCwzgzhr4YBVSBhxMGqEWw8sJCLBXLGxr0MUl1kDRmSptBsc2k7EerGm8JlKI4Xu6XbmXJy3Mjq4aa7Q0elayCnr5izbh9-VJoOEnXMkNgS4PcsEPm3yQdlyk1AlkXK71S4gfUW0DVzfh3NJxWS-xnHPGafu0WnvDdl42wUl-prt6A8AAHWQOQZW1hrGi3gxwCJqQ5vOcqmxXuMdGdCd7xEdBaeuzOFBZSLW5AF1i_0gvmMQAr7YYsV33ZKfX59UHuQG7-Ia9WNRhCRvm2N35jZBQz-F2uenNHd5RFB4h28OvJ5yIVKHVmDAVxrAfq2tf6liqdhECPwqV1BUf13TfF-LDwm93zp4Sp4Enbjur4egN1Pyl2lkGQNQKSWHgAgzq60uNPuzeS-DUm0OvnxmDGaJ-S966lBl7FmPOnoZCJZTk3uXB96m3N4qJ6dZddgqKQDfhBG_Zd87wVQbLjR4bYdBqcH3NY51s1mqjurRzy5RCEqsZCZQL7xCRh5uwyjWZC-oqIp9XBTyqvu7E_j6kWIGX4P0FispRPOxc-LJLoau6Fu1Fp1ZcxBLYBJyRfBAnwIaoRHpoM_zlWUVzkEx_ChUYFkxjCBEJMqf027087_aTB5rdFNxm7etW5RQBPcWwc5KtxTcWo9ae5XfE1aJmRVX17P2rlkXmYD9oiZdOxt21hUktNKM1Y3ZXmbfKLsgteFHv1G8KTN52xPz4y0AYmORD2U1jFn_e0DeQulYQrdgcTys9WLmteZZe1CE7VgBmj-Pd_U9zDMJ8OI8jj3Y7enuWa1TiIyCuHzwnNcT7wDnlcbrpxQfz3zztsdAw6qO1HfJm4VgA0K1UeCQzggySjMUaYMQa20euqLIko-TmdoWPjgIPG0BcVKXbbwyeW178M8ZOMZ32Y-zoZoWs26GwzrKZFolX4EHiNvZlKBa5FJmi4l6aGjT5r4Ipe68EYwsojCCNdtTVO4Ds1tfeNqDT3FmuBktg3aLAwQggQj_Jinjc9hLglTqfKm5TSUEl1iIvt3t9jxv5UKJ06LgXru2YZxX6f255wPmtHVxqqBggVLmhpRKTV2ifq6bQ0AWSexN3PKQ6XXIpsF2UWmtUJABiJmRuy4UOg85uZC4V56JjJFEwiAjw9VBYf5I0nbSOaBEQkSx7-qSF2fXOkYKw7fl09ur9Q40ZkvVDcCtJRemPMpult7sVB_lg3eINTwSq8tqN6AOrsBQpk4UjidQlXatgXKtXWahkINCruy_PHlQQSYCLL9UxUMhA9Xw1WDircweDeS_4IwoSWqrApu1FBRYQemHvGpWO1kGrdhJCph9V548iRIJd5-6q5lWDZiGGWVs5_drjS6LlBgWNOrkxV80Hv1EI0eKm_G9N08HvpEHhcOu1tpRZhLFzPP5PvWlEecXUTbrxJ6RJEJVBRxTDnzW2ngSoHSC10rZdAwcTV6nkeGYcUv_TH-TJxsBe6-3p8kMpJaGaGIJ83e9av0Uegonl0KGbv0XGcmI2MR2rAvgyPN4oSDtsCqu2pYVeIjF8JJq-WmJfKpP8TwiFGQgXRJSyAkOSDfQF3K4f3ucjW-Vca5YMX7q7b3jtV_YyVZDB-pUve6qaRFcgKw7ZDoQAVMY04yNMG61YWpjetPHl4sf3j39_CMinVq5UGHZgvlTErEqBIVaFksee5QDL5M552-ksp9XHuxOewK-QzpKqK7WalNnwI9YxlRJEu1utoOrp3y5ZO-HtLLTGjunL9bwSaFQ_M1MqqNqDHMOUEwuZuiF0zLq61UDT5Z00JXsYbMBRHFqYam6KkTrEub6Dx9pljsQW-J-S0LAJWO5pnsRSCQuoHu6tx3cTnPeCJQMMA1ThqFcrELxmM3EYv4pUZ6AiugwaTmq2Ym4f_UF9hgIr74O8M2xgTUOc2eoLaMuPInf55EzzKtWNuDrGvKsEJAgKzCDn7w==")
})


# Name spaces

hello_space = api.namespace('hello', description='Check the server is on')
staff_space = api.namespace('staff_tables', description='Return the staff tables')
tags_space = api.namespace('tags_tables', description='Return the tags tables')
users_space = api.namespace('users', description='Add or remove a user from the Serums network')
ml_space = api.namespace('machine_learning', description='Return the patient data for the machine learning algorithm')
search_space = api.namespace('search', description="Search for a patient\'s SERUMS ID")
sphr_space = api.namespace('smart_patient_health_record', description='Retrieve the Smart Patient Health Record')
dv_space = api.namespace('data_vault', description='Returns the patient data in data vault format')

# Routes

# Server check: Check that the server is actually on


@hello_space.route('/hello')
class ServerCheck(Resource):
    @api.marshal_with(hello)
    def get(self):
        """Checks that the server is online"""
        return {"hello": "Welcome to the API. The server is on"}, 200


# Staff tables: Return details about staff members for use in checking they belong to an appropriate department

@staff_space.route('/get_department_of_staff_member')
class StaffDepartment(Resource):
    @api.expect(staff_parser_token)
    def post(self):
        """Returns the department details of a single staff member based on the serums_id within the body of the jwt verification response"""
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        if response['status_code'] == 200:
            if 'MEDICAL_STAFF' not in response['groupIDs'] and 'HOSPITAL_ADMIN' not in response['groupIDs']:
                return {"message": "Must be either a medical staff or admin to view staff members"}, 404
            try:
                staff_details = get_department_of_staff_member(response)
                return staff_details, 200
            except:
                return {"message": "Unable to retrieve details about staff member"}, 500
        else:
            return {"message": response['message']}, response['status_code']


@staff_space.route('/departments')
class Departments(Resource):
    @api.expect(staff_parser_body, staff_parser_body_fields)
    def post(self):
        """Returns the details about all of the staff members for a healthcare provider"""
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        if response['status_code'] == 200:
            # if 'MEDICAL_STAFF' not in response['groupIDs'] and 'HOSPITAL_ADMIN' not in response['groupIDs']:
            #     return {"message": "Must be either a medical staff or admin to view staff members"}, 404
            try:
                body = request.get_json()
                department_ids = get_departments(body)
                return department_ids, 200
            except:
                return {"message": "Unable to retrieve department ids"}, 500
        else:
            return {"message": response['message']}, response['status_code']


# Tags: Return the lists of available tags during the rule construction in the front end 

@tags_space.route('/tags')
class Tags(Resource):
    @api.expect(tags_parser, tags_fields)
    def post(self):
        """Returns a list of tags and translated tags available for an individual hospital"""
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        if response['status_code'] == 200:
            try:
                body = request.get_json()
                tags = get_tags(body)
                return tags, 200
            except:
                return {"message": "Unable to retrieve tags"}, 500
        else:
            return {"message": response['message']}, response['status_code']

@tags_space.route('/all_tags')
class MultipleTags(Resource):
    @api.expect(tags_parser, multiple_tags_fields)
    def post(self):
        """Returns a list of tags and translated tags available for multiple hospitals"""
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        if response['status_code'] == 200:
            try:
                body = request.get_json()
                multiple_tags = {}
                for hospital_id in body['hospital_ids']:
                    tags = get_tags({'hospital_id': hospital_id})
                    multiple_tags[hospital_id] = tags
                return multiple_tags, 200
            except:
                return {"message": "Unable to retrieve tags"}, 500
        else:
            return {"message": response['message']}, response['status_code']


# Add and remove users

@users_space.route('/add_user')
class AddUser(Resource):
    @api.expect(user_parser, add_user_fields)
    def post(self):
        """Adds a user to a hospital's serums_ids table. This allows their serums id to be linked to any of their available data in the data lake"""
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        if response['status_code'] == 200:
            if 'HOSPITAL_ADMIN' not in response['groupIDs']:
                return {"message": "Must be an admin to add user"}, 404
            try:
                body = request.get_json()
                response = add_user(body['serums_id'], body['patient_id'], body['hospital_id'])
                return response
            except:
                return {"message": "Unable to add user"}, 500
        else:
            return {"message": response['message']}, response['status_code']


@users_space.route('/remove_user')
class RemoveUser(Resource):
    @api.expect(user_parser, remove_user_fields)
    def post(self):
        """Deletes a user from one or more hospital's serums_ids table. This instantly severs the system's ability to access the patient's records even before their medical data is removed during the next nightly ETL process"""
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        if response['status_code'] == 200:
            if 'HOSPITAL_ADMIN' not in response['groupIDs']:
                return {"message": "Must be an admin to remove user"}, 404
            try:
                body = request.get_json()
                response = remove_user(body['serums_id'], body['hospital_ids'])
                return response
            except:
                return {"message": "Unable to remove user"}, 500
        else:
            return {"message": response['message']}, response['status_code']


# Machine Learning: Used by SCCH's machine learning algorithm

@ml_space.route('/analytics')
class MachineLearning(Resource):
    @api.expect(ml_parser)
    def post(self):
        """Returns the data within from a hospital's source system for use by the machine learning algorithm"""
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        if response['status_code'] == 200:
            try:
                patient_data = get_patient_data_for_ml(response)
                return patient_data, 200
            except:
                return {"message": "Unable to retrieve the data for analytics"}, 500
        else:
            return {"message": response['message']}, response['status_code']


# Search function: Returns a Serums ID for an individual patient based on known details such as name, dob, etc.

@search_space.route('/serums_id')
class Search(Resource):
    @api.expect(search_parser, search_fields)
    def post(self):
        """Search function to find a patient's Serums id based on information provided such as: name, dob, gender, native patient id, etc."""
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        if response['status_code'] == 200:
            if 'MEDICAL_STAFF' not in response['groupIDs'] and 'HOSPITAL_ADMIN' not in response['groupIDs']:
                return {"message": "Must be either a medical staff or admin to search for users"}, 404
            try:
                return search_for_serums_id(request.get_json())
            except:
                return {"message": "Unable to retrieve Serums ID"}, 500
        else:
            return {"message": response['message']}, response['status_code']


# Smart Patient Health Record: Returns data based on the rules created by the patients

@sphr_space.route('/get_sphr')
class SPHR(Resource):
    @api.expect(sphr_parser, request_fields)
    def post(self):
        '''Return the Smart Patient Health Record from the Serums data lake'''
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        if response['status_code'] == 200:
            # try:
            body = request.get_json()
            patient_data = get_patient_data(body, jwt)
            if patient_data:
                parse_data = parse_sphr(patient_data)
                return parse_data, 200
            else:
                return {"message": "Incorrect Serums ID provided for logged in patient"}, 404
            # except:
                # {"message": "Unable to create SPHR"}, 500
        else:
            return {"message": response['message']}, response['status_code']


@sphr_space.route('/encrypted')
class SPHR_Encrypted(Resource):
    @api.expect(sphr_parser, request_fields)
    def post(self):
        '''Return the encrypted Smart Patient Health Record from the Serums data lake'''
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        # print(response)
        if response['status_code'] == 200:
            try:
                # body = request.get_json()
                # patient_data, proof_id = get_patient_data(body)
                # print(patient_data)
                # proof_id = 'abc123'
                body = request.get_json()
                patient_data = get_patient_data(body, jwt)
                parse_data = parse_sphr(patient_data)
                encrypted_data, encryption_key, public_key = encrypt_data_with_new_key(parse_data, body['public_key'])
                encrypted_key = encrypt_key(encryption_key, public_key)
                # record_updated = update_record(proof_id, 'encryption', 'success', {'public_key': body['public_key']})
                # print(f"Record updated: {record_updated}")
                return {"data": encrypted_data, "key": encrypted_key}, 200
            except:
                return {"message": "Unable to create SPHR"}, 500
        else:
            return {"message": response['message']}, response['status_code']


# Data Vault space

@dv_space.route('/get_data_vault')
class DV(Resource):
    @api.expect(dv_parser, dv_request_fields)
    def post(self):
        '''Return the unencrypted patient data in data vault format'''
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        print(response)
        if response['status_code'] == 200:
            try:
                body = request.get_json()
                patient_data = get_patient_data(body, jwt)
                satellites = process_satellites(patient_data)
                data_vault = create_data_vault(satellites)
                add_id_values(data_vault['links'])
                hub_equalizer(data_vault['hubs'])
                print(f"DATA VAULT: {data_vault}")
                return data_vault, 200
            except:
                return {"message": "Unable to create data vault"}, 500
        else:
            return {"message": response['message']}, response['status_code']
        

@dv_space.route('/encrypted')
class DVEncrypted(Resource):
    @api.expect(dv_parser, dv_request_fields)
    def post(self):
        '''Return the encrypted patient data in data vault format'''
        jwt = request.headers['Authorization']
        response = validate_jwt(jwt)
        print(response)
        if response['status_code'] == 200:
            try:
                body = request.get_json()
                patient_data = get_patient_data(body, jwt)
                satellites = process_satellites(patient_data)
                data_vault = create_data_vault(satellites)
                add_id_values(data_vault['links'])
                hub_equalizer(data_vault['hubs'])
                encrypted_data, encryption_key, public_key = encrypt_data_with_new_key(data_vault, body['public_key'])
                encrypted_key = encrypt_key(encryption_key, public_key)
                return {"data": encrypted_data, "key": encrypted_key}, 200
            except:
                return {"message": "Unable to create data vault"}, 500
        else:
            return {"message": response['message']}, response['status_code']
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)