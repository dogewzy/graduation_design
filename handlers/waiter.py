# coding: utf-8

from tornado import web
from tornado import gen, escape
from model import *
from model.db import db_session, redis_connect
import json
from sqlalchemy import desc
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
        # menu_id = str(uuid.uuid4())
        for i in food_list:
            redis_connect.lpush(table_num, i)
        # Menu.create(food=response['food'], id=menu_id, table_num=table_num)


class MenuStatus(web.RequestHandler):
    def get(self, table):
        if bytes(table, 'utf-8') not in redis_connect.smembers('table_num'):
            self.render('menu_status.html', food_list='', food_status='', table=table)
        else:
            food_status = {}
            for i in redis_connect.lrange(table, 0, -1):
                i = i.decode('utf-8')
                food_status[i] = '未完成'
            for each in redis_connect.lrange(str(int(table)+3000), 0, -1):
                food_status[each] = '已完成'
            self.render('menu_status.html', food_status=food_status, table=table)

    def post(self, *args, **kwargs):
        response = json.loads(self.request.body.decode('utf-8'))
        if response['action'] == 'bu':
            table = response['table']
            for f in response['food'].split(',')[0:-1]:
                redis_connect.lpush(table, f)
            self.write('success')
        if response['action'] == 'tui':
            result = '退点成功'
            table = response['table']
            tui_food = response['food'].split(',')[0:-1]
            unfinish = []
            finish = []
            for i in redis_connect.lrange(table, 0, -1):
                unfinish.append(i.decode('utf-8'))
            for i in redis_connect.lrange(str(int(table)+3000), 0, -1):
                finish.append(i.decode('utf-8'))
            for f in tui_food:
                if f in unfinish:
                    pass
                elif f in finish:
                    result = '菜肴已经制作完成或者不在原始订单中'
                    break
            if result == '退点成功':
                for f in tui_food:
                    redis_connect.lrem(table, 1, f)
            data = {'msg': result}
            self.write(escape.json_encode(data))


