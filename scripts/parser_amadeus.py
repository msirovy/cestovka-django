#!/usr/bin/env python3

from html.parser import HTMLParser
from pprint import pprint
from necestovka.models import Airports, Airlines, Flights, Tickets, Extras, Orders, Passengers

class AmadeusParser(HTMLParser):
    SEARCH_PATTERN = [
        "Booking ref",
        "Issued date",
        "Traveler",
        "Departure",
        "Arrival",
        "Class",
        "Baggage allowance",
        "Booking status"
        ]
    tr_start = False
    key = None
    RET = {
        "Traveler" : None,
        "Issued date" : None,
        "Booking ref": None, 
        "fly" : {
            1: dict()
        } 
    }
    fly_id = 1
    fly_dict = None

    
    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.tr_start = True
        
    def handle_endtag(self, tag):
        if tag == "tr":
            self.tr_start = False
            self.key = None

        
    def handle_data(self, data):
        if len(data) > 1:
            if data.replace(":", "") in self.SEARCH_PATTERN:
                # nasel jsem klic
                self.key=data.replace(":", "")
                #print("KEY::: ", key)

                if self.key not in self.RET.keys():

                    if self.key in self.RET["fly"][self.fly_id].keys():
                        # klic v tomto letu jiz je, takze zalozime novy let
                        # pprint(self.RET["fly"][self.fly_id])
                        self.fly_id += 1
                        self.RET["fly"][self.fly_id] = {self.key: []}


                    else:
                        # pokud jeste neni, pripravime ho
                        self.RET["fly"][self.fly_id][self.key] = []
                #else:
                #    jde o klic spolecny pro vsechny lety
                    
                
            elif self.key is not None:
                # pokud uz vim jaky jsem nasel klic mohu pridavat data
                try:
                    if self.key in self.RET.keys():
                        # pridavam data do korene slovniku
                        if self.RET[self.key] is None:
                            self.RET[self.key] = data

                    else:
                        # pridavam data do letu
                        self.RET["fly"][self.fly_id][self.key].append(data)

                except KeyError as err:
                    print("---------------------------")
                    print(err.__doc__)
                    print("EXCEPT::  klic: {}   data: {}".format(self.key, data))
                    pprint(self.RET)
                    print("---------------------------")
                    exit()



def run():
    from json import load

    with open("./cache/testovaci", "r") as F:
        msg = load(F)
        eml = AmadeusParser()
        eml.feed(msg["body"])
        

        print("###########################\n\n")
        pprint(eml.RET)


if __name__ == "__main__":
    run()
