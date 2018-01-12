from django.http import HttpResponse
import json

def index(request):
    """ Index page
    """
    jsondata = json.dumps({'k1':'val1'})
    return HttpResponse(jsondata, 
                        content_type="application/json")

