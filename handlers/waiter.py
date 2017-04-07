# coding: utf-8

from tornado import web
from tornado import gen, escape
from model import *
from model.db import db_session, redis_connect
import json

import uuid


class AddMenuHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        food = db_session.query(Food).all()
        food_list = [f.name for f in food]
        self.render('menu.html', title='food_list', items=food_list)

    def post(self, *args, **kwargs):
        response = json.loads(self.request.body.decode('utf-8'))
        print(response, '===================')
        food_list = response['food'].split(',')[0:-1]
        table_num = int(response['table'])
        menu_id = str(uuid.uuid4())
        for i in food_list:
            redis_connect.lpush(table_num, i)
        Menu.create(food=response['food'], id=menu_id, table_num=table_num)


class MenuStatus(web.RequestHandler):
    def get(self, table):
        food_status = {}
        total_food = []
        menu = db_session.query(Menu).filter(Menu.table_num == table).first()
        food = db_session.query(Food).all()
        for tasty in food:
            total_food.append(tasty.name)

        food_list = menu.food.split(',')[0:-1]
        for i in redis_connect.lrange(table, 0, -1):
            i = i.decode('utf-8')
            food_status[i] = '未完成'

        self.render('menu_status.html', food_list=food_list, food_status=food_status)

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        if data['action'] == 'add':
            self.write(escape.json_encode({'a': 1}))
        elif data['action'] == 'flush':
            pass


