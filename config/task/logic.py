import requests


def add_XML(url):
    indicator = 'ValCurs'
    try:
        requests.get(url)
        value = str(requests.get(url).text)
    except requests.exceptions.RequestException as e:
        return e

    if indicator in value:
        return value
