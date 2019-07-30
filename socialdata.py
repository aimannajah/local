from socialmodels import UserProfile
from socialmodels import Experience

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

# def show_experience(city):
#     q = Experience.query(Experience.city == city)
#     results = q.fetch()
#     return results

def save_experience(city, state, experiencename, description, starttime, endtime, category, price):
    # p = show_experience()
    # if not p:
    #     p.city = city
    #     p.state = state
    #     p.experiencename = experiencename
    #     p.description = description
    #     p.starttime = starttime
    #     p.endtime = endtime
    #     p.category = category
    #     p.price = price
    #     p.latestpost = latestpost
    # else:
    p = Experience(city = city, state = state, experiencename = experiencename, description = description, starttime = starttime, endtime = endtime, category = category, price = price)
    p.put()

def get_profile_by_email(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None