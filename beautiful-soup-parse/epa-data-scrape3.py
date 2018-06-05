import requests
from bs4 import BeautifulSoup
import csv
#from model import EIS_data

#create csv file to save data
#pass in csv to writer method
#create column names in csv
csv_file = open('epa_scrape3.csv', 'write')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['EIS ID', 'Title', 'Title Link', 'Document', 'EPA Comment Letter Date', 'Federal Register Date', 'Agency', 'State', 'Document Link','Comment Due Date', 'Contact Name', 'Contact Number'])

#get request EIS data from EPA and bind to page variable
page = requests.get("https://cdxnodengn.epa.gov/cdx-enepa-II/public/action/eis/search?d-446779-p=3&search=&commonSearch=openComment#results", cookies={
    'JSESSIONID':'AF244936B7A181D0A56AD0559A21F90F',
    'ARRAffinity': '4b66915ecab4bec141bb219950c0d40d0a9097886d8801c4efd2e6971c5bd650',
    '_gid': 'GA1.2.173804977.1528139290',
    '_gat_EPA':'1',
    '_gat_GSA':'1',
    '_ga': 'GA1.2.1949185182.1528139290', 
    '_ceg.s': 'p9tmb0',
    '_ceg.u': 'p9tmb0',
    'has_js': '1',
    '_4c_':'llVJra9swFP0rQ4N9SmLrEVsOjNF1rPRDx9jra5Cl60TMkTxZblpK%2FnuvbId2dIMtENv33KNzdB8P5LgHRzZ0zWT6l4IxviA%2F4b4nmweiu%2FS8TY8htGRD9jF2%2FSbLtLlz3oDbuRV0arXztwlagsNoeX2ddUPdWp0pHa13Gdg%2B60EFvX83vd6%2B0f5w8O7rFPkO3CUC4OLrAP3Qxp4siEYDtKTVar1iGP%2BwvY0%2BXH9AEMMeRvHt8XhkiHz6HZoR1%2F4aINzP0fvgj66x0Jp%2B2wW%2FC%2BrwhwzCLn4cnLFu97f01WANtNYBtmlkTJV8g3BICAK2%2Fxz8hCLgfMQQ4RtrLmKLClZvv8AObzsL1GjRQ8Doch%2F8AV4VBaINDoAI2iijqGJC1nVeg5YgqBBVwUWem4YizyfXG6XxM0ADIYxKqSU2pibOQ5oBHO%2BELScsPl27w2ETgR%2Bt16odjzqMri6238fG00pUVK6pZKtxZ3jFqhwJJtVhoFE4PHJakLtppxjmy7zgFE0iLpAs8Mr4Q0awZl4uAtoYYSrGlRG65pKqvCxzA8ClBKkB9Uc9vq6SaCU5RYEO9cbzKD7bIaVI6XK2wy6d7VJhI1s8XY6tJc1lWby83DSN%2FzuD1c%2F0%2FJ%2Fo2LGp%2FHPbnlcpKOWFQJo9s9SLfMVSG3HVpy6cEzxPds%2BpCTmdTo8%3D',
    })
#creates an instance of the BeautifulSoup class to parse
soup = BeautifulSoup(page.content, 'html.parser')

#find all information for table
table = soup.find('table', class_='responsive-table')

rows = table.find('tbody').findAll('tr')

# #list of links to iterate for second parse
# link_list = []

def information(full_link):

    #iterate through list of project links from first parse
    # for url in link_list:

    page = requests.get(full_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    item = soup.findAll(class_='form-item')

    #capture eis id, comment due date, and contact information from project specific page
    eis_id = item[1].get_text().strip().lstrip('EIS Number')
    comment_due_date = item[4].get_text().strip().lstrip('EIS Comment Due/ Review Period Date').strip().rstrip('00:00:00.0')
    #multi_states = item[10].get_text().strip().split(' - ')
    contact_name = item[12].get_text().strip().replace('Contact Name','').lstrip()
    contact_phone = item[13].get_text().strip().lstrip('Contact Phone')

    #append these values to epa_scrape.csv
    return [eis_id, comment_due_date, contact_name, contact_phone]

#add values to csv file by unpacking values into appropriate columns
for row in rows:
    #list of links to iterate for second parse
    columns = row.findAll('td')

    #values to be placed into column 
    title = columns[0].get_text().strip()
    document = columns[1].get_text().strip()
    epa_comment_date = columns[2].get_text().strip()
    fed_reg_date = columns[3].get_text().strip()
    agency = columns[4].get_text().strip()
    state = columns[5].get_text().strip()

    download_docs_link = columns[6].find('a').get('href')

    #grab href associated with title; does not return full url
    title_link = columns[0].find('a').get('href')

    #complete link and make a list of those links to perform second get request
    full_link = 'https://cdxnodengn.epa.gov' + title_link
    eis_id, comment_due_date, contact_name, contact_phone = information(full_link)
    csv_writer.writerow([eis_id, title, full_link, document, epa_comment_date, fed_reg_date, agency, state, 'https://cdxnodengn.epa.gov' + download_docs_link, comment_due_date, contact_name, contact_phone])

csv_file.close()
