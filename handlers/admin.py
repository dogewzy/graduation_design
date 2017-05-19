# coding: utf-8

from tornado import web
from tornado import gen, escape
from model import *
from model.db import db_session, redis_connect
import json

import uuid


class AdminHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        menu = db_session.query(Menu).all()
        people = db_session.query(People).all()
        food = db_session.query(Food).all()
        self.render('admin.html', menu=menu, people=people, food=food)

    def post(self, *args, **kwargs):
        response = json.loads(self.request.body.decode('utf-8'))
        print(response)
        if response['action'] == 'add_food':
            Food.create(name=response['name'], price=response['price'], id=str(uuid.uuid4()))
            data = {'name': response['name']}
            self.write(escape.json_encode(data))
        if response['action'] == 'delete_food':
            the_food = db_session.query(Food).filter(Food.name == response['name']).first()
            the_food.delete()
        if response['action'] == 'update_food':
            the_food = db_session.query(Food).filter(Food.name == response['name']).first()
            the_food.update(price=response['price'])
        if response['action'] == 'add_people':
            People.create(name=response['name'], role=response['role'], id=str(uuid.uuid4()),
                          account=response['account'], password=response['password'])
            data = {'name': response['name']}
            self.write(escape.json_encode(data))
        if response['action'] == 'update_people':
            p = db_session.query(People).filter(People.name == response['name']).first()
            p.update(password=response['password'])
        if response['action'] == 'delete_people':
            p = db_session.query(People).filter(People.name == response['name']).first()
            print(p)
            p.delete()


class DataHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('data.html')


class AnnouncementHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('announcement.html')


class CultureHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('culture.html')

