import datetime
import logging
import os
import webapp2

from google.appengine.api import mail
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb


class UserRequests(ndb.Model):
    id = ndb.IntegerProperty(required=True)
    user_address = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    experience = ndb.StringProperty(required=True)
    active = ndb.BooleanProperty(default=True)


class RequestExperienceHandler(webapp2.RequestHandler):

    def get(self):
        html = """
        <html>
            <body>
                <form method="post" action="/">
                    <input type="text" name="emailrequest">
                    <input type="submit" value="Request">
                    <a href="/request-experience">
            </body>
        </html>
        """
        # html

        name = self.request.get("name")
        from_address = "yuh@local.appspotmail.com"
        subject = "New Request from: " + name
        body = "Request from " + get_user_email() + ": \n\n" + \
        get_experience_name()
        user = users.get_current_user()

        if user:
            self.redirect("/new-request?experience=get_experience_id")
            mail.send_mail(from_address, get_user_email(), body, subject)

        else:
            self.redirect("/signuppage") ###
