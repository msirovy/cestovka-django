#!/usr/bin/env python3

from html.parser import HTMLParser
from pprint import pprint
from sys import argv


class AmadeusParser(HTMLParser):
    SEARCH_PATTERN = [
        "Booking ref:",
        "Issued date:",
        "Traveler",
        "Departure",
        "Arrival",
        "Class",
        "Baggage allowance",
        "Booking status"
        ]
    tr_start = False
    load_data = None
    RET = dict()
    
    
    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.tr_start = True

        
    def handle_endtag(self, tag):
        if tag == "tr":
            try:
                pprint(self.RET[self.load_data])
            except:
                pass
                
            self.tr_start = False
            self.load_data = None

        
    def handle_data(self, data):
        if len(data) > 1:
            if data in self.SEARCH_PATTERN:
                self.load_data = data
                self.RET[data] = []
                
            if self.load_data is not None:
                self.RET[self.load_data].append(data)

def download_unread_emails():
    pass

if __name__ == "__main__":
    page = []
    with open(argv[1]) as F:
        page = "".join(F.readlines())

    parser = AmadeusParser()
    parser.feed(page)
