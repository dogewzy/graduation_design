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
        if bytes(table, 'utf-8') not in redis_connect.smembers('table_num'):
            self.render('menu_status.html', food_list='', food_status='', table=table)
        else:
            food_status = {}
            menu = db_session.query(Menu).filter(Menu.table_num == table).first()

            food_list = menu.food.split(',')[0:-1]
            for i in redis_connect.lrange(table, 0, -1):
                i = i.decode('utf-8')
                food_status[i] = '未完成'
            for each in food_list:
                if each not in food_status:
                    food_status[each] = '已完成'
            self.render('menu_status.html', food_list=food_list, food_status=food_status, table=table)

    def post(self, *args, **kwargs):
        response = json.loads(self.request.body.decode('utf-8'))
        result = '退点成功'
        if response['action'] == 'bu':
            table = response['table']
            menu = db_session.query(Menu).filter(Menu.table_num == table).first()
            menu.update(food=menu.food+response['food'], add_food=response['food'])
            for f in response['food'].split(',')[0:-1]:
                redis_connect.lpush(table, f)
            self.write('success')
        if response['action'] == 'tui':
            table = response['table']
            menu = db_session.query(Menu).filter(Menu.table_num == table).first()
            origin_food = menu.food.split(',')[0:-1]
            tui_food = response['food'].split(',')[0:-1]
            redis_data = []
            for i in redis_connect.lrange(table, 0, -1):
                redis_data.append(i.decode('utf-8'))
            # print(origin_food, 'oo')
            # print(tui_food, 'tt')
            # print(redis_data)
            for f in tui_food:
                if f in origin_food and f in redis_data:
                    pass
                else:
                    result = '菜肴已经制作完成或者不在原始订单中'
                    break
            if result == '退点成功':
                for f in tui_food:
                    origin_food.remove(f)
                    redis_connect.lrem(table, 1, f)
                tui_str = ','.join(tui_food)+','
                origin_str = ','.join(origin_food)+','
                menu.update(food=origin_str, tui_food=tui_str)
            data = {'msg': result}
            # print(origin_food, 'oo')
            # print(tui_food, 'tt')
            # print(redis_connect.lrange(table, 0, -1))
            self.write(escape.json_encode(data))


