import utils
import requests


def get_libgen_search(query, proxies):
    # Format query for url
    query = query.replace(' ', '%20')
    for proxy in proxies:
        if utils.ping_url(proxy):
            url = proxy + 'search.php?req={}'.format(query)
            break
    else:
        raise Exception('Error: No reachable proxy found.')
    soup = utils.get_soup(url)
    # Extract content
    if soup is None:
        raise Exception('Error: Soup cannot be None type.')
    table = soup.find('table', attrs={'class':'c'})
    if table is None:
        raise Exception('Search results not found on page.')
    return table

    

    