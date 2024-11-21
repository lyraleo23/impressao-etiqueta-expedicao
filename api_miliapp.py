import requests
import json

def atualizar_req_miliapp(numero_tiny, req_smart, req_smart_list):
    url = f'https://api.fmiligrama.com/vendas/smart-'

    payload = json.dumps({
        "numero_tiny": numero_tiny,
        "req_smart": req_smart,
        "req_smart_list": req_smart_list
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    return

def get_vendas_filtro(PARAMS):
    url_params = ''
    for key, value in PARAMS.items():
        url_params += f'{key}={value}&'

    url = f'https://api.fmiligrama.com/vendas/busca?{url_params}'

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['data'][-1]

def obter_item_miliapp(id):
    url = f'https://api.fmiligrama.com/produtos/busca?idTiny={id}'

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)

    return response.json()['data'][0]

def obter_tokens_tiny(origin):
    url = f'https://api.fmiligrama.com/tiny/token?sorting='

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
    
    # access_token = response[-1]['access_token']
    # refresh_token = response[-1]['refresh_token']

    return access_token, refresh_token
