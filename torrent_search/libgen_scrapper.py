import utils
import requests
import bs4

def get_libgen_search(query, proxies):
    '''
    Perform a search on Library Genesis and retrieve search results with a working proxy.
    
    Args:
        query (str): The search query.
        proxies (list of str): A list of URLs to attempt the search.
    
    Returns:
        tuple: A tuple contains two elements:
            - BeatifulSoup object: The search results parsed using BeautifulSoup.
            - str: The used working proxy URL. 
    '''
    # Format query for url
    query = query.replace(' ', '%20')
    for proxy in proxies:
        if utils.ping_url(proxy):
            true_proxy = proxy
            full_url = proxy + 'search.php?req={}'.format(query)
            break
    else:
        raise Exception('Error: No reachable proxy found.')
    soup = utils.get_soup(full_url)
    # Extract content
    if soup is None:
        raise Exception('Error: Soup cannot be None type.')
    table = soup.find('table', attrs={'class':'c'})
    if table is None:
        raise Exception('Search results not found on page.')
    return table , true_proxy

def extract_libgen_data(table, url):
    '''
    Extracts data from search table on Library Genesis (LibGen) search page.
    
    Args:
        table (bs4.element.Tag): A BeautifulSoup Tag object representing the table of search info.
        url (str): The base URL for complete book links.
        
    Returns:
        tuple: A tuple containing two elements:
            - data (list of dict): A list of dictionaries where each one represents book data.
                Each dictionary contains the following keys:
                - 'ID' (str): The book's unique identifier.
                - 'Authors' (str): The author(s) of the book.
                - 'Title' (str): The title of the book.
                - 'Publisher' (str): The book's publisher.
                - 'Year' (str): The publication year of the book.
                - 'Pages' (str): The number of pages in book.
                - 'Language' (str): The language of the book.
                - 'Size' (str): The size of the book file.
                - 'Extension' (str): The file extension (e.g., PDF, EPUB).
                - 'Link' (str): The full URL to book's details page.
            - href_links (list of str): A list of URLs to the details pages of extracted books.
    '''
    # Initialize an empty list to store data
    data = []
    href_links = []

    for row in table.find_all('tr')[1:]:
        # Initialize an empty dictionary for each row
        row_data = {}

        # Extract data from each cell in the row
        cells = row.find_all('td')
        if len(cells) >= 11:
            row_data['ID'] = cells[0].text.strip()
            row_data['Authors'] = cells[1].text.strip()
            row_data['Title'] = cells[2].text.strip()
            row_data['Publisher'] = cells[3].text.strip()
            row_data['Year'] = cells[4].text.strip()
            row_data['Pages'] = cells[5].text.strip()
            row_data['Language'] = cells[6].text.strip()
            row_data['Size'] = cells[7].text.strip()
            row_data['Extension'] = cells[8].text.strip()
            row_data['Link'] = url + cells[2].find('a', id=row_data['ID']).get('href')
            href_links.append(row_data['Link'])

            # Append  row data to the list
            data.append(row_data)
    return data, href_links

def show_libgen_data(data):
    '''
    Display data retrieved from Library Genesis.
    
    Args:
        data (list of dict): List of dictionaries, where each one represents data packet.
    
    '''
    for idx, packet in enumerate(data, start=1):
        print('Number:', idx)
        # Example packet = {'ID': '123', 'Title': 'Lorem Ipsum' ...}
        for key, val in packet.items():
            print(key,':', val)
        print('\n')

def libgen_magnet(url):
    '''
    Extract magnet links from chosen Library Genesis search result.
    
    Args:
        url (str): The URL of LibGen page to extract magnet.
    
    Returns:
        list of str: A list of magnet links found on page.
    '''
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    a_tag = soup.find_all('a')
    magnet_hashes = []
    if a_tag:
        for item in a_tag:
            href_link = item.get('href')
            # Check if the href starts with 'magnet' (assume magnet link) 
            if href_link[:6] == 'magnet':
                magnet_hashes.append(href_link)
 
    return magnet_hashes