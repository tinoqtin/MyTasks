#encoding=utf8

__author__ = 'Administrator'

import tornado.web
from base import BaseHandler


#主题列表
class TopicsHandler(BaseHandler):
    def get(self):
        userid = self.get_current_user().Id
        topics = self.db.query("select * from topics where userid = %s", userid)
        self.render("topic.html", topics=topics)


#创建/修改主题
class TopicComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        topic = None
        if id:
            topic = self.db.get("select * from topics where id = %s", id)

        self.render("topic_compose.html", topic=topic)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        categoryid = self.get_argument("categoryid")
        name = self.get_argument("name")
        userid = self.get_current_user().Id

        if not id:
            self.db.execute("insert into topics (userid, categoryid, name) values (%s, %s, %s)",
                            userid, categoryid, name)
            self.redirect("/category")
            return
        else:
            if id and name and categoryid:
                self.db.execute("update topic set name = %s, categoryid = %s where id = %s and userid = %s",
                                name, categoryid, id, userid)
                self.redirect("/topic")
            else:
                self.render("topic_compose.html", cate={"id": id, "name": name, "categoryid": categoryid})

#删除/恢复主题
class TopicRestoreHandler(BaseHandler):
    pass

