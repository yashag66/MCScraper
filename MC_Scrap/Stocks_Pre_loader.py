"""
Code to write the information for the stocks in the db like symbol, company name, money control link, etc.
"""
import os
from utilities_py import CURRENT_PATH, DOWNLOAD_DIR, ROOT_DIR
from db_util import Session, Stock
import pandas as pd

pre_session = Session()


class DB_Pre_Ops:

    global pre_session

    def insert_stock(self, stock_mapping: list = []):
        """
        :param stock_mapping:
        :return:
        """
        for stock in stock_mapping:
            try:
                stock_object = Stock()
                stock_object.set_details(stock)
                pre_session.add(stock_object)
                pre_session.commit()
            except Exception as e:
                print("Exception Occured")
                print(e)
                print("Probably, the data for the given stock already exists in the fact table")


filepath = os.path.join(CURRENT_PATH, 'Stocks_Info', 'MC_det.csv')
stocks_df = pd.read_csv(filepath)

# Converting dataframe to list of dictionary
stocks_dict = stocks_df.to_dict('records')
object = DB_Pre_Ops()
object.insert_stock(stocks_dict)