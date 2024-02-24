import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def fetch_detail_page_URLs(base_url, max_count=50):
	detail_page_URLs = []
	page = 1
	while len(detail_page_URLs) < max_count:
		res = requests.get(f'{base_url}&p={page}', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.57'})
		res.encoding = 'utf-8'
		soup = BeautifulSoup(res.text, 'html.parser')
		links = soup.find_all('a',{'class':'style_titleLink__oiHVJ'})
		if not links:
			break
		for link in links:
			if len(detail_page_URLs) < max_count:
				detail_page_URLs.append(link['href'])
			else:
				break
		page += 1
	return detail_page_URLs


def fetch_store_data(url):
	time.sleep(3)
	res2 = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.57'})
	res2.encoding = 'utf-8'
	soup2 = BeautifulSoup(res2.text,'html.parser')

	store_name = soup2.find('p',{'id':'info-name', 'class':'fn org summary'}).text.strip()	if soup2.find('p',{'id':'info-name', 'class':'fn org summary'})	else ''
	phone_number = soup2.find('span',{'class': 'number'}).text.strip() if soup2.find('span', {'class': 'number'}) else ''
	address_elm= soup2.find('span',{'class':'region'})
	address = address_elm.text.strip() if address_elm else ''
	building_name = soup2.find('span',{'class':'locality'}).text.strip() if soup2.find('span',{'class':'locality'}) else''

	match = re.match(r"(.+?[都道府県])(.+?[市区町村])(.+)", address)

	if match:
		prefecture = match.group(1)
		city = match.group(2)
		street_address =match.group(3)
	else:
		prefecture =''
		city = ''
		street_address = ''
	return [store_name, phone_number, '', prefecture, city, street_address, building_name,'','']

base_url = "https://r.gnavi.co.jp/area/tokyo/rs/?fw="
detail_page_URLs =fetch_detail_page_URLs(base_url)


data = []
for url in detail_page_URLs:
    store_data = fetch_store_data(url)
    data.append(store_data)

df = pd.DataFrame(data, columns=["店舗名","電話番号","メールアドレス","都道府県","市区町村","番地","建物名","URL","SSL"])
df.to_csv('1-1.csv', index=False, encoding='utf=8=sig')