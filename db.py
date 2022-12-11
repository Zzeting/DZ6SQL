from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, ForeignKey, Integer, String, DateTime, Numeric

Base = declarative_base(metadata=MetaData(schema='library'))


class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    id_publisher = Column(Integer, ForeignKey("publisher.id"), nullable=False)
    publisher = relationship("Publisher", backref="book")


class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey("book.id"), nullable=False)
    id_shop = Column(Integer, ForeignKey("shop.id"), nullable=False)
    count = Column(Integer)
    book = relationship("Book", backref="book")
    shop = relationship("Shop", backref="shop")


class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True)
    price = Column(Numeric)
    date_sale = Column(DateTime)
    id_stock = Column(Integer, ForeignKey("stock.id"), nullable=False)
    count = Column(Numeric)
    stock = relationship("Stock", backref="sale")


def create_table(engine):
    Base.metadata.create_all(engine)


def delete_data(session, table):
    data = session.query(table).all()
    session.delete(data)
    session.commit()