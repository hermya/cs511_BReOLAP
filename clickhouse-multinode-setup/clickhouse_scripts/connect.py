from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
conn_str = 'clickhouse://default:@localhost/default'
engine = create_engine(conn_str)
session = sessionmaker(bind=engine)()

from sqlalchemy import DDL, DML
database = 'test'
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM table"))

