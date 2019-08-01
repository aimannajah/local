import datetime
import logging
import os
import webapp2
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
import socialdata
from google.appengine.api import mail

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
    email = get_user_email()
    if email:
        values['Traveller'] = socialdata.is_traveller(email)
        values['Local'] = socialdata.is_local(email)
        values['logout_url'] = users.create_logout_url('/')
    else:
        values['login_url'] = users.create_login_url('/')
    return values

def get_experience_name(city):
    experience = socialdata.show_experience(city)
    if experience:
        return experience.experiencename()
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
            print('\n \n profile \n \n') 
            print(profile)
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
                print('\n \n hello \n \n \n')
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
            date = self.request.get('date')
            starttime = self.request.get('starttime')
            endtime = self.request.get('endtime')
            category = self.request.get('category')
            price = self.request.get('price')
            socialdata.save_experience(city, state, experiencename, description, date, starttime, endtime, category, price, email)
            print(description)
        render_template(self, 'create-experience.html', {})

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
        city = self.request.get('city')
        print(city)
        # city = 'Tucson'
        values = get_template_parameters()
        # values = self.request.get('city') dictionary
        values['experiences'] = socialdata.show_experience(city)
        print(values['experiences'])
        render_template(self, 'view-experience.html', values)

class RequestExperienceHandler(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id')
        experience = socialdata.retrieve_experience(id)
        profile = socialdata.get_user_profile(get_user_email())
        print(experience)
        from_address = "admin@localll.appspotmail.com"
        email = experience.email
        body = "New Experience Request for " + experience.experiencename + " from: " + profile.firstname + " " + profile.lastname + ". Visit localll.appspot.com/searchexperience to accept or reject "  + profile.firstname + "'s request."
        # body = """
        # New Experience request for {{experience.experiencename}} from {{profile.name}} {{profile.lastname}} has been received. Visit localll.appspot.com/accept-reject to accept or reject {{profile.firstname}}'s requqest.
        # """
        subject = "Request from " + profile.firstname
        mail.send_mail(from_address, email, subject, body)
        self.redirect('/searchexperience')


class AcceptRejectHandler(webapp2.RequestHandler):
    def post(self):
        pass


        
        # if experience.email:
        #     self.redirect("/new-request?experience=get_experience_id")
        #     mail.send_mail(from_address, experience.email, body, subject)
        # else:
        #     self.redirect("/signuppage") ###
        # these lines should go right below the def get(Self) and then make sure 


app = webapp2.WSGIApplication([
    ('/profile-view', ProfileViewHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/profile-edit', ProfileEditHandler),
    # ('/experiences', ExperiencesHandler),
    ('/experiences/create', CreateExperienceHandler),
    ('/experiences/save', SaveExperienceHandler),
    ('/searchexperience', SearchExperienceHandler),
    ('/viewexperience', ViewExperienceHandler),
    ('/requestexperience', RequestExperienceHandler),
    ('/accept-reject', AcceptRejectHandler),
    ('/', MainHandler),
    # ('.*', ErrorHandler),
])
