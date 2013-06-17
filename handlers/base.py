#encoding=utf8

__author__ = 'Administrator'

import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.task_count = self.db.get("select count(1) as task_count from tasks t "
                                      "inner join topics tp on tp.id = t.topicid "
                                      "inner join users u on u.id = tp.userid "
                                      "where t.status = 0 and u.username = %s",
                                      self.get_secure_cookie("current_user"))["task_count"]
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

