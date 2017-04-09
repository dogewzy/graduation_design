from tornado import gen, escape
from model import *
from model.db import db_session, redis_connect
import json
from tornado import web
import uuid


class AllocationHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('cashier.html')

    def post(self, *args, **kwargs):
        response = json.loads(self.request.body.decode('utf-8'))
        # table_num is a set to store the table_num not used
        if response['action'] == 'get_num':
            num = redis_connect.spop('table_client')
            if not num:
                # self.write('已经没有空闲的桌号')
                data = {'msg': '已经没有空闲的桌号'}
                self.write(escape.json_encode(data))
            elif num:
                data = {'msg': str(num)}
                self.write(escape.json_encode(data))
        if response['action'] == 'to_be_finish':
            table = response['table']
            redis_connect.sadd('table_client', int(table))

            try:
                redis_connect.lrem('table_num', 0, table)
                redis_connect.ltrim(table,2,1)
            except:
                pass
            menu = db_session.query(Menu).filter(Menu.table_num == int(table)).first()
            print(menu.food)
            total_fee = menu.total_fee()
            data = {'msg': '您好，总额为'+str(total_fee)}
            self.write(escape.json_encode(data))
