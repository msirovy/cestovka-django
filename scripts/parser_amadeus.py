#!/usr/bin/env python3

from html.parser import HTMLParser



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
    key = None
    RET = {
        "Traveler" : [],
        "Issued date" : [],
        "Booking ref": [], 
        1 : dict() 
        }
    part = 1
    
    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.tr_start = True
        
    def handle_endtag(self, tag):
        if tag == "tr":
            self.tr_start = False
            self.load_data = None

        
    def handle_data(self, data):
        if len(data) > 1:
            if data in self.SEARCH_PATTERN:
                if data in self.RET[self.part]:
                    self.part += 1
                    self.RET[self.part] = dict()

                self.load_data = data
                self.RET[self.part][data] = []
   

            if self.load_data is not None:
                if data != self.load_data:
                    # pokud nachazim parametry pro prvni urovan slovniku,
                    #   neukladam je do letu, 
                    #   ale ulozim je do provniho levelu slovniku
                    #   rozepsat to tak, aby vystup nebyl s dvojteckama
                    if self.load_data.replace(":","") in self.RET.keys():
                        self.RET[self.load_data.replace(":","")].append(data)


                    else:
                        self.RET[self.part][self.load_data].append(data)



if __name__ == "__main__":
    from json import load
    from pprint import pprint

    with open("./cache/testovaci", "r") as F:
        msg = load(F)
        eml = AmadeusParser()
        eml.feed(msg["body"])
        

        print("###########################\n\n")
        pprint(eml.RET)

