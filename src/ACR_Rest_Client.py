# POC for ACR token creation

import adal # <= ToDo: should probably be using MSAL
import requests
import os
import json
# can use this to debug requests
import http.client

# Registry Token mgmt features are not yet available in the SDK
# can replace using env vars with KeyVault entries
tenant = os.environ['AZURE_TENANT_ID']
authority_url = 'https://login.microsoftonline.com/' + tenant
client_id = os.environ['AZURE_CLIENT_ID']
client_secret = os.environ['AZURE_CLIENT_SECRET']
resource = 'https://management.azure.com'
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

context = adal.AuthenticationContext(authority_url)
token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
params = {}
scope = f'/subscriptions/{subscription_id}'
resourceGroupName = 'akstests'
registry= 'edwinspoctests' # replace with your own ACR registry
params = {}
# we need this for the preview token features
apiversion = '2021-08-01-preview'
acrTokenResourceApi = f'registries/{registry}/tokens'
acrScopeMapResourceApi = f'registries/{registry}/scopeMaps'


def decode_list_tokens_response(response):
    # print all the token names:
    if response:
        # read the JSON content
        json_resp = response.json()
        # get the items
        items = json_resp['value']
        for item in items:
            print('Token: ', item['name'])
            print('  Scope: ', item['properties']['scopeMapId'])

def decode_list_scopemaps_response(response):
    # print all the token names:
    if response:
        # read the JSON content
        json_resp = response.json()
        # get the items
        items = json_resp['value']
        for item in items:
            print('ScopeMap: ', item['name'])
            print('  Description: ', item['properties']['description'])
            print('  Actions: ', item['properties']['actions'])

# List token Ids
def decode_token_ids(response):
    # print all the token names:
    if response:
        # read the JSON content
        json_resp = response.json()
        # get the items
        items = json_resp['value']
        ids = []
        for item in items:
            ids.append(item["id"])
        return ids

# list ops
# GET https://management.azure.com/providers/Microsoft.ContainerRegistry/operations?api-version=2019-05-01
# url = f'{resource}providers/Microsoft.ContainerRegistry/operations?api-version=2019-05-01'

# list tokens
def get_list_token_url():
    url = f'{resource}/{scope}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/{acrTokenResourceApi}?api-version=2021-08-01-preview'
    return url

# list scopemaps
def get_list_scopemap_url():
    url = f'{resource}/{scope}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/{acrScopeMapResourceApi}?api-version=2021-08-01-preview'
    return url

# generate credentials (and passwords)
def get_generate_credentials_url():
    url = f'{resource}/{scope}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/registries/{registry}/generateCredentials?api-version={createtokenapiversion}'
    return url

# create token
# using  TokenUpdateParameters
# https://github.com/Azure/azure-sdk-for-python/blob/eb12059c40d04c96da60455a807d347be15ccfa8/sdk/containerregistry/azure-mgmt-containerregistry/azure/mgmt/containerregistry/v2020_11_01_preview/models/_models.py
# https://github.com/Azure/azure-cli/blob/7148fd2d7f76853a8cfd3232c8ee3c27fcc6d207/src/azure-cli/azure/cli/command_modules/acr/tests/latest/recordings/test_acr_connectedregistry.yaml#L1255
createtokenapiversion='2020-11-01-preview'
def get_create_token_url(tokenName):
    url = f'{resource}/{scope}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/{acrTokenResourceApi}/{tokenName}?api-version={createtokenapiversion}'
    return url

def generate_token_json():
    token_attributes = {
        'properties':{
            'scopeMapId':'/subscriptions/7fdcde88-0aa7-4342-ac7c-fceebb18912e/resourceGroups/akstests/providers/Microsoft.ContainerRegistry/registries/edwinakstests/scopeMaps/_repositories_push',
            'status':'disabled'
        } 
    }
    return token_attributes

# generate credentials
# NOTE: a password is either called "password1" or "password2", which are used as enums in the token system
# using this API spec
# https://github.com/Azure/azure-rest-api-specs/blob/main/specification/containerregistry/resource-manager/Microsoft.ContainerRegistry/preview/2021-08-01-preview/examples/TokenUpdate.json
# exmaple here:
# https://github.com/Azure/azure-rest-api-specs/blob/main/specification/containerregistry/resource-manager/Microsoft.ContainerRegistry/preview/2021-08-01-preview/examples/RegistryGenerateCredentials.json
def generate_credentials_json(tokenId):
    generatecredentials_parameters = {
        'tokenId':tokenId,
        'name':'password1',
        }     
    return generatecredentials_parameters

# examples:

# list tokens
# r1 = requests.get(get_list_token_url(), headers=headers, params=params)
# decode_list_tokens_response(r1)
# print(json.dumps(r1.json(), indent=4, separators=(',', ': ')))

# list scope maps
# r2 = requests.get(get_list_scopemap_url(), headers=headers, params=params)
# decode_list_scopemaps_response(r2)
http.client.HTTPConnection.debuglevel = 1
r3 = requests.put(get_create_token_url("myPyTest2"), headers=headers, json=generate_token_json()) # json=generate_create_token_json())
print(json.dumps(r3.json(), indent=4, separators=(',', ': ')))

# an example to generate a token password
r4 = requests.get(get_list_token_url(), headers=headers, params=params)
# we shall just choose the first token in the list of tokens returned as an example
tokenIDToUpdate=decode_token_ids(r4)[0]
print('Updating this token password:')
print(tokenIDToUpdate)

# http.client.HTTPConnection.debuglevel = 1
r5 = requests.post(get_generate_credentials_url(), headers=headers, json=generate_credentials_json(tokenIDToUpdate)) # json=generate_create_token_json())
print(json.dumps(r5.json(), indent=4, separators=(',', ': ')))