#!/usr/bin/env python
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape= True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    title = db.StringProperty(required = True)
    txt = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    def get(self):

        posts = db.GqlQuery("SELECT * FROM Post "
                               "ORDER BY created DESC "
                               "LIMIT 5"
                               )

        self.render("main.html", posts=posts)


class NewPost(Handler):
    def render_front(self, title ="", txt="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post "
                               "ORDER BY created DESC "
                               )
        self.render("newpost.html", title=title, txt=txt, error=error, posts=posts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        txt = self.request.get("txt")

        if title and txt:
            # creates new instance of Post
            a = Post(title = title, txt = txt, key=key)
            #puts new instance in database
            a.put()
            self.render_front()
        else:
            error = "we need both a title and a post"
            self.render_front(title, txt, error)

class ViewPostHandler(Handler):
    def get(self, id):
        post_id = Post.get_by_id(int(id))
        if not post_id:
            self.redirect("/blog/?error=")
        self.render("viewpost.html", post_id = post_id)


app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/blog/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
