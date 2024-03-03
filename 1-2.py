import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def fetch_detail_page_URLs(driver, base_url, max_count=50):
    detail_page_URLs = []
    page = 1
    while len(detail_page_URLs) < max_count:
        driver.get(f'{base_url}&p={page}')
        time.sleep(3)
        links = driver.find_elements(By.CSS_SELECTOR, 'a.style_titleLink__oiHVJ')
        if not links:
            break
        for link in links:
            if len(detail_page_URLs) < max_count:
                detail_page_URLs.append(link.get_attribute('href'))
            else:
                break
        page += 1
    return detail_page_URLs

def fetch_store_data(driver, url):
    driver.get(url)
    time.sleep(3)

    try:
        store_name = driver.find_element(By.ID, 'info-name').text.strip()
    except:
        store_name = ''
    try:
        phone_number = driver.find_element(By.CSS_SELECTOR, 'span.number').text.strip()
    except:
        phone_number = ''
    try:
        address = driver.find_element(By.CSS_SELECTOR, 'span.region').text.strip()
    except:
        address = ''
    try:
        building_name = driver.find_element(By.CSS_SELECTOR, 'span.locality').text.strip()
    except:
        building_name = ''
    try:
        urls_element_sv = driver.find_element(By.CSS_SELECTOR,'a.sv-of.double')
        urls_sv = urls_element_sv.get_attribute('href')
    except NoSuchElementException:
        urls_sv = ''
    try:
        urls_element_go_off = driver.find_element(By.CSS_SELECTOR,'a.url.go-off')
        urls_go_off = urls_element_go_off.get_attribute('href')
    except NoSuchElementException:
        urls_go_off =''

    urls =''
    ssl = 'FALSE'

    if urls_sv.startswith('https'):
        urls = urls_sv
        ssl = 'TRUE'
    elif urls_go_off.startswith('https'):
            urls = urls_go_off
            ssl = 'TRUE'
    elif urls_sv.startswith('http'):
        urls = driver.current_url
        ssl = 'FALSE'
    elif urls_go_off.startswith('http'):
        urls = driver.current_url
        ssl = 'FALSE'
    else:
        urls = urls_sv if urls_sv else urls_go_off
        ssl = 'FALSE'
    if urls.startswith('https'):
        ssl = 'TRUE'

    match = re.match(r"(.+?[都道府県])(.+?[市区町村])(.+)", address)
    if match:
        prefecture = match.group(1)
        city = match.group(2)
        street_address = match.group(3)
    else:
        prefecture = ''
        city = ''
        street_address = ''

    return [store_name, phone_number, '', prefecture, city, street_address, building_name, urls, ssl]

options = Options()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
driver = webdriver.Chrome(options=options)

base_url = 'https://r.gnavi.co.jp/area/tokyo/rs/?fw='
detail_page_URLs = fetch_detail_page_URLs(driver, base_url)

data = []
for url in detail_page_URLs:
    store_data = fetch_store_data(driver,url)
    data.append(store_data)


df = pd.DataFrame(data, columns=["店舗名","電話番号","メールアドレス","都道府県","市区町村","番地","建物名","URL","SSL"])
df.to_csv('1-2.csv', index=False, encoding='utf=8=sig')

driver.quit()