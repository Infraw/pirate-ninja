import utils
import requests
import bs4
import webbrowser


def get_libgen_search(query, proxies):
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
    
    # Initialize an empty list to store the data
    data = []
    href_links = []

    # Loop through the rows of the table
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

def show_data(data):
    for idx, packet in enumerate(data, start=1):
        print('Number:', idx)
        for key, val in packet.items():
            print(key,':', val)
        print('\n')

def libgen_magnet(url):
    
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    a_tag = soup.find_all('a')
    magnet_hashes = []
    if a_tag:
        for item in a_tag:
            href_link = item.get('href')
            if href_link[:6] == 'magnet':
                magnet_hashes.append(href_link)
 
    return magnet_hashes