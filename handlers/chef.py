from tornado import gen, escape
from model import *
from model.db import db_session, redis_connect
import json
from tornado import web
import uuid


class ChefHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        unfinish = []
        for i in redis_connect.smembers('table_num'):
            unfinish.append(i.decode('utf-8'))
        table_status = {}
        for i in unfinish:
            # not finish food
            table_status[i] = [food.decode('utf-8') for food in redis_connect.lrange(i, 0, -1)]
        self.render('chef.html', t=table_status)

    def post(self, *args, **kwargs):
        response = json.loads(self.request.body.decode('utf-8'))
        print(response)
        if response['action'] == 'update_food':
            table = response['table']
            if ',' in table > 1:
                food_list = response['food'].split(',')[0:-1]
            else:
                # single update
                food_list = response['food'].split(',')[0:1]
            for i in food_list:
                redis_connect.lrem(table, 1, i)
                redis_connect.lpush(str(int(table)+3000), i)
        self.write('success')