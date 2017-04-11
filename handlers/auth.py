# coding: utf-8

from tornado import web, escape
from tornado import gen
from model import *
from model.db import db_session
import json


class IndexHandler(web.RequestHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        self.render('login.html', title='login', items='no')

    def post(self, *args, **kwargs):
        response = json.loads(self.request.body.decode('utf-8'))
        print(response)
        a = response['account']
        p = response['password']
        people = db_session.query(
            People
        ).filter_by(account=a, password=p).first()
        if people:
            url = 'http://127.0.0.1:8080/'+a
            data = {'msg': url}
            self.write(escape.json_encode(data))
        else:
            self.render('login_false.html')
