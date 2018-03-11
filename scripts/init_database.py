#!/usr/bin/env python3

from necestovka.models import Airports, Airlines
import csv


def import_airports(airports_path):
    print("Create airports")
    try:
        with open(airports_path) as airports:
            for r in csv.reader(airports, delimiter=","):
                print(r[0])
                try:
                    ap = Airports(name=r[0], code=r[1])
                    ap.save()
                except:
                    print("Row is already exists in databaze: {} {}".format(r))

    except IOError:
        print("Source data file does not exists")


def import_airlines(airlines_path):
    print("Create airlines")
    try:
        with open(airlines_path) as airlines:   
            for l in airlines:
                try:
                    al = Airlines(name=str(l))
                    al.save()
                except:
                    pass

    except IOError:
        print("Source data file does not exists")


#if __name__ == '__main__':
def run():
    import_airports("./data/airports.csv")
    import_airlines("./data/airlines.csv")
