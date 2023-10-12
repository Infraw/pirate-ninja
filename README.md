# Pirate Ninja ![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) [![License](https://img.shields.io/badge/license-GPLv3-green)](LICENSE)
Pirate Ninja is a Python-based command-line tool that allows you to search for torrents on PirateBay and books on LibGen.  
It provides find and access torrent files from your terminal.  

* Search for torrents on PirateBay.
    * Retrieve torrent details such as name, size, seeders, and leechers.
    * Get torrent magnet links.
* Search for books on LibGen.
    * Retrive book details such as title, author, year, size, extension.
    * Get Gnutella and DC++ magnet links.

# Installation
Before using Pirate Ninja, ensure you have Python 3.x and the required dependencies installed:

    pip install -r requirements.txt


# Usage
Pirate Ninja provides a command-line interface with the following options:

    -p or --piratebay: Search for torrents on PirateBay.
    -l or --libgen: Search for books on LibGen

# Example Usage
Search for a torrent on PirateBay:

    python3 pirate_ninja_cli.py -p "your_query_here"

Search for a book on LibGen:

    python3 pirate_ninja_cli.py -l "your_query_here"

# Contributing
We welcome contributions to Pirate Ninja! If you'd like to add new features, improve existing code, or fix issues, please feel free to open a pull request.

# License
This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

# Disclaimer
Pirate Ninja is intended for educational and research purposes only. Downloading copyrighted material may be illegal in your jurisdiction. Please use this tool responsibly and respect copyright laws.
