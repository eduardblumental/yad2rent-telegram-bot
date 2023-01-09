import json, time
from bs4 import BeautifulSoup

from utils import build_url, get_driver


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
    return new_item_ids


def main():
    city = 'topArea=19&area=17&city=7400'
    rooms = 'rooms=3-3.5'
    price = 'price=3000-4500'
    url = build_url(city, rooms, price)
    # driver.get(url)
    # time.sleep(2)
    with open('index.html', 'r', encoding='utf-8') as f:
        new_item_ids = get_new_item_ids_from_page_source(f)
        print(new_item_ids)


if __name__ == "__main__":
    main()
