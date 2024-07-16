from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def get_netloc_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def make_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response

    except requests.exceptions.RequestException as exception:
        raise exception


def get_status_code(url):
    return make_response(url).status_code


def get_attributes_content(url):
    response = make_response(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description = soup.find_all('meta')
    if description:
        for item in description:
            if item.get('name') == 'description':
                description = item
                break
        else:
            description = None
    attributes = (soup.find("h1"), soup.find("title"), description)

    result = {
        attribute.name: attribute.text
        if attribute.name != "meta"
        else attribute.get("content")
        for attribute in attributes
        if attribute
    }

    return result
