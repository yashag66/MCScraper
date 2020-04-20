import os
from bs4 import BeautifulSoup
from utilities_py import directory_create, file_create, list_files
from utilities_py import CURRENT_PATH, DOWNLOAD_DIR, ROOT_DIR
from db_util import Session, Stock, Stock_Details
from db_util import set_stock_details
from utilities_py import stocks_info_mapping

session = Session()


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


class db_ops:
    global session

    def insert_stock_details(self, stock_details={}):
        pass


def getDataForRest(file=None):
    # file = r'C:\Users\yagarwal\PycharmProjects\Yash\Scraping\MC_Scrap\WebsiteDownload\ONGC\ONGC_2020_04_15 16_17_11.html'
    with open(file, 'r', encoding='utf-8') as f_read:
        website_html = f_read.read()
        data = ""
        website_soup = BeautifulSoup(website_html, 'lxml')
        obj_parser = MCParser()
        stock_quotes = obj_parser.stock_details(website_soup, file)
        if 'exception' not in str(stock_quotes).lower():
            temp_symbol = str(file).split('\\')[-2]
            # print(stocks_info_mapping(stock_quotes, temp_symbol))
            set_stock_details(class_ref=Stock_Details, data=stock_quotes, symbol=temp_symbol)


# directory_create(DOWNLOAD_DIR)
if __name__ == '__main__':

    files = []
    files = list_files(DOWNLOAD_DIR)
    for f in files:
        getDataForRest(f)



# # create a Session
# session = Session()
#
# # work with sess
# myobject = Stock()
# myobject.stockname = 'ONGC'
# myobject.symbol = 'ONGC'
# myobject.company_name = 'ONGC'
# myobject.mc_link = 'ONGC.com'
# myobject.description = 'ONGC'
# myobject.updated_by = 'YASH'
# session.add(myobject)
#
# # myobject1 = Stock()
# # myobject1.stockname = 'ONGC'
# # myobject1.symbol = 'ONGC'
# # myobject1.company_name = 'ONGC'
# # myobject1.mc_link = 'ONGC.com'
# # myobject1.description = 'ONGC'
# # myobject1.updated_by = 'YASH'
# # session.add(myobject1)
#
# session.commit()