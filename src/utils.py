from selenium import webdriver


def build_url(city, rooms, price):
    return f"https://www.yad2.co.il/realestate/rent?{city}&{rooms}&{price}"


def get_driver():
    options = webdriver.ChromeOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    return driver