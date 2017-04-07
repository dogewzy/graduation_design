# coding: utf-8

import datetime
from sqlalchemy import Column
from sqlalchemy.types import Unicode, DateTime, Integer
from .db import Model


class People(Model):
    __tablename__ = 'people'
    id = Column(Unicode(70), unique=True,
                nullable=False, primary_key=True)
    name = Column(Unicode(255))
    menu_id = Column(Unicode(255), default=u'')
    role = Column(Unicode(255))
    password = Column(Unicode(255))
    account = Column(Unicode(255))

    def __repr__(self):
        return str(self.name)+str(self.role)


class Menu(Model):
    __tablename__ = 'menu'
    id = Column(Unicode(70), unique=True,
                nullable=False, primary_key=True)
    table_num = Column(Integer, default=0)
    create_time = Column(DateTime, default=datetime.datetime.now())
    food = Column(Unicode(1500))
    add_food = Column(Unicode(500), default=u'')
    ret_food = Column(Unicode(255), default=u'')

    def __repr__(self):
        return self.table_num


class Food(Model):
    __tablename__ = 'food'
    id = Column(Unicode(70), unique=True,
                nullable=False, primary_key=True)
    name = Column(Unicode(255))
    # 0:not ready, 1:ready
    status = Column(Unicode(64), default=u'0')
    menu_id = Column(Unicode(70), default=u'')
    price = Column(Integer)
    type = Column(Unicode(70))

    def __repr__(self):
        return str(self.name) + str(self.status)
