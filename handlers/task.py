#encoding=utf8

__author__ = 'Administrator'

import tornado.web
from base import BaseHandler
from sgmllib import SGMLParser
import urllib
from topic import getTopics

#任务列表
class TasksHandler(BaseHandler):

    def get(self, template="task.html"):
        userId = self.get_current_user().Id
        tasks = self.db.query("select t.*,tp.Name as TopicName from tasks t inner join topics tp on "
                              "tp.Id =  t.TopicId where tp.UserId = %s order by t.Deadline asc", userId)
        for task in tasks:
            task["References"] = self.db.query("select * from mytasks.references where taskid = %s",task.Id)

        self.render("task.html", tasks=tasks)


class TaskDetailHandler(BaseHandler):
    def get(self):
        id = self.get_argument("id", None)
        if id:
            userId = self.get_current_user().Id
            task = self.db.get("select t.*,tp.Name as TopicName from tasks t inner join topics tp on "
                              "tp.Id =  t.TopicId where t.id = %s and tp.userid = %s", id, userId)
            references = self.db.query("select * from mytasks.references where taskid = %s",id)
            self.render("task_detail.html", task=task, references=references)
        else:
            self.redirect("/task")


#创建修改任务
class TaskComposeHandler(BaseHandler):
    def get(self):
        id = self.get_argument("id", None)
        task = None

        if id:
            task = self.db.get("select * from tasks where id = %s", id)

        self.render("task_compose.html",task=task, mem_topics=getTopics(self))

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


class RefComposeHandler(BaseHandler):

    def post(self):
        taskId = self.get_argument("taskid", None)
        url = self.get_argument("url", None)

        if taskId and url:
            title = loadUrlTitle(url)
            self.db.execute("insert into mytasks.references(taskid,url,title) values (%s,%s,%s)",
                            taskId, url, title)
        self.redirect("/task/detail?id=" + taskId)


class RefDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        result = False
        if id:
            self.db.execute("delete from mytasks.references where id = %s", id)
            result = True

        self.write({"result": result})


class URLListener(SGMLParser):

    def reset(self):
        SGMLParser.reset(self)
        self.found_title = 0
        self.title = ""

    def start_title(self, attrs):
       self.found_title = 1

    def end_title(self):
        self.found_title = 0

    def handle_data(self, text):
        if self.found_title > 0:
            self.title = text.decode("utf8").encode("utf8")


def loadUrlTitle(url):
    try:
        sock = urllib.urlopen(url)
        parser = URLListener()
        parser.feed(sock.read())
    except:
        raise tornado.web.HTTPError(500)
    finally:
        sock.close()
        parser.close()
        return parser.title