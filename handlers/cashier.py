from tornado import gen, escape
from model import *
from model.db import db_session, redis_connect
import json
from tornado import web
from sqlalchemy import desc
import uuid


class AllocationHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        num = [int(i.decode('utf-8')) for i in redis_connect.smembers('table_client')]
        print(num)
        al = [i+1 for i in range(10)]
        self.render('cashier.html', num=num, all=al)

    def post(self, *args, **kwargs):
        response = json.loads(self.request.body.decode('utf-8'))
        # table_num is a set to store the table'num in used
        # table_clniet is a set to store the table'num not in used
        if response['action'] == 'get_num':
            print(response)
            num = response['num']
            if not num:
                # self.write('已经没有空闲的桌号')
                data = {'msg': '已经没有空闲的桌号'}
                self.write(escape.json_encode(data))
            elif num:
                data = {'msg': str(num)}
                redis_connect.sadd('table_num', num)
                redis_connect.srem('table_client', num)
                self.write(escape.json_encode(data))
        if response['action'] == 'to_be_finish':
            table = response['table']
            redis_connect.sadd('table_client', int(table))

            try:
                redis_connect.srem('table_num', int(table))
                redis_connect.ltrim(table,2,1)
            except:
                pass
            total_fee = 0
            food_list = ''
            for i in redis_connect.lrange(str(int(table)+3000), 0, -1):
                total_fee += db_session.query(Food).filter(Food.name == i).first().price
                food_list += (i.decode('utf-8'))+','
            Menu.create(food=food_list, id=str(uuid.uuid4()), table_num=int(table))
            # clean the finished food
            redis_connect.ltrim(str(int(table)+3000), 2, 1)
            data = {'msg': '您好，总额为'+str(total_fee)+'\n菜品:\n'+str(food_list)}
            self.write(escape.json_encode(data))
