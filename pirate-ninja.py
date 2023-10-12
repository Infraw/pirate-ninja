import argparse
import webbrowser
from torrent_search.utils import get_proxy, get_choice
from torrent_search.pirate_bay_scrapper import piratebay_magnet, get_pirate_search, print_pirate_search
from torrent_search.libgen_scrapper import get_libgen_search, extract_libgen_data, show_libgen_data, libgen_magnet

def main():
    parser = argparse.ArgumentParser(prog='Pirate Ninja',
                                     description='A command-line torrent search tool')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--piratebay', metavar='query', type=str, action='store',help='Search on Pirate Bay.')
    group.add_argument('-l', '--libgen', metavar='query', type=str, action='store', help='Search on Library Genesis.')
    args = parser.parse_args()
    
    if args.piratebay:
        print('Searching on PirateBay...')
        # Get proxies as list
        proxies = get_proxy('data/piratebay_proxies.txt')
        # Itarate over proxies and get table about results (if find reachable proxy)
        search_table = get_pirate_search(args.piratebay, proxies)
        #Print results and return torrent urls
        url_list = print_pirate_search(search_table)
        torrent_count = len(url_list)
        # Get input from user in range of torrent count. 
        choice = get_choice(torrent_count) - 1 # Extract 1 because results are enumerated from 1
        # Get magnet hash from sublink
        magnet_hash = piratebay_magnet(url_list[choice])
        if isinstance(magnet_hash, str):
            webbrowser.open(magnet_hash)
    elif args.libgen:
        print('Searching on Library Genesis (LibGen)...')
        # Get proxies as list
        proxies = get_proxy('data/libgen_proxies.txt')
        # Itarate over proxies return working one and get table about results (if find reachable proxy)
        search_table, url = get_libgen_search(args.libgen, proxies)
        # Extract data from search table
        data, href_links = extract_libgen_data(search_table, url)
        # Print results on screen
        show_libgen_data(data)
        # Get input from user in range of book count
        book_count = len(href_links)
        choice = get_choice(book_count) - 1
        # Get magnet hashes from sublink
        magnet_hashes = libgen_magnet(href_links[choice])
        if isinstance(magnet_hashes[0], str):
            print('Gnutella:', magnet_hashes[0])
            print('DC++:', magnet_hashes[1])
                
if __name__ == '__main__':
    main()