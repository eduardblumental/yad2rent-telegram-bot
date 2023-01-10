import json, os, re
from bs4 import BeautifulSoup


class MainScraper:
    def __init__(self, page_source, file_name):
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
    def __init__(self, page_source):
        self.soup = BeautifulSoup(page_source, 'html.parser')

        self.image_urls = self._get_image_urls()
        self.address = self.soup.find("h4", {"class": "main_title"}).text
        self.contact_person = self.soup.find("span", {"class": "name"}).text
        self.price = self.soup.find("strong", {"class": "price"}).text
        self.phone_number = self.soup.find("div", {"id": "lightbox_phone_number_0"}).text

        # self.sq_meters =
        # self.room_count =
        # self.floor =
        # self.description =

    def _get_image_urls(self):
        divs = self.soup.find_all("div", {"data-swiper-slide-index": re.compile("\d")})
        return sorted(set([div.find('img')['src'] for div in divs]))
