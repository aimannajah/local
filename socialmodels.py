from google.appengine.ext import ndb


class UserProfile(ndb.Model):
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    email = ndb.StringProperty()
    address = ndb.StringProperty()
    city = ndb.TextProperty()
    state = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    country = ndb.StringProperty()
    role = ndb.StringProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)
