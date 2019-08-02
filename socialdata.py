from google.appengine.ext import ndb

from socialmodels import UserProfile
from socialmodels import Experience
from socialmodels import Request

def save_profile(firstname, lastname, email, address, city, state, zipcode, country, role):
    p = get_user_profile(email)
    print(firstname, lastname, email, address, city, state, zipcode, country, role)
    if p is not None:
        p.firstname = firstname
        p.lastname = lastname
        p.email = email
        p.address = address
        p.city = city
        p.state = state
        p.zipcode = zipcode
        p.country = country
        p.role = role
    else:
        p = UserProfile(firstname = firstname, lastname = lastname, email = email, address = address, city = city, state = state, zipcode = zipcode, country = country, role = role)
    print(p)
    p.put()

def is_traveller(email):
    profile = get_user_profile(email)
    if profile and profile.role == 'Traveller':
        return True
    return False

def is_local(email):
    profile = get_user_profile(email)
    if profile and profile.role == 'Local':
        return True
    return False

def get_user_profile(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None

def get_recent_profiles():
    q = UserProfile.query().order(-UserProfile.last_update)
    return q.fetch(50)

def show_experience(city):
    q = Experience.query(Experience.city == city)
    results = q.fetch()
    experiences = []
    for experience in results:
        experiences.append(experience)
        # hard coded at view-experience.html
        # to enter more info, append the necessary information
    return experiences

def retrieve_experience(id):
    print(id)
    q = Experience.get_by_id(long(id))
    print(q)
    # results = q.fetch(1)
    # for experience in results:
    #     return expereience
    # return None
    return q

def request_experience(experienceid, useremail):
    p = Request(experienceid = experienceid, useremail = useremail)
    if p:
        p.experienceid = experienceid
        p.useremail = useremail
    else:
        p = Request(experienceid = experienceid, useremail = useremail)
    p.put()


def update_experience(exp_id, city, state, experiencename, description, date, starttime, endtime, category, price, email):
    exp = ndb.Key(urlsafe=exp_id).get()
    exp.city = city
    exp.state = state
    exp.experiencename = experiencename
    exp.description = description
    exp.date = date
    exp.starttime = starttime
    exp.endtime = endtime
    exp.category = category
    exp.price = price
    exp.email = email
    exp.put()


def save_experience(city, state, experiencename, description, date, starttime, endtime, category, price, email):
    p = Experience(city = city, state = state, experiencename = experiencename, description = description, date = date, starttime = starttime, endtime = endtime, category = category, price = price, email = email)
    if p:
        p.city = city
        p.state = state
        p.experiencename = experiencename
        p.description = description
        p.date = date
        p.sarttime = starttime
        p.endtime = endtime
        p.category = category
        p.price = price
    else:
        p = Experience(city = city, state = state, experiencename = experiencename, description = description, date = date, starttime = starttime, endtime = endtime, category = category, price = price, email = email)
    print('save experience')
    p.put()

def retrieve_requests(email):
    q = Request.query(Request.useremail == email)
    results = q.fetch()
    requests = []
    for request in results:
        requests.append(request)
    return requests

def get_profile_by_email(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None

def get_experience_by_email(email):
    q = Experience.query(Experience.email == email)
    results = q.fetch()
    experiences = []
    for experience in results:
        experiences.append(experience)
    return experiences

# def get_experience_by_id(exp_key):
#     print('##################')
#     print(exp_key)
#     print('###################')
#     key = ndb.Key(urlsafe=exp_key)
#     return key.get()
    