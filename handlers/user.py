#encoding=utf8

__author__ = 'Administrator'

import tornado.web
from base import BaseHandler

class LoginHandler(BaseHandler):

    def get(self):
        if self.get_secure_cookie("current_user"):
            self.redirect("/modify")
        self.render("login.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        if not username and password:
            self.render("login.html", error="empty username or password.")

        user = self.db.get("select * from users where username = %s and password = %s and isdeleted = 0",
                           username, password)
        if not user:
            self.render("login.html", error="please check your username and password.")
        self.set_secure_cookie("current_user", str(username))
        self.redirect("/modify")


class LogoutHandler(BaseHandler):

    def get(self):
        current_user = self.get_secure_cookie("current_user")
        self.mem.delete("current_user_" + current_user)
        self.clear_cookie("current_user")
        self.redirect("/")


class RegisterHandler(BaseHandler):

    def get(self):
        self.render("register.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        email = self.get_argument("email")
        phone = self.get_argument("phone")
        name = self.get_argument("name")

        if not username and password and email and phone and name:
            print 'error'
            self.render("register.html", error="please complete all required data and try it again.")

        self.db.execute("insert into users (username, password, email, phone, name) values (%s, %s, %s, %s, %s)",
                        username, password, email, phone, name)

        self.set_secure_cookie("current_user", str(username))

        self.redirect("/modify")


class UsernameIsValidHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")

        if not username:
            return False

        isValid = self.db.get("select count(1) from users where username = %s", username)
        if isValid and int(isValid) > 0:
            return True
        return False


class UserModifyHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        username = self.get_secure_cookie("current_user")

        if not username:
            self.redirect("/")
            return
        my = self.db.get("select * from users where username = %s", username)
        self.render("user_modify.html", my=my)

    @tornado.web.authenticated
    def post(self):
        username = self.get_secure_cookie("current_user")

        if not username:
            self.redirect("/")
            return

        email = self.get_argument("email")
        phone = self.get_argument("phone")
        name = self.get_argument("name")

        self.db.execute("update users set email = %s, phone = %s, name = %s where username = %s",
                        email, phone, name, username)
        my = self.db.get("select * from users where username = %s", username)
        self.render("user_modify.html", message="update success", my=my)






