'''
This script will generate a spotify playlist from a 1001tracklists.com tracklist
'''

import spotipyExt
from lxml import html
import requests

USERNAME = '1232863129'
PL_URL = 'https://www.1001tracklists.com/tracklist/28uj5vr1/luttrell-crssd-fest-united-states-2019-03-03.html'

page = requests.get(PL_URL)
tree = html.fromstring(page.content)

