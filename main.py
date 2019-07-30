import webapp2
import socialdata
import os

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext.webapp import template


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
        values['login_url'] = users.create_login_url('/profile-view')
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
                values['type'] = profile.role
                print(profile.role)
                if values['type'] == 'local':
                    values['local'] = True
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
            role = self.request.get('type')


            values = get_template_parameters()
            values['firstname'] = firstname
            values['lastname'] = lastname


            if error_text:
                values = get_template_parameters()
            else:
                socialdata.save_profile(firstname, lastname, email, address, city, state, zipcode, country, role)
                values['successmsg'] = 'Your profile edits have been saved'
            render_template(self, 'profile-view.html', values)


class ProfileViewHandler(webapp2.RequestHandler):
    def get(self):
        profile = socialdata.get_profile_by_email(get_user_email())
        values = get_template_parameters()
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
            values['description'] = profile.description
        print(values)
        render_template(self, 'profile-view.html', values)


class ProfileListHandler(webapp2.RequestHandler):
    def get(self):
        profiles = socialdata.get_recent_profiles()
        values = get_template_parameters()
        values["profiles"] = profiles
        render_template(self, "profile-list.html", values)


class EmailHandler(webapp2.RequestHandler):

    def post(self):
        name = self.request.get("name")
        experience = self.request.get("experience")
        email = self.request.get("email")

        params = {
            "name": name,
            "experience": experience,
            "email": email

        }

        from_address = "local@mail.appspot.mail.com"
        subject = "New Request from: " + name
        body = "Request from " + email + ": \n\n" + experience

        # this has to be either an admin address, or:
        # YOUR_APP_ID@mail.appspot.mail.com - YOUR_APP_ID is your project ID

        mail.send_mail(from_address, email, body, subject)
        render_template(self, "newrequest.html", params)

        #functions for each email -def : new experience, request, confirmation

    def newrequest(self, params):
        name = self.request.get("name")
        experience = self.request.get("experience")
        email = self.request.get("email")
        from_address = "local@mail.appspot.mail.com"

        if button.form["accept"] == "Accept":
            mail.send_mail(from_address, email)
            render_template(self, "accept.html", params)
            #send email back saying request has been accepted

        elif button.form["reject"] == "Reject":
            mail.send_mail(from_address, email)
            render_template(self, "reject.html", params)
            #send email back saying request has been denied

    def confirmation(self, params):
        name = self.request.get("name")
        experience = self.request.get("experience")
        email = self.request.get("email")
        from_address = "local@mail.appspot.mail.com"

        mail.send_mail(from_address, email)
        render_template(self, "confirmation.html", params)
        #if new profile is made, send email to new users

    def newexperience(self, params):
        name = self.request.get("name")
        experience = self.request.get("experience")
        email = self.request.get("email")
        from_address = "local@mail.appspot.mail.com"

        mail.send_mail(from_address, email)
        render_template(self, "newexperience.html", params)
        #when user creates a new experience, send email


app = webapp2.WSGIApplication([
    ('/profile-list', ProfileListHandler),
    ('/profile-view', ProfileViewHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/profile-edit', ProfileEditHandler),
    (, EmailHandler),
    ('.*', MainHandler)
])


