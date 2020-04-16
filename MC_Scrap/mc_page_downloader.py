import os
import time
from threading import Thread
from bs4 import BeautifulSoup
from selenium import webdriver
from utilities_py import directory_create, file_create, remove_special_characters, url_sanitizer
from utilities_py import current_date_time, CURRENT_PATH, DOWNLOAD_DIR, ROOT_DIR


# money control website template
# web_page = 'https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/oilnaturalgascorporation/ONG'
# SYMBOL_LIST = ['ONGC']

SYMBOL_WEBPAGE_MAPPING = {'ONGC': 'https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/oilnaturalgascorporation/ONG'}


class PageDownloader:
    def __init__(self, site_url):
        """
        Constructor to assign the instance variable i.e download page URL(page that needs to be downloaded)
        :param site_url: URL for website to be scraped
        """
        self.download_page_url = site_url

    def create_driver(self, driverType='chrome'):
        """
        method to create driver object
        :param driverType: type of driver object ot be created based on browser type
        :return: driver object
        """
        if driverType == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            # chrome_options.binary_location = DOWNLOAD_DIR
            driver = webdriver.Chrome(options=chrome_options,
                                      executable_path=ROOT_DIR + '\\chromedriver\\chromedriver.exe')
        return driver

    def close_driver(self, driver=None):
        """
        method to terminate/close the driver object properly
        :param driver: driver object to be flushed/closed
        :return: None
        """
        if driver:
            driver.close()
            driver.quit()

    def get_raw_html(self, current_dir, wait_time=12, SYMBOL=None):
        """
        method to fetch/download the page
        :param current_dir:
        :param wait_time:
        :param SYMBOL:
        :return:
        """
        if SYMBOL:
            driver = self.create_driver()

            driver.get(url=self.download_page_url)
            time.sleep(wait_time)
            file_create_name = SYMBOL + "_" + current_date_time(time_zone='utc') + ".html"
            source_html = driver.page_source
            file_create(os.path.join(current_dir, file_create_name), source_html)

            self.close_driver(driver)
            return source_html, []


def main(current_dir, web_page, symbol):
    downloader_obj = PageDownloader(site_url=web_page)
    website_html, list_restaurants = downloader_obj.get_raw_html(current_dir=current_dir, wait_time=10, SYMBOL=symbol)


if __name__ == '__main__':
    for i in SYMBOL_WEBPAGE_MAPPING:
        directory_create(os.path.join(DOWNLOAD_DIR, i))
        main(os.path.join(DOWNLOAD_DIR, i), SYMBOL_WEBPAGE_MAPPING[i], i)
