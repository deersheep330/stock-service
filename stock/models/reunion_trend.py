from sqlalchemy import Column, String, Date, Integer, ForeignKey, text
from sqlalchemy.orm import relationship

from ..db import Base

class ReunionTrend(Base):

    __tablename__ = 'reunion_trend'

    symbol = Column(String(16), ForeignKey('stock_symbol.symbol'), nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True, server_default=text('(CURRENT_DATE)'))
    popularity = Column(Integer, nullable=False)
    stock = relationship('StockSymbol')

    def __repr__(self):
        return str([getattr(self, c.name, None) for c in self.__table__.c])
