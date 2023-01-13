import json, os, re

from bs4 import BeautifulSoup
from translate import Translator

iw2ru = Translator(to_lang='ru', from_lang='iw')
iw2en = Translator(to_lang='en', from_lang='iw')


class MainScraper:
    def __init__(self, page_source, file_name='item_ids.json'):
        self.file_name = file_name
        self.soup = BeautifulSoup(page_source, 'html.parser')

        if os.path.isfile(file_name):
            self.old_item_ids = self._get_item_ids_from_json()
        else:
            self.old_item_ids = []

        self.fetched_item_ids = self._get_item_ids_from_page_source()
        self.new_item_ids = self._get_new_item_ids()
        self._save_item_ids_to_json()

    def _get_item_ids_from_page_source(self):
        items = self.soup.find_all('div', {"class": "feed_item"})
        return [item['item-id'] for item in items]

    def _save_item_ids_to_json(self):
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump({'item_ids': self.old_item_ids + self.new_item_ids}, f)

    def _get_item_ids_from_json(self):
        with open(self.file_name, 'r', encoding='utf-8') as f:
            item_ids = json.load(f)
            return item_ids.get('item_ids')

    def _get_new_item_ids(self):
        new_item_ids = [item_id for item_id in self.fetched_item_ids if item_id not in self.old_item_ids]
        return new_item_ids


class ItemScraper:
    def __init__(self, page_source, city, item_url):
        self.soup = BeautifulSoup(page_source, 'html.parser')
        self.city = city

        self.url = item_url
        self.image_urls = self._get_image_urls()
        self.address = f'{iw2en.translate(self.soup.find("h4", {"class": "main_title"}).text)}, {self.city}'
        self.contact_person = iw2en.translate(self.soup.find("span", {"class": "name"}).text)
        self.price = self.soup.find("strong", {"class": "price"}).text
        self.phone_number = self.soup.find(string=re.compile(r"\d\d\d-\d\d\d\d\d\d\d")).text.strip()

        self.sq_meters = self.soup.find("dl", {"class": "cell SquareMeter-item"}).text.split(' ')[0]
        self.room_count = self.soup.find("dl", {"class": "cell rooms-item"}).text.split(' ')[0]
        self.floor = iw2en.translate(self.soup.find("dl", {"class": "cell floor-item"}).text.split(' ')[0])
        self.description = iw2ru.translate(self.soup.find("div", {"class": "show_more content"}).text)

    def _get_image_urls(self):
        divs = self.soup.find_all("div", {"data-swiper-slide-index": re.compile(r"\d")})
        return sorted(set([div.find('img')['src'] for div in divs]))
