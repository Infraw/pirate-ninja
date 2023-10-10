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

def extract_libgen_data(table):
    
    # Initialize an empty list to store the data
    data = []

    # Loop through the rows of the table
    for row in table.find_all('tr'):
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

            # Append  row data to the list
            data.append(row_data)
    return data