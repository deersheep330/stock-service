from sqlalchemy import Column, String, Date, Integer, func, ForeignKey
from sqlalchemy.orm import relationship

from ..db import Base

class TwseOverSold(Base):

    __tablename__ = 'twse_over_sold'

    symbol = Column(String(16), ForeignKey('stock.symbol'), nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True, server_default=func.sysdate())
    quantity = Column(Integer, nullable=False)
    stock = relationship('Stock')

    def __repr__(self):
        return str([getattr(self, c.name, None) for c in self.__table__.c])
