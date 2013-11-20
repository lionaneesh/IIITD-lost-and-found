#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import logging
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
import time
from datetime import datetime

from Template_Handler import Handler
from google.appengine.api import search

#-- Database Classes

from Items import Items

#---- Webpage Handlers

class Home(Handler):
    def get(self):
        poster = users.get_current_user()
        lost = db.GqlQuery("SELECT * FROM Items WHERE is_lost=True ORDER BY when DESC LIMIT 4")
        found = db.GqlQuery("SELECT * FROM Items WHERE is_lost=False ORDER BY when DESC LIMIT 4")
        lost = lost.fetch(4)
        found = found.fetch(4)
        self.render("index.html", lost=lost, found=found)

class DisplayItem(Handler):
    def get(self, key):
        poster = users.get_current_user()
        item = db.get(key)
        self.render("displayItem.html", item=item)

class Search(Handler):
    def get(self):
        poster = users.get_current_user()
        query = self.request.get('search').strip()
        index = search.Index(name="itemsIndex")
        items = index.search(query)
        self.render("search.html", items=items)

class Submit(Handler):
    def post(self):
        poster  = users.get_current_user()
        what    = self.request.get('what').strip()
        where   = self.request.get('where').strip()
        when    = self.request.get('when').strip()
        name    = self.request.get('name').strip()
        desc    = self.request.get('desc').strip()
        notes   = self.request.get('notes').strip()
        lost    = self.request.get('lost').strip()
        found   = self.request.get('found').strip()
        image   = self.request.get('image').strip()
        print what, where, when, name, desc, notes, lost, found
        if poster:
            if what and where and when and name and desc and (lost or found):
                when = time.strptime(when, "%Y-%m-%d")
                when = datetime.fromtimestamp(time.mktime(when))
                if image:
                    u = Items(user = poster, what = what, when = when, where = where, name = name, description = desc, notes = notes, is_lost = bool(lost), image=db.Blob(str(image)))
                else:
                    u = Items(user = poster, what = what, when = when, where = where, name = name, description = desc, notes = notes, is_lost = bool(lost))
                u.put()
                if found:
                    res = "Found"
                else:
                    res = "Lost"
                document = search.Document(
                                              fields=[
                                                  search.TextField(name="item_id", value=str(u.key())),
                                                  search.TextField(name='what', value=what),
                                                  search.TextField(name='where', value=where),
                                                  search.TextField(name='name', value=name),
                                                  search.TextField(name='description', value=desc),
                                                  search.TextField(name='foundlost', value=res)])

                index = search.Index(name="itemsIndex")
                index.put(document)
                self.redirect("/items/" + str(u.key()))
            else:
                self.error("504")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Image(webapp2.RequestHandler):
    def get(self):
        item = db.get(self.request.get('img_id'))
        if item.image:
            self.response.headers['Content-Type'] = 'image/' + item.image.split(".")[-1]
            self.response.out.write(item.image)
        else:
            image = db.Blob("/assets/img/RecentLost/1.jpg")
            self.response.headers['Content-Type'] = 'image/' + 'jpg'
            self.response.out.write(image)

app = webapp2.WSGIApplication([(r'/', Home),
                               (r'/submit', Submit),
                               (r'/search', Search),
                               (r'/image', Image),
                               (r'/items/(.*)', DisplayItem),
                               ], debug=True)