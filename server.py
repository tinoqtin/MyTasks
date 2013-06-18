#encoding=utf8

__author__ = 'Administrator'

import os.path
import torndb
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import memcache
from tornado.options import define, options

from handlers.user import *
from handlers.category import *
from handlers.topic import *
from handlers.task import *

define("port", default=8800, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="mytasks database host")
define("mysql_database", default="mytasks", help="mytasks database name")
define("mysql_user", default="root",help="mytasks database user")
define("mysql_password", default="testdb", help="mytasks database password")


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", LoginHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/register", RegisterHandler),
            (r"/modify", UserModifyHandler),
            (r"/my", TasksHandler),
            (r"/category$", CategoriesHandler),
            (r"/category/compose", CateComposeHandler),
            (r"/category/restore", CateRestoreHandler),
            (r"/topic$", TopicsHandler),
            (r"/topic/compose", TopicComposeHandler),
            (r"/topic/restore", TopicRestoreHandler),
            (r"/task$", TasksHandler),
            (r"/task/compose", TaskComposeHandler),
            (r"/task/delete", TaskDeleteHandler),
            (r"/task/detail", TaskDetailHandler),
            (r"/task/ref/compose", RefComposeHandler),
            (r"/task/ref/delete", RefDeleteHandler)
        ]

        settings = dict(
                contact_title=u"My Tasks Ver 0.1",
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                ui_modules={"CategorySelect": CategorySelectModule,
                            "TopicSelect": TopicSelectModule},
                #xsrf_cookies = True,
                cookie_secret="this is my secret password",
                login_url="/",
                debug=True
            )

        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

        self.mem = memcache.Client(["localhost"], debug=False)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()