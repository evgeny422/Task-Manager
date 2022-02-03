import requests


def add_XML(url):
    indicator = 'ValCurs'
    try:
        response = requests.get(url)
        value = response.text
    except requests.exceptions.RequestException as e:
        return e

    if indicator in value:
        return value
    else:
        raise Exception

