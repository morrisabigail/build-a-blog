#!/usr/bin/env python
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape= True)

# limit = 5
# def get_posts(limit, offset):
#
#     # return posts
#     #self.render("main.html", posts=posts, prev=prev, nxt=nxt)
#     #posts.count(offset=offset, limit=page_size)
# def get_current_page():
#
#     #TODO:returns current page in # format
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

        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")


        # posts.count(limit=limit, offset=offset) # returns TOTAL # of entities
        # if get_current_page == 0:
        #     offset = 0
        # else:
        #     offset = (page_num - 1 ) * items_per_page

        self.render("main.html", posts=posts, heading = "My Blog")


class NewPost(Handler):
    def render_front(self, title ="", txt="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created DESC "

                               )
        self.render("newpost.html", title=title, txt=txt, error=error, posts=posts,heading="New Post")

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        txt = self.request.get("txt")

        if title and txt:
            # creates new instance of Post
            post = Post(title = title, txt = txt)
            #puts new instance in database
            post.put()
            self.render_front()
            post_id = str(post.key().id())
            self.redirect("/blog/"+post_id)
        else:
            error = "Must enter title and text"
            self.render_front(title, txt, error)

class ViewPostHandler(Handler):
    def get(self, id):
        post_id = Post.get_by_id(int(id))
        if not post_id:
            error = "Sorry, we couldn't find what you were looking for"
            self.redirect("/blog?error="+ error)
        self.render("viewpost.html", post_id = post_id)


app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    # ('/blog?page=')
    ('/blog/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
