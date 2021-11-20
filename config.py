"""Configuration settings for running the Python auth samples locally.

In a production deployment, this information should be saved in a database or
other secure storage mechanism.
"""
#YDigital
CLIENT_ID = '431e6bcb-57d7-4029-b366-99cb55fb157b'
CLIENT_SECRET = '.37K3CQ~Q22ab7_d7G.m.9~RknB_O~55A5'


#KNB
# CLIENT_ID = 'd1f3f353-6aa8-492c-b0bd-e5108e587546'
# CLIENT_SECRET = '9U_.m~HeDC_DO-W0BalO2wQqZtpj0wM-ZJ'


REDIRECT_URI = 'http://localhost:5000/login/authorized'
# AUTHORITY_URL ending determines type of account that can be authenticated:
# /organizations = organizational accounts only
# /consumers = MSAs only (Microsoft Accounts - Live.com, Hotmail.com, etc.)
# /common = allow both types of accounts
AUTHORITY_URL = 'https://login.microsoftonline.com/common'

AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
TOKEN_ENDPOINT = '/oauth2/v2.0/token'

RESOURCE = 'https://graph.microsoft.com/'
API_VERSION = 'v1.0'
SCOPES = ['User.Read'] # Add other scopes/permissions as needed.


# This code can be removed after configuring CLIENT_ID and CLIENT_SECRET above.
if 'ENTER_YOUR' in CLIENT_ID or 'ENTER_YOUR' in CLIENT_SECRET:
    print('ERROR: config.py does not contain valid CLIENT_ID and CLIENT_SECRET')
    import sys
    sys.exit(1)
