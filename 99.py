from model.models import Menu
from model.db import db_session
menu = db_session.query(Menu).filter(Menu.table_num==66).first()
print(menu.total_fee())


