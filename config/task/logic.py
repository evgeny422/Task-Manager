import requests


def add_XML(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        return e
        # return f'Exception {e}', 'Status_code: <400>'
    return requests.get(url).text, f'Status code: {requests.get(url).status_code}'
