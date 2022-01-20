import requests


def add_XML(url):
    return requests.get(url).text
