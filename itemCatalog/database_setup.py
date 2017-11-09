#!/usr/bin/env python
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):


    __tablename__ = 'category'

    name = Column(String(40), nullable = False)
    description = Column(String (120), nullable = True)
    id = Column(Integer, primary_key = True)
    items = relationship('Item', cascade = 'delete')


class Item(Base):


    __tablename__ = 'item'

    name = Column(String(40), nullable = False)
    description = Column(String(120), nullable = True)
    id = Column(Integer, primary_key = True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)
