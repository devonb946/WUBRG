from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from xml.sax import saxutils as su

# informational tools views
def index(request):

    soup = BeautifulSoup(su.unescape(requests.get('https://magic.wizards.com/en/rss/rss.xml').text), 'xml')
    print(soup.prettify())
    rss_items = []

    for soup_item in soup.find_all('item', limit=2):
        item = RssItem()
        item.title = soup_item.title.contents[0] if soup_item.title else None
        item.link = 'https://magic.wizards.com' + soup_item.link.contents[0] if soup_item.link else None

        description = ''.join([str(d) for d in soup_item.description.contents]) if soup_item.description else None

        # open up the inner HTML and edit the hyperlink for "Read more" before we parse it
        # since WotC likes to use relative links
        html_soup = BeautifulSoup(description, 'html.parser')
        anchor = html_soup.find('a', {'class': ['cta', 'learn-more']})
        if anchor:
            anchor['href'] = 'https://magic.wizards.com' + anchor['href']
            anchor['target'] = '_blank'

        # use our newly cooked soup for our custom made description
        item.description = ''.join([str(d) for d in html_soup.contents]) if html_soup else None

        item.pubDate = soup_item.pubDateString.contents[0] if soup_item.pubDateString else None
        item.creator = soup_item.find('dc:creator').contents[0] if soup_item.find('dc:creator') else None
        rss_items.append(item)

    context = {
        'rss_items': rss_items
    }
    return render(request, 'information/base.html', context)

def mtgrss(request):
    return render(request, 'information/mtgrss.html')

def youtube(request):
    return render(request, 'information/youtube.html')

class RssItem(object):
    pass
