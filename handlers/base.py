#encoding=utf8

__author__ = 'Administrator'

import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    @property
    def mem(self):
        return self.application.mem

    def get_current_user(self):
        username = self.get_secure_cookie("current_user")

        if not username:
            return None
        return self.db.get("select * from users where username = %s", username)
