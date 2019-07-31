import datetime
import logging
import os
import webapp2
import jinja2
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
import socialdata

messages = []

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


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
    email = get_user_email()
    if email:
        values['Traveller'] = socialdata.is_traveller(email)
        values['Local'] = socialdata.is_local(email)
        values['logout_url'] = users.create_logout_url('/')
    else: 
        values['login_url'] = users.create_login_url('/')
    return values

def get_experience_name():
    experience = users.show_experience()
    if experience:
        return experience.name()
    else:
        return None

class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        values['Local'] = False
        values['experiences'] = True
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
                if values['role'] == 'Local':
                    values['Local'] = True
            # else:
            #     self.redirect('/profile-edit')
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
            self.redirect('/profile-view')


class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
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
                print(email)
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
            values['type'] = profile.role
            values['role'] = profile.role
        print(values)
        render_template(self, 'profile-view.html', values)

class ProfileListHandler(webapp2.RequestHandler):
    def get(self):
        profiles = socialdata.get_recent_profiles()
        values = get_template_parameters()
        values['profiles'] = profiles
        render_template(self, 'profile-list.html', values)
    
class CreateExperienceHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        values['experiences'] = True
        if not get_user_email():
            self.redirect('/')
        else:
            render_template(self, 'create-experience.html', values)

class SaveExperienceHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            city = self.request.get('city')
            state = self.request.get('state')
            experiencename = self.request.get('experiencename')
            description = self.request.get('description')
            starttime = self.request.get('starttime')
            endtime = self.request.get('endtime')
            category = self.request.get('category')
            price = self.request.get('price')
            socialdata.save_experience(city, state, experiencename, description, starttime, endtime, category, price)
            self.redirect('/experience/view')

class ManageExperienceHandler(webapp2.RequestHandler):
    def post(self):
        
        render_template(self, 'manage-experience.html', {})

class ExperienceHandler(webapp2.RequestHandler):
    def get(self):
        render_template(self, 'experiences-page.html', {})
class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("nothing mapped there (get).")
    def post(self):
        self.response.out.write('nothing mapped there (post).')

class SearchExperienceHandler(webapp2.RequestHandler):
    def get(self):
        render_template(self, 'search-experience.html', {})

class ViewExperienceHandler(webapp2.RequestHandler):
    def post(self):
        view_template = the_jinja_env.get_template('templates/view-experience.html')
        city = self.request.get('city')
        print(city)
        # city = 'Tucson'
        values = get_template_parameters()
        # values = self.request.get('city') dictionary
        values['experiences'] = socialdata.show_experience(city)
        # values['experiences'] = [[0,1,2],[3,4,5]]
        print(values['experiences'])
        # render_template(self, 'view-experience.html', values)
        self.response.write(view_template.render(values))

app = webapp2.WSGIApplication([
    ('/profile-view', ProfileViewHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/profile-edit', ProfileEditHandler),
    ('/experiences', ExperienceHandler),
    ('/experiences/create', CreateExperienceHandler),
    ('/experiences/save', SaveExperienceHandler),
    ('/experiences/manage', ManageExperienceHandler),
    ('/searchexperience', SearchExperienceHandler),
    ('/viewexperience', ViewExperienceHandler),
    ('/', MainHandler),
    # ('.*', ErrorHandler),
])