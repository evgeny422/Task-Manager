import requests


def add_XML(url):
    try:
        response = requests.get(url)
        value = response.text

    except requests.exceptions.RequestException as e:
        raise e

    if 'application/xml' in response.headers['Content-Type']:
        return value
    else:
        raise requests.exceptions.FileModeWarning
