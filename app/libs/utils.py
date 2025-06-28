from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def use_disable_chrome_annoyings():
    options = Options()
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    return options

def get_page_content(driver, url):
    driver.get(url)
    print('Getting page content of title: ', driver.title)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def write_file(output, file_name):
    with open(f'static/{file_name}', 'w', encoding='utf-8') as f:
        f.write(output)
        return True

def use_selenium():
    options = use_disable_chrome_annoyings()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

def render_link(link, title):
    return f'<a href="{link}" target="_blank">{title}</a>'

def render_images(image_list):
    return ''.join([f'<img src="{img}" width="100" />' for img in image_list])
