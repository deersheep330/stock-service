from sqlalchemy import Column, String

from ..db import Base

class Stock(Base):

    __tablename__ = 'stock'

    symbol = Column(String(16), nullable=False, primary_key=True)
    name = Column(String(64), nullable=False)

    def __repr__(self):
        return str([getattr(self, c.name, None) for c in self.__table__.c])
