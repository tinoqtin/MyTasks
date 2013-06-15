#encoding=utf8

__author__ = 'Administrator'

import tornado.web
from base import BaseHandler
from topic import getMemTopics

#任务列表
class TasksHandler(BaseHandler):

    def get(self):
        userId = self.get_current_user().Id
        tasks = self.db.query("select t.*,tp.Name as TopicName from tasks t inner join topics tp on "
                              "tp.Id =  t.TopicId where tp.UserId = %s order by t.Deadline asc", userId)

        self.render("task.html", tasks=tasks)

class TaskDetailHandler(BaseHandler):
    def get(self):
        id = self.get_argument("id", None)
        if id:
            userId = self.get_current_user().Id
            task = self.db.get("select t.*,tp.Name as TopicName from tasks t inner join topics tp on "
                              "tp.Id =  t.TopicId where t.id = %s and tp.userid = %s", id, userId)
            self.render("task_detail.html",task=task)
        else:
            self.redirect("/task")

#创建修改任务
class TaskComposeHandler(BaseHandler):
    def get(self):
        id = self.get_argument("id", None)
        task = None

        if id:
            task = self.db.get("select * from tasks where id = %s", id)

        self.render("task_compose.html",task=task, mem_topics = getMemTopics(self))

    def post(self):
        topicId = self.get_argument("topicid")
        name = self.get_argument("name")
        deadline = self.get_argument("deadline")
        id = self.get_argument("id", None)

        if not id:
            self.db.execute("insert into tasks(topicid,name,deadline) values (%s,%s,%s)",
                            topicId,name,deadline)
        else:
            self.db.execute("update tasks set topicid = %s, name = %s, deadline = %s where id = %s",
                            topicId, name, deadline, id)

        self.redirect("/task")


#处理任务
class TaskDoHandler(BaseHandler):
    def post(self):
        id = self.get_argument("id", None)
        status = self.get_argument("status", None)
        if id and status:
            self.db.execute("update tasks set status = %s where id = %s",
                            status, id)
            return True
        else:
            return False


class TaskDeleteHandler(BaseHandler):
    def post(self):
        id = self.get_argument("id", None)
        userId = self.get_current_user().Id

        if id:
            task = self.db.get("select t.* from tasks t inner join topics tp on tp.id = t.topicid"
                               "where t.id = %s and tp.userid = %s", id, userId)
            if task:
                self.db.execute("delete from mytasks.references where taskid = %s", id)
                self.db.execute("delete from tasks where id = %s",id)
                return True
            else:
                return False
        return False