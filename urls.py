from handlers import *

url_patterns = [
    (r"/", IndexHandler),
    (r"/menu", AddMenuHandler),
    (r"/waiter", AddMenuHandler),
    (r"/menustatus/(?P<table>[\d]+)", MenuStatus),
    (r"/test", TestHandler),
    (r"/cashier", AllocationHandler),
    (r"/admin", AdminHandler),
    (r"/chef", ChefHandler),
]