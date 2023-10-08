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
        request.RequestException: If an error occurs during HTTP request.
    '''
    try:
        # Send HTTP GET request to url and parse it
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print("An error occured while fetching data from {}".format(url), e)

def get_proxy(proxy_list):
    '''
    Get proxies from proxy list.
    
    Args:
        proxy_list (str): The file name of proxy list.
        
    Returns:
        list: List of proxies (can contains duplicates) if successful.
        
    Raises:
        FileNotFoundError: If the proxy list file is not found.
        IOError: If an error occurs while trying open the file.
    '''
    proxies = []
    try:
        # Open file and iterate over lines
        with open(proxy_list, 'r') as f:
            for line in f:
                proxies.append(line.strip())
        return proxies
    except FileNotFoundError as e:
        raise e
    except IOError as e:
        raise e
    
def ping_url(url):
    '''
    Send HTTP GET request to URL and check if it returns successfully.
    
    Args:
        url (str): The URL to ping.
        
    Returns:
        bool: True if the URL reachable and returns successfull response.
        False otherwise.
    '''
    try:
        response = requests.get(url)
        # Check if the status code is in the range 2xx (indicating success)
        if 200 <= response.status_code < 300:
            return True
        else:
            return False
    except requests.RequestException as e:
        print("An error occured while sending the request (e.g., network issues):", e)
        return False
    
def get_choice(length):
    '''
    Get the user's choice for torrent number within a valid range.
    
    Args:
        length (int): The max valid number the user can choose
    
    Returns:
        int: The user's chosen torrent number
    '''
    while True:
        try:
            num = int(input('Enter torrent number: '))
            if 1 <= num <= length:
                break
            else:
                print('Error: Input is not within the valid range.')
        except ValueError:
            print('Invalid input. Input must be integer.')
    return num