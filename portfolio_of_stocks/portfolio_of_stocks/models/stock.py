from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey
)

from .meta import Base


class Stock(Base):
    __tablename__ = 'stock_entries'
    id = Column(Integer, primary_key=True)
    account_id = Column(Text, ForeignKey('accounts.username'), nullable=False)
    symbol = Column(String, nullable=False, unique=True)
    companyName = Column(String)
    exchange = Column(String)
    industry = Column(String)
    website = Column(String)
    description = Column(String)
    CEO = Column(String)
    issueType = Column(String)
    sector = Column(String)
    date = Column(DateTime)

Index('stock_index', Stock.id, unique=True, mysql_length=255)
