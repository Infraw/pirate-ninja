import utils
import requests
import bs4

def get_search_table(query, proxy_list):
    '''
    Get search table data from Pirate Bay.
    
    Args:
        query (str) : A query for search in website.
        proxy_list (list) : Proxy list for find available proxy for script.
        
    Returns:
        table (bs4.element.Tag) : Bs4 Tag object representing search table on the webpage
    
    Raises:
        Exception: If no reachable proxy server found or if the search table not found on webpage.
    '''
    # Format spaces for url 
    query = query.replace(' ', '%20')
    # Find working proxy 
    for proxy in proxy_list:
        if utils.ping_url(proxy):
            url = proxy + 'search/{}/1/99/0'.format(query)
            break
    else:
        raise Exception("Error: No reachable proxy found.")
    soup = utils.get_soup(url)
    # Extract search table
    if soup is None:
        raise Exception("Error: Soup cannot be None type.")
    table = soup.find('table', id='searchResult')
    if table is None:
        raise Exception("Table not found on the webpage.")
    return table