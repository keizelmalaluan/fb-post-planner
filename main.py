import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import json
import jinja2
import webapp2
import logging


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
class YourPost(ndb.Model):
    fbookid = ndb.StringProperty(indexed=False)
    accesstoken = ndb.StringProperty(indexed=False)
    message = ndb.StringProperty(indexed=False)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        self.response.write(template.render())
    def post(self):
    	yourpost = YourPost()
    	yourpost.fbookid = self.request.get("facebookid1")
    	yourpost.accesstoken = self.request.get("access_token1")
    	yourpost.message = self.request.get("msg1")
    	yourpost.put()
    	self.redirect("/")

class PostHandler(webapp2.RequestHandler):
    def post(self):
    	data = {
                    "method": "post",
                    "message": self.request.get('msg'),
                    "access_token": self.request.get('access_token')
        };
        fbid = self.request.get("facebookid")
    	form_data = urllib.urlencode(data)
    	url = "https://graph.facebook.com/v2.1/"+fbid+"/feed"
    	result = urlfetch.fetch(url=url,payload=form_data,method=urlfetch.POST)
    	content = json.loads(result.content)
    	self.redirect("/")


application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post', PostHandler)
], debug=True)