import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup
import data  # tax_types, periods, counties, municipalities,

report_url = 'https://www.revenue.state.il.us/app/kob/KOBReport'

# param: r
reports = {
    'CountyTotals': 'CountyTotals',
    'Specific': 'Specific'
}


## We want to grab all the td elements like the one below
##
## <TD CLASS='data' ALIGN='right' VALIGN='top' NOWRAP>
## <CENTER><B>ST</B></CENTER>
## 18,887,148.64<BR>
## 16,185,354.22<BR>
## 62,117,172.52<BR>
## 17,352,693.36<BR>
## 14,166,524.92<BR>
## 7,891,375.77<BR>
## 32,494,883.62<BR>
## 29,752,400.16<BR>
## 20,989,444.21<BR>
## 4,220,617.81<BR>
## 224,057,615.23<BR><BR></TD>

categories = [
    'General Merchandise',
    'Food',
    'Drinking and Eating Places',
    'Apparel',
    'Furniture & H.H. & Radio',
    'Lumber, Bldg, Hardware',
    'Automotive & Filling Stations',
    'Drugs & Misc. Retail',
    'Agriculture & All Others',
    'Manufacturers',
    'Totals'
]


def parse_td(td):
    b = td.find('b')
    header = b.text if b else None
    matches = re.findall(r'>([^<>]*)<br/', str(td))
    cells = [match.strip() for match in matches]
    numbers = [float(cell.replace(',', '')) if cell else None for cell in cells]
    return header, numbers


params = dict(r='Specific', p='20121', m='0160001')
response = requests.get(report_url, params=params).text
# print response

# table's keys are column headers and values are lists, all of the same length
# table = dict()

soup = BeautifulSoup(response, 'lxml')
# print soup.prettify()

taxes = {}

tables = soup.find_all('table', cellspacing='3')
# the first table is the form
for table in tables[1:]:
    header_tds = table.find('table', width='600').find_all('td')
    name = header_tds[0].text.strip()
    county = header_tds[1].text.strip()
    taxpayer_match = re.search('Number of Taxpayers:\s+([0-9,]+)', header_tds[2].text)
    # taxpayers = '0'
    # if taxpayer_match:
    taxpayers = taxpayer_match.group(1).replace(',', '').strip()
    # else:
        # print 'Could not find taxpayers'
        # print header_tds

    table_id = '%s - %s - %d' % (name, county, int(taxpayers))

    taxes[table_id] = dict()
    for td in table.find_all('td', class_='data', align='right', valign='top'):
        header, cells = parse_td(td)
        taxes[table_id][header] = cells

pprint(taxes)

print 'Done'
