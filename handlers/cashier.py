from tornado import gen, escape
from model import *
from model.db import db_session, redis_connect
import json
from tornado import web
from sqlalchemy import desc
import uuid
import time


class AllocationHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        num = [int(i.decode('utf-8')) for i in redis_connect.smembers('table_client')]
        print(num)
        al = [i+1 for i in range(10)]
        checkin_time = {}
        for i in redis_connect.hgetall('test'):

            key = int(i.decode('utf-8'))
            print(type(key))
            checkin_time[key] = redis_connect.hgetall('test')[i].decode('utf-8')
        print('time', checkin_time)
        self.render('cashier.html', num=num, all=al, time=checkin_time)

    def post(self, *args, **kwargs):
        response = json.loads(self.request.body.decode('utf-8'))
        # table_num is a set to store the table'num in used
        # table_clniet is a set to store the table'num not in used
        # time is a set to store customer's checkin time
        if response['action'] == 'get_num':
            print(response)
            num = response['num']
            if not num:
                # self.write('已经没有空闲的桌号')
                data = {'msg': '已经没有空闲的桌号'}
                self.write(escape.json_encode(data))
            elif num:
                data = {'msg': str(num)}
                redis_connect.hset('test', int(num), time.strftime('%H:%M:%S', time.localtime(time.time())))
                redis_connect.sadd('table_num', num)
                redis_connect.srem('table_client', num)
                self.write(escape.json_encode(data))
        if response['action'] == 'to_be_finish':
            table = response['table']
            redis_connect.sadd('table_client', int(table))
            total_fee = 0
            food_list = ''
            for i in redis_connect.lrange(str(int(table)+3000), 0, -1):
                total_fee += db_session.query(Food).filter(Food.name == i).first().price
                food_list += (i.decode('utf-8'))+','
            Menu.create(food=food_list, id=str(uuid.uuid4()), table_num=int(table))
            # clean the finished food

            try:
                redis_connect.srem('table_num', int(table))
                redis_connect.ltrim(table, 2, 1)
                redis_connect.ltrim(str(int(table) + 3000), 2, 1)
            except:
                print('clean error')
            data = {'msg': '您好，总额为'+str(total_fee)+'\n菜品:\n'+str(food_list)}
            self.write(escape.json_encode(data))
