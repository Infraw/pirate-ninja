from . import utils
import requests
import bs4

def get_pirate_search(query, proxy_list):
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

def print_pirate_search(table):
    '''
    Print data from HTML table about search results.
    
    Args:
        table (BeatifulSoup): The bs4 object containing the table.
    
    Returns:
        list: A list of links found in the table
    
    Prints:
        - Number
        - Type
        - Name
        - Uploaded
        - Size
        - Seeders
        - Leechers
        - ULed by
        - Link
        - "Table not found" if the param is None.
    '''
    href_links = []
    if table:
        href = None
        # Find all table rows
        rows = table.find_all("tr") 
        # Skip the header row (index 0) and enumerate from 1
        for row_num, row in enumerate(rows[1:], start=1): 
            columns = row.find_all("td") 
            if len(columns) >= 7:
                type_column = columns[0].get_text(strip=True)
                name_column = columns[1].find("a")
                uploaded_column = columns[2].get_text(strip=True)
                size_column = columns[4].get_text(strip=True)
                seeders_column = columns[5].get_text(strip=True)
                leechers_column = columns[6].get_text(strip=True)
                uled_by_column = columns[7].get_text(strip=True)

                if name_column:
                    href = name_column.get("href")
                    href_links.append(href)

                print("Number:", row_num)
                print("Type:", type_column)
                print("Name:", name_column.get_text(strip=True) if name_column else "N/A")
                print("Uploaded:", uploaded_column)
                print("Size:", size_column)
                print("Seeders:", seeders_column)
                print("Leechers:", leechers_column)
                print("ULed by:", uled_by_column)
                print("Link:", href)
                print("\n")
    else:
        print("Table not found on the webpage.")
    return href_links

def piratebay_magnet(url):
    '''
    Get magnet link from target url in Pirate Bay.
    
    Args:
        url (str) : Target url for scarp magnet.
    
    Returns
        str or None : Magnet link if found, or None if no magnet link is found.  
    '''
    piratebay = requests.get(url)
    soup = bs4.BeautifulSoup(piratebay.text, 'html.parser')
    # Find magnet link using a CSS selector
    magnet_link = soup.select_one('a[href^="magnet:?xt=urn:btih:"]')
    if magnet_link:
        magnet = magnet_link['href']
    else:
        magnet = None
    return magnet