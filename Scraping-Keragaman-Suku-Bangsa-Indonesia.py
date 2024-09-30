import requests
page = requests.get('https://www.juraganles.com/2016/08/keragaman-suku-bangsa-dan-budaya-di-indonesia-34-Provinsi.html')
page
print(page.text)
from bs4 import BeautifulSoup
import requests
page = requests.get('https://www.juraganles.com/2016/08/keragaman-suku-bangsa-dan-budaya-di-indonesia-34-Provinsi.html')
bs = BeautifulSoup(page.text, 'html.parser')
bs
bs.title
bs.title.name
bs.title.string
bs.span
bs.span.string
bs.find("head")
bs.find("div")
bs.find_all('div', {'class':'league-table'})

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.juraganles.com/2016/08/keragaman-suku-bangsa-dan-budaya-di-indonesia-34-Provinsi.html"
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')
province_headers = soup.find_all('h4')

data = []
info_keys = ['Luas Wilayah', 'Dasar Hukum', 'Tanda Plat Nomor Kendaraan']

def clean_text(text):
    return text.replace(':', '').strip()

for header in province_headers:
    province_data = {}
    
    province_name = clean_text(header.text)
    province_data['Provinsi'] = province_name

    next_siblings = header.find_next_siblings()

    for sibling in next_siblings:
        if sibling.name == 'b':
            info_title = clean_text(sibling.text)

            if sibling.next_sibling:
                if sibling.next_sibling.name:
                    info_value = sibling.next_sibling.get_text(strip=True)
                else:
                    info_value = sibling.next_sibling.strip()

                if info_value:
                    province_data[info_title] = clean_text(info_value)
        
        if sibling.name == 'h4':
            break

    for key in info_keys:
        if key not in province_data:
            province_data[key] = 'data tidak ditemukan'
    
    data.append(province_data)

df = pd.DataFrame(data)
df = df[['Provinsi', 'Luas Wilayah', 'Dasar Hukum', 'Tanda Plat Nomor Kendaraan']]
df = df.replace('', 'data tidak ditemukan')
print(df.to_string(index=False))
df.to_csv('provinsi_data.csv', index=False)