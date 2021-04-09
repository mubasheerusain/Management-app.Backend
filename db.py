from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Table, Column, String, MetaData,Integer,ForeignKey,JSON,TIMESTAMP
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base  

db =  create_engine('postgresql+pg8000://root:root@localhost/demo')  
base = declarative_base()

class Users(base):  
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String,nullable = False)
    username = Column(String, nullable = False)
    password = Column(String, nullable = False)
    access = Column(String, nullable = False)

class Product(base):  
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    product_line = Column(String,nullable = False)
    product_name = Column(String, nullable = False)
    part_no = Column(String, nullable = False)
    label = Column(String, nullable = False)
    csd = Column(String, nullable = False)


Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)
