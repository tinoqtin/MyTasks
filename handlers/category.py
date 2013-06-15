#encoding=utf8

__author__ = 'Administrator'

import tornado.web
from base import BaseHandler


class CateComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        category = None
        if id:
            category = self.db.get("select * from categories where id = %s", id)

        self.render("cate_compose.html", category=category)
    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        name = self.get_argument("name")
        location = self.get_argument("location")

        if not id:
            self.db.execute("insert into categories (name, location) values (%s, %s)",
                            name, location)
            _resetMemCategories(self)
            self.redirect("/category")
            return
        else:
            if id and name and location:
                self.db.execute("update categories set name = %s, location = %s where id = %s",
                                name, location, id)
                _resetMemCategories(self)
                self.redirect("/category")
            else:
                self.render("cate_compose.html", cate={"id": id, "name": name, "location": location})


class CateRestoreHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id")
        status = self.get_argument("status")
        if id and status:
            self.db.execute("update categories set isdeleted = %s where id = %s",
                            status, id)
            _resetMemCategories(self)
            return True
        return False


#分类列表
class CategoriesHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("category.html",
                    categories=_getCategories(self),
                    mem_categories=getMemCategories(self))


#下拉菜单
class CategorySelectModule(tornado.web.UIModule):
    def render(self, categories, id=0):
        return self.render_string("modules/category_select.html",
                                  categories=categories, id=id)


#刷新缓存
def _resetMemCategories(self):
    self.mem.set("categories", _getCategories(self))


def getMemCategories(self):
    mem_categories = self.mem.get("categories")

    if not mem_categories:
        current_categories = _getCategories(self)
        self.mem.set("categories", current_categories)
        return current_categories
    return mem_categories


def _getCategories(self):

    return self.db.query("select * from categories order by location asc")