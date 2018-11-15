from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from xml.sax import saxutils as su


# informational tools views
def index(request):

    r = BeautifulSoup(su.unescape(requests.get('https://magic.wizards.com/en/rss/rss.xml').text))
    for i in r:
        print(i, "\n")
    context = {

    }
    return render(request, 'information/base.html')

def mtgrss(request):
    return render(request, 'information/mtgrss.html')

def youtube(request):
    return render(request, 'information/youtube.html')
