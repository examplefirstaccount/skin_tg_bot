import requests

from bot.data import config

IMAGE_API_ENDPOINT = "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/images"
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

headers = {'user-agent': UA}
cookies = dict()


def get_ext_prices(ext_ids: list) -> dict:
    """
    Get trading prices for skins

    :param ext_ids: skins' api ids
    :return: most relevant price for each skin
    """

    ext_ids = [ext_id for ext_id in ext_ids if ext_id]
    json_data = {
        'operationName': 'price_trader_log',
        'variables': {
            'name_ids': ext_ids,
        },
        'query': '''query price_trader_log($name_ids: [Int!]!) {
                        price_trader_log(input: {name_ids: $name_ids}) {
                            name_id
                            values {
                                price_trader_new
                                time
                            }
                        }
                    }''',
    }

    response = requests.post('https://wiki.cs.money/api/graphql', cookies=cookies, headers=headers, json=json_data)
    if response.status_code == 200:
        data = response.json()['data']['price_trader_log']
        result = {price_obj['name_id']: price_obj['values'][-1]['price_trader_new'] for price_obj in data}
        return result
    else:
        print(f'Status code {response.status_code}')
        raise requests.exceptions.RequestException


def get_ext_images(skin_name: str) -> dict:
    """
    Get all available patterns of skin

    :param skin_name: skin name
    :return: one skin pattern for each existing exterior of a skin
    """

    json_data = {
        'operationName': 'pattern_list',
        'variables': {
            'name': skin_name,
            'exterior': '',
            'sortBy': 'float_value',
            'rareOnly': False,
            'contains_paint_seed': None,
        },
        'query': '''query pattern_list($contains_paint_seed: Int, $exterior: String, 
                                       $name: String!, $rareOnly: Boolean, $sortBy: String) {
                        pattern_list(input: {contains_paint_seed: $contains_paint_seed, exterior: $exterior, 
                                             name: $name, rare_only: $rareOnly, sort_by: $sortBy}) {
                            available
                            exterior
                            float_value
                            paint_seed
                            rare_name
                            uuid
                        }
                    }''',
    }

    response = requests.post('https://wiki.cs.money/api/graphql', cookies=cookies, headers=headers, json=json_data)
    if response.status_code == 200:
        data = response.json()['data']['pattern_list']
        result = dict()
        for img_obj in data:
            if img_obj['exterior'] not in result:
                img_id = img_obj['uuid']
                result[img_obj['exterior']] = f'{IMAGE_API_ENDPOINT}/wiki_{img_id}_preview.png'
            else:
                continue
        return result
    else:
        print(f'Status code {response.status_code}')
        raise requests.exceptions.RequestException


def get_ex_rate(key: str):
    """
    Get the exchange rate against the USD

    :param key: currency code  (ex. CNY)
    :return: up-to-date exchange rate
    """

    url = f'https://www.amdoren.com/api/currency.php?api_key={config.CURRENCY_API_KEY}&from=USD&to={key}'
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()
        if res['error'] == 0:
            return round(res['amount'])

    else:
        print(f'Status code {response.status_code}')
        raise requests.exceptions.RequestException
