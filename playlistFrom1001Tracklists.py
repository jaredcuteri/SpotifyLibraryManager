'''
This script will generate a spotify playlist from a 1001tracklists.com tracklist
'''
# HTML Track Format
#<span class="trackFormat">
#    <span class="blueTxt">
#        "ARTIST NAME"
#        <span title="open artist page" class="tgHidspL">...</span>
#        </span>
#    <span class> - </span>
#    <span class="blueTxt">
#        "TRACK NAME"
#        <span title="oepn track page" class="tgHidspL">...</span>
#    </span>
#</span>

import spotipyExt
from lxml import html
import requests

USERNAME = '1232863129'
PL_URL = 'https://www.1001tracklists.com/tracklist/28uj5vr1/luttrell-crssd-fest-united-states-2019-03-03.html'

# Header is needed to make Website believe this request is coming from a browser
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like

class RequestError(Exception):
    pass
    
response = requests.get(PL_URL, headers=headers)
if response.status_code >= 300:
    raise RequestError("Failed to access webpage. Response Code: {0}".format(response.status_code))

tree = html.fromstring(response.content)
setlist_title = tree.xpath('//body/meta[@itemprop="name"]/@content')

result = tree.xpath('//span[@class="trackFormat"]/span[@class="blueTxt"]/text()')
artists_tracks = [pair for pair in zip(*[iter(result)]*2)]
print(artists_tracks)