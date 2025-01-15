import requests
from bs4 import BeautifulSoup

def get_london_postcodes(num):
    url = "https://www.ukpostcode.co.uk/random-london-postcode.htm"

    form_data = {
        'tb_numberofpostcodes': str(num),
        'cb_plain': 'on'
    }

    response = requests.post(url, data=form_data)

    soup = BeautifulSoup(response.content, "html.parser")
    postcodes_html = soup.find('p', {'id': 'pData'})

    postcodes = [a_tag.text.strip() for a_tag in postcodes_html.find_all('a')]

    return postcodes