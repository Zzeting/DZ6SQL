import db
import json
import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def insert_data_test(session):
    with open('tests_data.json') as data_test:
        data = json.load(data_test)
        for table in data:
            if table['model'] == 'publisher':
                insert = db.Publisher(
                    id=table['pk'],
                    name=table['fields']['name']
                )
                session.add(insert)
                session.commit()
            if table['model'] == 'book':
                insert = db.Book(
                    id=table['pk'],
                    title=table['fields']['title'],
                    id_publisher=table['fields']['id_publisher']
                )
                session.add(insert)
                session.commit()
            if table['model'] == 'shop':
                insert = db.Shop(
                    id=table['pk'],
                    name=table['fields']['name']
                )
                session.add(insert)
                session.commit()
            if table['model'] == 'stock':
                insert = db.Stock(
                    id=table['pk'],
                    id_book=table['fields']['id_book'],
                    id_shop=table['fields']['id_shop'],
                    count=table['fields']['count']
                )
                session.add(insert)
                session.commit()
            if table['model'] == 'sale':
                insert = db.Sale(
                    id=table['pk'],
                    price=table['fields']['price'],
                    date_sale=table['fields']['date_sale'],
                    id_stock=table['fields']['id_stock'],
                    count=table['fields']['count']
                )
                session.add(insert)
                session.commit()


def get_publisher(ssesion):
    publisher = int(input('Введите id -> '))
    data = ssesion.query(db.Book, db.Shop, db.Sale)
    data = data.join(db.Publisher, db.Publisher.id == db.Book.id_publisher)
    data = data.join(db.Stock, db.Stock.id_book == db.Book.id)
    data = data.join(db.Shop, db.Shop.id == db.Stock.id_shop)
    data = data.join(db.Sale, db.Sale.id_stock == db.Stock.id)
    records = data.filter(db.Publisher.id == publisher).all()
    for book, shop, sale in records:
        print(f'{book.title} | {shop.name} | {sale.price} | {sale.date_sale}')


database = 'postgres'
user = 'postgres'
password = '1234567890'
host = 'localhost'
port = '5434'

conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)

with conn.cursor() as cur:
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS "library";
        SET search_path TO "library";
        """)
    conn.commit()
conn.close()

DSN = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(DSN)

db.create_table(engine)
session = sessionmaker(bind=engine)
s = session()
insert_data_test(s)
get_publisher(s)

