import requests


def add_XML(url):
    try:
        response = requests.get(url)
        value = response.text
    except requests.exceptions.RequestException as e:
        return e

    if 'text/xml' in response.headers['Content-Type']:
        return value
    else:
        raise