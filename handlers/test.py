# coding: utf-8

from tornado import web
from tornado import gen
from model import *
from model.db import db_session, redis_connect
import json


class TestHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        food = db_session.query(Food).all()
        food_list = [f.name for f in food]
        self.render('test.html', title='food_list', items=food_list)

    def post(self, *args, **kwargs):
        response = self.request.body
        print(response, '???')


