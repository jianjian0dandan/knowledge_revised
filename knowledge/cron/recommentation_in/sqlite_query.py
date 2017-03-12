# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine=create_engine('sqlite:///../../flask-admin.db')

from sqlalchemy import Table,Column,Integer,String,DateTime,MetaData, Boolean, ForeignKey

Base=declarative_base()

class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    #confirmed_at = Column(DateTime())

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
result = session.query(User).all()
#for r in result:
#    print r.email

def get_user_name():
    admin_list = []
    for r in result:
        admin_list.append(r.email)
    return admin_list

