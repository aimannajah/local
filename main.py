import webapp2
import socialdata
import os


from google.appengine.api import users
from google.appengine.ext.webapp import template

messages = []


def render_template(handler, file_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/', file_name)
    handler.response.out.write(template.render(path, template_values))


def get_user_email():
    user = users.get_current_user()
    if user:
        return user.email()
    else:
        return None


def get_template_parameters():
    values = {}
    if get_user_email():
        values['logout_url'] = users.create_logout_url('/')
    else: 
        values['login_url'] = users.create_login_url('/')
    return values


class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        values['local'] = False
        if get_user_email():
            profile = socialdata.get_user_profile(get_user_email())
            if profile:
                values['firstname'] = profile.firstname
                values['lastname'] = profile.lastname
                values['email'] = profile.email
                values['address'] = profile.address
                values['city'] = profile.city
                values['state'] = profile.state
                values['zipcode'] = profile.zipcode
                values['country'] = profile.country
                values['role'] = profile.role
                print(profile.role)
                if values['role'] == 'local':
                    values['local'] = True
            else:
                self.redirect('/profile-edit')
        render_template(self, 'mainpage.html', values)


class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else: 
            values = get_template_parameters()
            profile = socialdata.get_user_profile(get_user_email())
            if profile:
                values['firstname'] = profile.firstname
                values['lastname'] = profile.lastname
                values['email'] = profile.email
                values['address'] = profile.address
                values['city'] = profile.city
                values['state'] = profile.state
                values['zipcode'] = profile.zipcode
                values['country'] = profile.country
                values['role'] = profile.role
            render_template(self, 'profile-edit.html', values)


class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            print(self.request.get('lastname'))
            error_text = ''
            firstname = self.request.get('firstname')
            lastname = self.request.get('lastname')
            email = self.request.get('email')
            address = self.request.get('address')
            city = self.request.get('city')
            state = self.request.get('state')
            zipcode = self.request.get('zipcode')
            country = self.request.get('country')
            role = self.request.get('role') 

            values = get_template_parameters()
            values['firstname'] = firstname
            values['lastname'] = lastname
            print('email ' + email)
            if error_text:
                values = get_template_parameters()
            else:
                socialdata.save_profile(firstname, lastname, email, address, city, state, zipcode, country, role)
                values['successmsg'] = 'Your profile edits have been saved'
            self.redirect('/profile-view')
            #self.redirect('/profile-view?save=true')


class ProfileViewHandler(webapp2.RequestHandler):
    def get(self):
        profile = socialdata.get_profile_by_email(get_user_email())
        values = get_template_parameters()
        values['profile_save'] = self.request.get('save')
        values['firstname'] = 'Unknown'
        values['lastname'] = 'Unknown'
        values['viewprofile'] = True
        if profile:
            values['firstname'] = profile.firstname
            values['lastname'] = profile.lastname
            values['email'] = profile.email
            values['address'] = profile.address
            values['city'] = profile.city
            values['state'] = profile.state
            values['zipcode'] = profile.zipcode
            values['country'] = profile.country
            values['role'] = profile.role

        print(values)
        render_template(self, 'profile-view.html', values)


class ProfileListHandler(webapp2.RequestHandler):
    def get(self):
        profiles = socialdata.get_recent_profiles()
        values = get_template_parameters()
        values['profiles'] = profiles
        render_template(self, 'profile-list.html', values)


app = webapp2.WSGIApplication([
    ('/profile-view', ProfileViewHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/profile-edit', ProfileEditHandler),
    ('/.*', MainHandler)
])