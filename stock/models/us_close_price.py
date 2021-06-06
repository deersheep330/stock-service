from sqlalchemy import Column, String, Date, Float, ForeignKey, text
from sqlalchemy.orm import relationship

from ..db import Base

class UsClosePrice(Base):

    __tablename__ = 'us_close_price'

    symbol = Column(String(16), ForeignKey('stock_symbol.symbol'), nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True, server_default=text('(CURRENT_DATE)'))
    price = Column(Float, nullable=False)
    stock = relationship('StockSymbol')

    def __repr__(self):
        return str([getattr(self, c.name, None) for c in self.__table__.c])
