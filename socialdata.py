from socialmodels import UserProfile
from socialmodels import Experience

def save_profile(firstname, lastname, email, address, city, state, zipcode, country, role):
    p = get_user_profile(email)
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

def get_user_profile(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None

def get_recent_profiles():
    q = UserProfile.query().order(-UserProfile.last_update)
    return q.fetch(50)

def show_experience(experiencename):
    q = Experience.query(Experience.experiencename == experiencename)
    results = q.fetch(1)
    for experience in results:
        return experience
    return None

def save_experience(location, activityname, description, starttime, endtime, category, price, latestpost):
    p = show_experience()
    if not p:
        p.location = location
        p.activityname = activityname
        p.description = description
        p.starttime = starttime
        p.endtime = endtime
        p.category = category
        p.price = price
        p.latestpost = latestpost
    else:
        p = Experience(location = location, activityname = activityname, description = description, starttime = starttime, endtime = endtime, category = category, price = price, latestpost = latestpost)
    p.put()

def get_profile_by_email(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None