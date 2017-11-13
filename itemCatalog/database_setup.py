#!/usr/bin/env python
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):

    __tablename__ = 'category'

    name = Column(String(40), nullable=False)
    description = Column(String(120), nullable=True)
    id = Column(Integer, primary_key=True)
    items = relationship('Item', cascade='delete')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class Item(Base):

    __tablename__ = 'item'

    name = Column(String(40), nullable=False)
    description = Column(String(120), nullable=True)
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)
