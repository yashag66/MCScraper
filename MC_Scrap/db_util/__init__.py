from sqlalchemy import Column
from sqlalchemy import create_engine, ForeignKey, event
from sqlalchemy import Integer, Float
from sqlalchemy import String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()
engine = None


# https://stackoverflow.com/questions/12753450/sqlalchemy-mixins-and-event-listener
# https://stackoverflow.com/questions/17819584/insert-mysql-timestamp-column-value-with-sqlalchemy
class BaseMixin(object):
    id = Column(Integer, primary_key=True)
    created_at = Column("created_at", DateTime, nullable=False)
    updated_at = Column("updated_at", DateTime, nullable=False)

    def __str__(self):
        return {"created_at": str(self.created_at), "updated_at": str(self.updated_at)}

    @staticmethod
    def create_time(mapper, connection, instance):
        now = datetime.utcnow()
        instance.created_at = now
        instance.updated_at = now

    @staticmethod
    def update_time(mapper, connection, instance):
        now = datetime.utcnow()
        instance.updated_at = now

    @classmethod
    def register(cls):
        event.listen(cls, "before_insert", cls.create_time)
        event.listen(cls, "before_update", cls.update_time)


class Stock(BaseMixin, Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True)
    stock_name = Column(String(255), unique=True, nullable=False)
    symbol = Column(String(255), unique=True, nullable=False)
    company_name = Column(String(255), unique=True, nullable=False)
    mc_link = Column(String(255), unique=True, nullable=False)
    description = Column(String(1000))
    sector = Column(String(255))
    updated_by = Column(String, nullable=False)

    # stockdetails = relationship("Stock_Details", back_populates="stock")

    def set_details(self, details={}):
        """

        :param details:
        :return:
        """
        self.stock_name = details["stock_name"]
        self.symbol = details["symbol"]
        self.company_name = details["company_name"]
        self.mc_link = details["mc_link"]
        self.description = details["description"]
        self.sector = details["sector"]
        self.updated_by = details["updated_by"]

    def __iter__(self):
        temp = super().__str__()
        temp["stock_name"] = self.stock_name
        temp["symbol"] = self.symbol
        temp["company_name"] = self.company_name
        temp["mc_link"] = self.mc_link
        temp["description"] = self.description
        temp['sector'] = self.sector
        temp["updated_by"] = self.updated_by
        for key, value in temp.items():
            yield (key, value)


class Stock_Details(BaseMixin, Base):
    __tablename__ = "stock_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stock.id"))
    open_price = Column(Float, nullable=False)
    prev_close_price = Column(Float, nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)
    no_of_contracts_traded = Column(Integer, nullable=False)
    turnover_in_lakhs = Column(Float, nullable=False)
    market_lot = Column(Integer)
    open_interest = Column(Float)
    open_interest_change = Column(Float)
    open_interest_change_percent = Column(Float)
    date = Column(DateTime, nullable=False)

    stock = relationship("Stock", back_populates="stock_details")

    def set_details(self, details={}):
        """

        :param details:
        :return:
        """
        self.stock_id = details['stock_id']
        self.open_price = details['open_price']
        self.prev_close_price = details['prev_close_price']
        self.open_price = details['open_price']
        self.high_price = details['high_price']
        self.low_price = details['low_price']
        self.average_price = details['average_price']
        self.no_of_contracts_traded = details['no_of_contracts_traded']
        self.turnover_in_lakhs = details['turnover_in_lakhs']
        self.market_lot = details['market_lot']
        self.open_interest = details['open_interest']
        self.open_interest_change = details['open_interest_change']
        self.open_interest_change_percent = details['open_interest_change_percent']
        self.date = details['date']

    def __iter__(self):
        temp = super().__str__()
        temp['stock_id'] = self.stock_id
        temp['open_price'] = self.open_price
        temp['prev_close_price'] = self.prev_close_price
        temp['open_price'] = self.open_price
        temp['high_price'] = self.high_price
        temp['low_price'] = self.low_price
        temp['average_price'] = self.average_price
        temp['no_of_contracts_traded'] = self.no_of_contracts_traded
        temp['turnover_in_lakhs'] = self.turnover_in_lakhs
        temp['market_lot'] = self.market_lot
        temp['open_interest'] = self.open_interest
        temp['open_interest_change'] = self.open_interest_change
        temp['open_interest_change_percent'] = self.open_interest_change_percent
        temp['date'] = self.date
        for key, value in temp.items():
            yield (key, value)


Stock.stock_details = relationship("Stock_Details", order_by=Stock_Details.id, back_populates="stock")

# Creating engine
# endpoint = "database-1.cdds2awb8gec.ap-south-1.rds.amazonaws.com"
# username = "postgres"
# password = "password"
# connection_string = "postgres://"+username+":"+password+"@"+endpoint+"/stocks"
# engine = create_engine(connection_string, echo = True)
engine = create_engine("sqlite:///stocks.db", echo=True)

# Creating all tables
Base.metadata.create_all(engine)

Stock.register()
Stock_Details.register()

Session = sessionmaker(bind=engine)


def get_all_stocks(class_ref=None):
    """

    :return:
    """
    if class_ref:
        session = Session()
        list_stocks = []
        try:
            stock_mappings = session.query(class_ref).all()
            for stock_info in stock_mappings:
                list_stocks.append(dict(stock_info))
            return list_stocks
        except Exception as e:
            print("Exception")
            print(e)


def set_stock_details(class_ref = None, data = {}, symbol = None):
    pass
#     if class_ref:
#         if class_ref == Stock_Details:
#             # Query stock id from stock table
#             session = Session()
#             try:
#                 stock_mappings = session.query(Stock).filter(Stock.symbol == symbol).first()
#                 print(stock_mappings)
#             except Exception as e:
#                 print("Exception")
#                 print(e)
