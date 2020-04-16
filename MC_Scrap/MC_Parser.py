import os
from bs4 import BeautifulSoup
from utilities_py import directory_create, file_create

CURRENT_PATH = os.getcwd()
DOWNLOAD_DIR = os.path.join(CURRENT_PATH, 'WebsiteDownload')
ROOT_DIR = CURRENT_PATH.replace('\\Zagat', '')


class MCParser:

    def get_date_file(self, filename=None):
        """
        get the date of the stock information from file name
        :param filename: name of the stock file
        :return: stocks info date
        """
        if filename:
            stock_with_date = filename.split("\\")[-1].split(".")[0]
            date = ':'.join(stock_with_date.split("_")[1:])
            return date
        return ""

    def stock_details(self, website_soup = None, filename = None):
        """
        Getting the stocks details like market cap, market lot, close, high, low price, etc
        For eg: {'Market Cap (Rs Cr.)': '97,245.56', 'Market Lot': '1', 'Price/Book': '0.49', 'Open Price': '76.55', 'Average Price': '77.00', 'Open Interest': '53,820,700'}
        :param website_soup: soup element consisting of current details about stock
        :return: stock_details in hashmap form/dictionary
        """
        if website_soup:
            try:
                ul_elements = website_soup.findAll('div', attrs={'id': "fnoquotetable"})
                share_details = {}

                for ul in ul_elements:
                    for li in ul.findAll('li', attrs={'class': 'clearfix'}):
                        header = None
                        value = None
                        for element_header in li.findAll('div', attrs={'class': 'value_txtfl'}):
                            header = element_header.text
                        for element_value in li.findAll('div', attrs={'class': 'value_txtfr'}):
                            value = element_value.text
                        share_details[header] = value
                date = self.get_date_file(filename)
                share_details['date'] = date
                return share_details
            except Exception as e:
                print("Exception")
                return "Exception: " + str(e)
        return "Exception: No website to scrap"


def getDataForRest(PARSE_DIR=None):
    file = r'C:\Users\yagarwal\PycharmProjects\Yash\Scraping\MC_Scrap\WebsiteDownload\ONGC\ONGC_2020_04_15 16_17_11.html'
    with open(file, 'r', encoding='utf-8') as f_read:
        website_html = f_read.read()
        data = ""
        website_soup = BeautifulSoup(website_html, 'lxml')
        obj_parser = MCParser()
        stock_quotes = str(obj_parser.stock_details(website_soup, file))
        if 'exception' not in stock_quotes.lower():
            file_create("./hello.txt", stock_quotes)


# directory_create(DOWNLOAD_DIR)
if __name__ == '__main__':

    files = []
    getDataForRest()
