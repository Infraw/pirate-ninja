import requests
from bs4 import BeautifulSoup

def get_soup(url):
    '''
    Retrive and parse HTML content from specified URL.
    Args:
        url (str): The URL to fetch and parse.
    Returns:
        BeautifulSoup object (if successfull) or an exception (if an error occurs).
    Raises:
        request.Exception: If an error occurs during HTTP request.
    '''
    try:
        # Send HTTP GET request to url and parse it
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        response.raise_for_status()
        return soup
    except requests.RequestException as e:
        print("An error occured while fetching data from {}".format(url), e)
        