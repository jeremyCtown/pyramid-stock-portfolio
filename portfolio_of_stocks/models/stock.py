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
from sqlalchemy.orm import relationship
from .association import association_table


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    companyName = Column(String)
    exchange = Column(String)
    industry = Column(String)
    website = Column(String)
    description = Column(String)
    ceo = Column(String)
    issueType = Column(String)
    sector = Column(String)
    account_id = relationship("Account", secondary=association_table, back_populates="stock_id")

# Index('stock_index', Stock.id, unique=True, mysql_length=255)
