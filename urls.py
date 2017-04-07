from handlers import *

url_patterns = [
    (r"/", IndexHandler),
    (r"/menu", AddMenuHandler),
    (r"/menustatus/(?P<table>[\d]+)", MenuStatus),
    (r"/test", TestHandler),
]