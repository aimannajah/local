from socialmodels import UserProfile


def save_profile(firstname, lastname, email, address, city, state, zipcode, country, role):
    p = get_user_profile
    if not p:
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
    p.put()


def get_user_profile(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None


def get_profile_by_email(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None

def get_recent_profiles():
    q = UserProfile.query().order(-UserProfile.last_update)
    return q.fetch(50)
