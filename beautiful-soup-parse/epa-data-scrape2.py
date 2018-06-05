import requests
from bs4 import BeautifulSoup
import unicodecsv as csv
#from model import EIS_data

#create csv file to save data
#pass in csv to writer method
#create column names in csv
csv_file = open('epa_scrape2.csv', 'write')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['EIS ID', 'Title', 'Title Link', 'Document', 'EPA Comment Letter Date', 'Federal Register Date', 'Agency', 'State', 'Document Link','Comment Due Date', 'Contact Name', 'Contact Number'])

#get request EIS data from EPA and bind to page variable
page = requests.get("https://cdxnodengn.epa.gov/cdx-enepa-II/public/action/eis/search;jsessionid=C7ED30E19AAC674E7E6239A24502C7CF?d-446779-p=2&search=&commonSearch=openComment#results", cookies={
    'JSESSIONID':'C6EEA84573F33DDB08960DFD176D749C',
    'ARRAffinity': '4b66915ecab4bec141bb219950c0d40d0a9097886d8801c4efd2e6971c5bd650',
    '_gid': 'GA1.2.173804977.1528139290',
    '_gat_EPA':'1',
    '_gat_GSA':'1',
    '_ga': 'GA1.2.1949185182.1528139290', 
    '_ceg.s': 'p9tdae',
    '_ceg.u': 'p9tdae',
    'has_js': '1',
    '_4c_':'llVNdb9s6DP0rgwb0qYktWbGlAMXQ22FFHzoM%2B3oNZIlOhDmSJ8tNiyL%2FvZTtdB26AXd5MMzDYx7ykHkkhx04sqYrJiinVDKW83PyAx56sn4kukvPu%2FQYQkvWZBdj16%2BzTJt75w24rVtCp5Zbf5egBTiMFjc3WTfUrdWZ0tF6l4Htsx5U0Lt3ZsF5WVVy0V2wswm7ONN%2Bv%2FfuyxT5DtwVAuDi2wD90MaenBONaqhP5XK1ZBh%2Ft72NPty8RxDDHkalzeFwYIh8%2FB2aEdf%2BHCA8zNF%2FwR9cY6E1%2FaYLfhvU%2Fg8ZhF38MDhj3fZv6evBGmitA%2FRsZEyTfIWwTwgCtv8U%2FIQi4HzEEOFbay5jixWs3nyGLXY7F6hRooeA0dUu%2BD28KUtEG9wG4bRRRlHFuKjrvAYtgFPOZVnwPDcNRZ5PqrdK42uABkIYKyVLbEwmzhubAdz1hC0mLP5qu8PNE44vrdeqHT91GF1fbr6NxlPJJRUrKthyPKBCMpkjwaQ5DDQKl0eO5%2BR%2BOjDGqpXMWZGjSMRrEiW2jD9kBGvmSyOgjeFGskIZrutCUJVXVW4ACiFAaMD6Y71iJVNRKQqKBTqsN35Pn%2BWQUqZ0NcuhSye5NNjIxlt%2Fbm4laC6q8nVz0zb%2B7RucfqbjtP%2BDjo5N459sezkl%2FjGLkiPNnljqVV6yZCOe%2BuTCKVHkSe4lNSHH4%2FEJ',
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
