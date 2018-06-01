import requests
from bs4 import BeautifulSoup
import csv
#from model import EIS_data

#create csv file to save data
#pass in csv to writer method
#create column names in csv
csv_file = open('epa_scrape2.csv', 'write')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['EIS ID', 'Title', 'Title Link', 'Document', 'EPA Comment Letter Date', 'Federal Register Date', 'Agency', 'State', 'Document Link','Comment Due Date', 'Contact Name', 'Contact Number'])

#get request EIS data from EPA and bind to page variable
page = requests.get("https://cdxnodengn.epa.gov/cdx-enepa-II/public/action/eis/search;jsessionid=C7ED30E19AAC674E7E6239A24502C7CF?d-446779-p=2&search=&commonSearch=openComment#results")
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
    contact_number = item[13].get_text().strip().lstrip('Contact Phone')

    #append these values to epa_scrape.csv
    return [eis_id, comment_due_date, contact_name, contact_number]

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
    eis_id, comment_due_date, contact_name, contact_number = information(full_link)
    csv_writer.writerow([eis_id, title, full_link, document, epa_comment_date, fed_reg_date, agency, state, 'https://cdxnodengn.epa.gov' + download_docs_link, comment_due_date, contact_name, contact_number])

csv_file.close()
