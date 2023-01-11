import json

from selenium import webdriver


def build_main_url(city, rooms, price):
    return f"https://www.yad2.co.il/realestate/rent?city={city}&rooms={rooms}&price={price}"


def build_item_url(item_id):
    return f"https://www.yad2.co.il/item/{item_id}"


def get_driver():
    options = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    # options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    return driver


def get_queries_from_json(file_name='queries.json'):
    with open(file_name, 'r', encoding='utf-8') as f:
        queries = json.load(f)
        return queries
