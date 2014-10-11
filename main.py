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
import json
from datetime import datetime,timedelta

import sched
import time
import threading

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
fba = "asdasd"
class YourPost(ndb.Model):
    fbookid = ndb.StringProperty(required=True)
    accesstoken = ndb.StringProperty(required=True)
    message = ndb.StringProperty()
    date_to_post = ndb.DateTimeProperty()
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        self.response.write(template.render())
    def post(self):
    	yourpost = YourPost()
    	yourpost.fbookid = self.request.get("facebookid1")
        fba = self.request.get("facebookid1")
        acctoken = self.request.get("access_token1")
        token = short_to_long_lived(acctoken, self)
        token = decode_response(token)
        yourpost.accesstoken = token["access_token"]
    	message = self.request.get("msg1")
        yourpost.message = message.upper()
        yourpost.date_to_post = datetime.strptime(self.request.get("datetopost"),'%m/%d/%Y %I:%M %p')
    	yourpost.put()
    	self.redirect("/")

def decode_response(str):
    access_token = str.split("&")[0].split("=")[1]
    return {
        "access_token" : access_token,
    }


def short_to_long_lived(access_token,self):
    url = "https://graph.facebook.com/oauth/access_token"
    data = {
        "grant_type" : "fb_exchange_token",
        "fb_exchange_token": access_token,
        "client_id" : "636107513170917",
        "client_secret" : "6ed9606e1e9faf44a94b7dae5e3a8700"
        
    }
    form_data = urllib.urlencode(data)
    result = urlfetch.fetch(url=url,payload=form_data,method=urlfetch.POST)
    return result.content


class ListHandler(webapp2.RequestHandler):
    def get(self,anyd):
        fbid = anyd
        yourpost = YourPost.query(ndb.AND(YourPost.date_to_post >= datetime.now()+timedelta(hours=8)),YourPost.fbookid == fbid).fetch()
        template_values = {
            "all_post": yourpost
        }
        template = JINJA_ENVIRONMENT.get_template('templates/list.html')
        self.response.write(template.render(template_values))

class PostHandler(webapp2.RequestHandler):
    def post(self):
    	data = {
                    "method": "post",
                    "message": self.request.get('msg').upper(),
                    "access_token": self.request.get('access_token')
        };
        fbid = self.request.get("facebookid")
    	form_data = urllib.urlencode(data)
    	url = "https://graph.facebook.com/v2.1/"+fbid+"/feed"
    	result = urlfetch.fetch(url=url,payload=form_data,method=urlfetch.POST)
    	content = json.loads(result.content)
    	self.redirect("/")

class PostAllScheduledPosts(webapp2.RequestHandler):
    def get(self):
            fbid = self.request.get("facebookid")
            que = YourPost.query(ndb.AND(YourPost.date_to_post <= datetime.now()+timedelta(hours=8))).fetch()
            for p in que:
                data = {
                    "method": "post",
                    "message": p.message,
                    "access_token": p.accesstoken
                };
                fbid = self.request.get("facebookid")
                form_data = urllib.urlencode(data)
                url = "https://graph.facebook.com/v2.1/"+fbid+"/feed"
                result = urlfetch.fetch(url=url,payload=form_data,method=urlfetch.POST)
                content = json.loads(result.content)
                p.key.delete()


application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post', PostHandler),
    ('/list/(.*)', ListHandler),
    ('/delay/post', PostAllScheduledPosts)
], debug=True)