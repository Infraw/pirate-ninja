import argparse
import webbrowser
from torrent_search.utils import get_proxy, get_choice
from torrent_search.pirate_bay_scrapper import get_magnet, get_search_table, print_search_table

def main():
    parser = argparse.ArgumentParser(prog='Pirate Ninja',
                                     description='A command-line torrent search tool')
    parser.add_argument('-p', '--piratebay', metavar='query', type=str, help='Search on Pirate Bay.')
    args = parser.parse_args()
    
    if args.piratebay:
        print('Searching on PirateBay...')
        # Get proxies as list
        proxies = get_proxy('data/piratebay_proxies.txt')
        # Itarate over proxies and get table about results (if find reachable proxy)
        search_table = get_search_table(args.piratebay, proxies)
        #Print results and return torrent urls
        url_list = print_search_table(search_table)
        torrent_count = len(url_list)
        # Get input from user in range of torrent count. 
        choice = get_choice(torrent_count) - 1 # Extract 1 because results are enumerated from 1
        # Get magnet from sublink
        magnet = get_magnet(url_list[choice])
        if magnet is str:
            webbrowser.open(magnet)

if __name__ == '__main__':
    main()