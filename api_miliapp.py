import requests
import json

def get_vendas_filtro(TOKEN_MILIAPP, PARAMS):
    url_params = ''
    for key, value in PARAMS.items():
        url_params += f'{key}={value}&'

    url = f'https://api.fmiligrama.com/vendas/busca?token={TOKEN_MILIAPP}&{url_params}'

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['data'][-1]

def obter_tokens_tiny(TOKEN_MILIAPP, origin):
    url = f'https://api.fmiligrama.com/tiny/token?token={TOKEN_MILIAPP}&sorting='

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    for token in response:
        if token['origin'] == origin:
            access_token = token['access_token']
            refresh_token = token['refresh_token']

    return access_token, refresh_token

def cadastrar_bip(TOKEN_MILIAPP, bip):
    url = f'https://api.fmiligrama.com/bip?token={TOKEN_MILIAPP}'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = json.dumps(bip)

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    response = response.json()

    return response
