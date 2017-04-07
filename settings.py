import os
import tornado
from tornado.options import define, options

path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("debug", default=True)
define("port", default=8080, help="run on this port", type=int)
define("address", default="127.0.0.1", help="run on this port", type=str)
MEDIA_ROOT = path(ROOT, "media")
TEMPLATE_ROOT = path(ROOT, "templates")

DOCS_INDEX_ROOT = path(ROOT, "site")

settings = {
    "template_path": TEMPLATE_ROOT,
    "static_path": MEDIA_ROOT,
    "debug": options.debug,
    "autoreload": options.debug
}
