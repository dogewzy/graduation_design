from tornado import gen, escape
from model import *
from model.db import db_session, redis_connect
import json
from tornado import web
import uuid
all_menu = []
import random
a = '瓜丝儿、山鸡丁儿、拌海蜇、龙须菜、炝冬笋、玉兰片、浇鸳鸯、烧鱼头、烧槟子、烧百合、炸豆腐、炸面筋、糖熘 儿、拔丝山药、糖焖莲子、酿山药、杏仁酪、小炒螃蟹、氽大甲、什锦葛仙米、蛤蟆鱼、扒带鱼、海鲫鱼、黄花鱼、扒海参、扒燕窝、扒鸡腿儿、扒鸡块儿、扒肉、扒面筋、扒三样儿、油泼肉、酱泼肉、炒虾黄儿、熘蟹黄儿、炒子蟹、佛手海参、炒芡子米、奶汤、翅子汤、三丝汤、熏斑鸠、卤斑鸠、海白米、烩腰丁儿、火烧茨菰、炸鹿尾儿、焖鱼头、拌皮渣儿、氽肥肠儿、清拌粉皮儿、木须菜、烹丁香、烹大肉、烹白肉、麻辣野鸡、咸肉丝儿、白肉丝儿、荸荠、一品锅、素炝春不老、清焖莲子、酸黄菜、烧萝卜、烩银耳、炒银枝儿、八宝榛子酱、黄鱼锅子、 白菜锅子、什锦锅子、汤圆子锅、菊花锅子、煮饽饽锅子、肉丁辣酱、炒肉丝儿'
f = a.split('、')

for i in f:
    Food.create(name=i,price=random.randint(10,50),id=str(uuid.uuid4()))
