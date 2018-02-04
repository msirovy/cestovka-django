from django.http import HttpResponse
import json
from pprint import pprint
import imaplib
import email
import socket
from django.conf import settings


def index(request):
    """ Index page
    """
    jsondata = json.dumps({'k1':'val1'})
    #pprint(request)
    return HttpResponse(jsondata, 
                        content_type="application/json")
                

def generate_docx(request):
    pass

def get_emails(request):
    """ Load and parse emails
    """
    try:
        mail = imaplib.IMAP4_SSL(getattr(settings, 'IMAP_HOST', None))
        mail.login(
            getattr(settings, 'IMAP_LOGIN', None), 
            getattr(settings, 'IMAP_PWD', None)
        )
        mail.select('inbox')
        state, data = mail.search(None, '(FROM "itinerary@amadeus.com")')

        id_list = data[0].split()

        for msg_id in range(int(id_list[-1]), int(id_list[0]), -1):
            print(msg_id)
            typ, data = mail.fetch(str(msg_id).encode(), '(RFC822)' )

            for _msg in data:
                if isinstance(_msg, tuple):
                    msg = email.message_from_string(str(_msg[1]))
                    pprint(msg['headers'])
                    email_subject = msg['subject']


    except socket.gaierror:
        state = "unable to connect mail server"
        print(state)


    finally:
        return HttpResponse(json.dumps({'return': state}),
                        content_type='application/json')
