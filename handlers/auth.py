# coding: utf-8

from tornado import web
from tornado import gen
from model import *
from model.db import db_session


class IndexHandler(web.RequestHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        self.render('login.html', title='login', items='no')

    def post(self, *args, **kwargs):
        a = self.get_argument('account')
        p = self.get_argument('password')
        people = db_session.query(
            People
        ).filter_by(account=a, password=p).first()
        if people:
            self.render('%s.html' % people.role)
        else:
            self.render('login_false.html')
