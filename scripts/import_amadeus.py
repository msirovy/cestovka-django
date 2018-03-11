#!/usr/bin/env python3

from html.parser import HTMLParser
from pprint import pprint
from sys import argv
import imaplib
import email
from config import conf

def logger(msg):
    print(msg)


def download_unread_emails(mailserver, username, password, sender_of_interest=None):
    # Login to INBOX
    imap = imaplib.IMAP4_SSL(mailserver, 993)
    imap.login(username, password)
    imap.select('INBOX')
    
    # Use search(), not status()
    # Print all unread messages from a certain sender of interest
    if sender_of_interest:
        #status, response = imap.uid('search', None, 'UNSEEN', 'FROM {0}'.format(sender_of_interest))
        status, response = imap.uid('search', None, 'FROM {0}'.format(sender_of_interest))
    else:
        status, response = imap.uid('search', None, 'UNSEEN')
    
    if status == 'OK':
        unread_msg_nums = response[0].split()
    else:
        unread_msg_nums = []
    
    data_list = []
    for e_id in unread_msg_nums:
        data_dict = {}
        e_id = e_id.decode('utf-8')
        _, response = imap.uid('fetch', e_id, '(RFC822)')
        html = response[0][1].decode('utf-8')
        email_message = email.message_from_string(html)       
        data_dict['mail_to'] = email_message['To']
        data_dict['mail_subject'] = email_message['Subject']
        data_dict['mail_from'] = email.utils.parseaddr(email_message['From'])
        data_dict['body'] = email_message.get_payload()[0].as_string()
        data_list.append(data_dict)
    
    return data_list



def run():
    from necestovka.models import (
        Passengers,
        Flights, 
        Orders,
        Airports,
        Airlines
    )
    
    from json import load, dump

    for msg in download_unread_emails(mailserver=conf.imap_server, 
                username=conf.imap_login, password=conf.imap_password, 
                sender_of_interest="itinerary@amadeus.com"):
        with open("./cache/mail-{}".format(msg["mail_subject"]), "w+") as F:
            dump(msg, F)

    """
        eml = AmadeusParser()
        eml.feed(msg["body"])
        
        print("###########################\n\n")
        pprint(eml.RET)
    """

if __name__ == "__main__":
    run()          
            
