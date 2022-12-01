import psycopg2
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Column, ForeignKey, Integer, String, DateTime, Numeric
import json

conn = psycopg2.connect(database='postgres', user='postgres', password='1234567890', host='localhost', port='5434')

with conn.cursor() as cur:
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS "library";
        """)
    conn.commit()
conn.close()

DSN = 'postgresql+psycopg2://postgres:1234567890@localhost:5434/postgres'
engine = create_engine(DSN)

Base = declarative_base(metadata=MetaData(schema='library'))


class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    # book = relationship("book")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    id_publisher = Column(Integer, ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")


class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    # stock = relationship("stock")


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey("book.id"), nullable=False)
    id_shop = Column(Integer, ForeignKey("shop.id"), nullable=False)
    count = Column(Integer)
    book = relationship(Book, backref="book")
    shop = relationship(Shop, backref="shop")
    # sale = relationship("sale")


class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True)
    price = Column(Numeric)
    date_sale = Column(DateTime)
    id_stock = Column(Integer, ForeignKey("stock.id"), nullable=False)
    count = Column(Numeric)
    stock = relationship(Stock, backref="sale")


def create_table(engine):
    Base.metadata.create_all(engine)


def delete_data(session, table):
    data = session.query(table).all()
    session.delete(data)
    session.commit()


def insert_data_test(session):
    with open('tests_data.json') as data_test:
        data = json.load(data_test)
        for table in data:
            if table['model'] == 'publisher':
                insert = Publisher(
                    id=table['pk'],
                    name=table['fields']['name']
                )
                session.add(insert)
                session.commit()
            if table['model'] == 'book':
                insert = Book(
                    id=table['pk'],
                    title=table['fields']['title'],
                    id_publisher=table['fields']['id_publisher']
                )
                session.add(insert)
                session.commit()
            if table['model'] == 'shop':
                insert = Shop(
                    id=table['pk'],
                    name=table['fields']['name']
                )
                session.add(insert)
                session.commit()
            if table['model'] == 'stock':
                insert = Stock(
                    id=table['pk'],
                    id_book=table['fields']['id_book'],
                    id_shop=table['fields']['id_shop'],
                    count=table['fields']['count']
                )
                session.add(insert)
                session.commit()
            if table['model'] == 'sale':
                insert = Sale(
                    id=table['pk'],
                    price=table['fields']['price'],
                    date_sale=table['fields']['date_sale'],
                    id_stock=table['fields']['id_stock'],
                    count=table['fields']['count']
                )
                session.add(insert)
                session.commit()


create_table(engine)
session = sessionmaker(bind=engine)
s = session()
insert_data_test(s)
