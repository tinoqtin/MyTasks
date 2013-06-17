#encoding=utf8

__author__ = 'Administrator'

import tornado.web
from base import BaseHandler
from category import getMemCategories

#主题列表
class TopicsHandler(BaseHandler):
    def get(self, showDeleted=False):
        userId = self.get_current_user().Id

        topics = self.db.query("select t.*,c.name as CategoryName from topics t inner join categories c "
                               "on t.CategoryId = c.Id where userid = %s", userId)

        self.render("topic.html", topics=topics)


#创建/修改主题
class TopicComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        topic = None
        if id:
            topic = self.db.get("select * from topics where id = %s", id)

        self.render("topic_compose.html", topic=topic, mem_categories=getMemCategories(self))

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        categoryId = self.get_argument("categoryid")
        name = self.get_argument("name")
        userId = self.get_current_user().Id

        if not id:
            self.db.execute("insert into topics (userid, categoryid, name) values (%s, %s, %s)",
                            userId, categoryId, name)
            self.redirect("/topic")
            return
        else:
            if id and name and categoryId:
                self.db.execute("update topic set name = %s, categoryid = %s where id = %s and userid = %s",
                                name, categoryId, id, userId)
                self.redirect("/topic")
            else:
                self.render("topic_compose.html", cate={"id": id, "name": name, "categoryid": categoryId})

#删除/恢复主题
class TopicRestoreHandler(BaseHandler):
    pass


#下拉菜单
class TopicSelectModule(tornado.web.UIModule):
    def render(self, topics, id=0):
        return self.render_string("modules/topic_select.html",
                                  topics=topics, id=id)

#下拉菜单
class TopicSelectModule(tornado.web.UIModule):
    def render(self, topics, id=0):
        return self.render_string("modules/topic_select.html",
                                  topics=topics, id=id)


#获取主题
def getTopics(self):
    username = self.get_secure_cookie("current_user")
    if username:
        return self.db.query("select t.* from topics t inner join users u "
                             "on t.userid = u.id where u.username = %s", username)
    return None