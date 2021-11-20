"""ADAL/Flask sample for Microsoft Graph """
# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.
import os
import urllib.parse
import uuid
from pprint import pprint
import adal
import flask
import requests
import json

import config
from helpers import api_endpoint, device_flow_session, profile_photo, \
    send_mail, sharing_link, upload_file, search_sites, permissions_check, list_group_members, \
        get_permission, get_user

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # enable non-HTTPS for testing

APP = flask.Flask(__name__, template_folder='static/templates')
APP.debug = True
APP.secret_key = 'development'

SESSION = requests.Session()

def jprint(json_toprint):
    print(json.dumps(json_toprint, indent=4, sort_keys=True))

@APP.route('/')
def homepage():
    """Render the home page."""
    return flask.render_template('homepage.html', sample='Microsoft Graph ')

@APP.route('/login')
def login():
    """Prompt user to authenticate."""
    auth_state = str(uuid.uuid4())
    SESSION.auth_state = auth_state

    # For this sample, the user selects an account to authenticate. Change
    # this value to 'none' for "silent SSO" behavior, and if the user is
    # already authenticated they won't need to re-authenticate.
    prompt_behavior = 'select_account'

    params = urllib.parse.urlencode({'response_type': 'code',
                                     'client_id': config.CLIENT_ID,
                                     'redirect_uri': config.REDIRECT_URI,
                                     'state': auth_state,
                                     'resource': config.RESOURCE,
                                     'prompt': prompt_behavior})

    return flask.redirect(config.AUTHORITY_URL + '/oauth2/authorize?' + params)

@APP.route('/login/authorized')
def authorized():
    """Handler for the application's Redirect Uri."""
    code = flask.request.args['code']
    auth_state = flask.request.args['state']
    if auth_state != SESSION.auth_state:
        raise Exception('state returned to redirect URL does not match!')
    auth_context = adal.AuthenticationContext(config.AUTHORITY_URL, api_version=None)
    token_response = auth_context.acquire_token_with_authorization_code(
        code, config.REDIRECT_URI, config.RESOURCE, config.CLIENT_ID, config.CLIENT_SECRET)
    SESSION.headers.update({'Authorization': f"Bearer {token_response['accessToken']}",
                            'User-Agent': 'adal-sample',
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'SdkVersion': 'sample-python-adal',
                            'return-client-request-id': 'true'})
    return flask.redirect('/graphcall')

@APP.route('/graphcall')
def graphcall():
    """Confirm user authentication by calling Graph and displaying some data."""
    endpoint = config.RESOURCE + config.API_VERSION + '/me'
    http_headers = {'client-request-id': str(uuid.uuid4())}
    graphdata = SESSION.get(endpoint, headers=http_headers, stream=False).json()

    # photo, photo_status_code, _, profile_pic = profile_photo(SESSION, save_as='Przemek')

    # print(f'Upload to OneDrive ------->',
    #       f'https://graph.microsoft.com/beta/me/drive/root/children/{profile_pic}/content')
    # upload_response = upload_file(SESSION, filename=profile_pic)
    # print(28*' ' + f'<Response [{upload_response.status_code}]>')
    
    # print('Create sharing link ------>',
    #       'https://graph.microsoft.com/beta/me/drive/items/{id}/createLink')
    # response, link_url = sharing_link(SESSION, item_id=upload_response.json()['id'])
    # print(28*' ' + f'<Response [{response.status_code}]>',
    #       f'bytes returned: {len(response.text)}')

    # print(link_url)
    
    results = search_sites(SESSION)
    print(28*' ' + f'<Response [{results[0].status_code}]>',
          f'bytes returned: {len(results[0].text)}')
    # pprint(results[0].json())
    results = results[0].json()
    # print(results)
    # send_response = send_mail(session=SESSION,
    #                           subject='email from Microsoft Graph console app',
    #                           recipients=['przemek@y.digital'],
    #                           body='dontworrybehappy',
    #                           attachments=[profile_pic])

    # print(28*' ' + f'<Response [{send_response.status_code}]>')

    total_results = results['value'][0]['hitsContainers'][0]['total']

    print(f'-----------------------\nSearch returns {total_results} results.')

    first_result = results['value'][0]['hitsContainers'][0]['hits'][0]
    item_id = first_result['resource']['id']
    drive_id = first_result['resource']['parentReference']['driveId']

    print('First result:')
    
    jprint(first_result)
    # print(item_id)
    # print(drive_id)

    print(f' ---------- \nAll permissions for this result:')
    results = permissions_check(SESSION, drive_id, item_id)
    jprint(results[0].json())

    permission_id = results[0].json()['value'][0]['id']
    print(permission_id)

    results = get_permission(SESSION, drive_id, item_id, permission_id)
    jprint(results[0].json())


    results = list_group_members(SESSION)
    jprint(results[0].json())

    results = get_user(SESSION)
    jprint(results[0].json())

    return flask.render_template('graphcall.html',
                                 graphdata=graphdata,
                                 endpoint=endpoint,
                                 sample='Y.Digital')

if __name__ == '__main__':
    APP.run()
