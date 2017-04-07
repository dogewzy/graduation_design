# coding: utf-8

import sys
import getopt
import tornado
from tornado import ioloop, web
from tornado.options import options
from settings import settings
from urls import url_patterns



class Usage(Exception):

    def __init__(self, msg):
        self.msg = msg


class Application(web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    opts, args = getopt.getopt(argv[1:], "h", ["help"])
    """Creates instance of the server and starts IOLoop."""
    tornado.options.parse_command_line()
    application = Application()
    application.listen(options.port, address=options.address)
    tornado.ioloop.IOLoop.current().start()
    #     except getopt.error, msg:
    #         raise Usage(msg)
    #     # more code, unchanged
    # except Usage, err:
    #     print >>sys.stderr, err.msg
    #     print >>sys.stderr, "for help use --help"
    #     return 2

if __name__ == "__main__":
    print('http://' + options.address + ':' + str(options.port))
    sys.exit(main())
