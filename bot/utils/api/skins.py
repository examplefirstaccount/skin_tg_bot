import requests

from bot.data import config

IMAGE_API_ENDPOINT = 'https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/images'
CURRENCY_API_ENDPOINT = 'https://www.amdoren.com/api/currency.php'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

headers = {'user-agent': UA}
cookies = dict()


def get_ext_prices(ext_ids: list) -> dict:
    """
    Retrieves the most relevant trading prices for skins from the CS:GO market.

    This function sends a GraphQL request to retrieve the latest trader log prices
    for specified skin IDs, and returns the most recent price for each skin.

    Args:
        ext_ids (list): A list of skin API IDs to query prices for.

    Returns:
        dict: A dictionary mapping each skin ID to its most recent price.

    Raises:
        requests.exceptions.RequestException: If the request fails or returns a non-200 status code.
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
    Retrieves available patterns (images) for a specified skin.

    Sends a request to obtain all patterns of the specified skin, and
    returns one pattern image for each existing exterior (condition) of the skin.

    Args:
        skin_name (str): The name of the skin to retrieve patterns for.

    Returns:
        dict: A dictionary mapping each skin exterior to its corresponding pattern image URL.

    Raises:
        requests.exceptions.RequestException: If the request fails or returns a non-200 status code.
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
    Retrieves the current exchange rate of a specified currency against USD.

    Fetches the latest exchange rate for the given currency key using an external
    currency exchange API.

    Args:
        key (str): The currency code (e.g., 'CNY' for Chinese Yuan).

    Returns:
        float: The current exchange rate rounded to the nearest whole number.

    Raises:
        requests.exceptions.RequestException: If the request fails or returns a non-200 status code.
    """

    url = f'{CURRENCY_API_ENDPOINT}?api_key={config.CURRENCY_API_KEY}&from=USD&to={key}'
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()
        if res['error'] == 0:
            return round(res['amount'])

    else:
        print(f'Status code {response.status_code}')
        raise requests.exceptions.RequestException
