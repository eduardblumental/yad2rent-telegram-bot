import json, time

from selenium import webdriver

from scrapers import MainScraper


def build_main_url(city, rooms, price):
    return f"https://www.yad2.co.il/realestate/rent?city={city}&rooms={rooms}&price={price}"


def build_item_url(item_id):
    return f"https://www.yad2.co.il/item/{item_id}"


def get_driver(headless=True):
    options = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    if headless:
        options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1080, 720)
    return driver


def get_queries_from_json(file_name='queries.json'):
    with open(file_name, 'r', encoding='utf-8') as f:
        queries = json.load(f)
        return queries


async def handle_captcha(chat_id, context, error):
    await context.bot.send_message(chat_id=chat_id, text=f'Не вышло обойти CAPTCHA, требуется вмешательство: {error}.')
    driver = get_driver(headless=False)
    driver.get('https://www.yad2.co.il/')
    print(input('Issue solved?\n'))


def get_new_item_ids_from_query(driver, query):
    city, city_code, rooms, price = query.values()
    driver.get(build_main_url(city_code, rooms, price))
    time.sleep(2)
    new_item_ids = MainScraper(page_source=driver.page_source).new_item_ids
    return new_item_ids
