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
    image = ndb.BlobKeyProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)

class Experience(ndb.Model):
    location = ndb.StringProperty()
    experiencename = ndb.StringProperty()
    description = ndb.TextProperty()
    starttime = ndb.StringProperty()
    endtime = ndb.StringProperty()
    category = ndb.StringProperty()
    price = ndb.StringProperty()
    latestpost = ndb.DateTimeProperty(auto_now=True)
