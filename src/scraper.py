import json, re, time
from bs4 import BeautifulSoup

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from utils import get_driver, build_main_url, build_item_url

driver = get_driver()


def get_item_ids_from_page_source(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    items = soup.find_all('div', {"class": "feed_item"})
    return [item['item-id'] for item in items]


def save_item_ids_to_json(item_ids, file_name='item_ids.json'):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump({'item_ids': item_ids}, f)


def get_item_ids_from_json(file_name='item_ids.json'):
    with open(file_name, 'r', encoding='utf-8') as f:
        item_ids = json.load(f)
        return item_ids.get('item_ids')


def get_new_item_ids_from_page_source(page_source):
    candidate_item_ids = get_item_ids_from_page_source(page_source)
    original_item_ids = get_item_ids_from_json()
    new_item_ids = [item_id for item_id in candidate_item_ids if item_id not in original_item_ids]
    save_item_ids_to_json(original_item_ids + new_item_ids)
    return new_item_ids


def get_item_image_urls(soup):
    image_divs = soup.find_all("div", {"data-swiper-slide-index": re.compile("\d")})
    image_urls = sorted(set([image_div.find('img')['src'] for image_div in image_divs]))
    return image_urls


def get_item_data(page_source):
    item_data = {}
    soup = BeautifulSoup(page_source, 'html.parser')
    item_data['image_urls'] = get_item_image_urls(soup)
    return item_data


def main():
    city = 'topArea=19&area=17&city=7400'
    rooms = 'rooms=3-3.5'
    price = 'price=3000-4500'
    url = build_item_url('2dr00e9d')
    # driver.get(url)
    # driver.find_element(By.ID, 'lightbox_contact_seller_0').click()
    # time.sleep(2)
    with open('item.html', 'r', encoding='utf-8') as f:
        item_data = get_item_data(f)
        for image_url in item_data.get('image_urls'):
            print(image_url)


if __name__ == "__main__":
    main()
