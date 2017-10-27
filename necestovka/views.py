from django.http import HttpResponse
import json
from pprint import pprint

def index(request):
    """ Index page
    """
    jsondata = json.dumps({'k1':'val1'})
    pprint(request)
    return HttpResponse(jsondata, 
                        content_type="application/json")
                
