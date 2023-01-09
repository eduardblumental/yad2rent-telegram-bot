import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


def build_url(city, rooms, price):
    return f"https://www.yad2.co.il/realestate/rent?{city}&{rooms}&{price}"


def main():
    city = 'topArea=19&area=17&city=7400'
    rooms = 'rooms=3-3.5'
    price = 'price=3000-4500'
    url = build_url(city, rooms, price)
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all('div', {"class": "feed_item"})
    for item in items:
        print(type(item))


if __name__ == "__main__":
    main()
