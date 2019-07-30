import datetime
import logging
import os
import webapp2

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
import socialdata

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
        values['upload_url'] = blobstore.create_upload_url('/upload')
    else: 
        values['login_url'] = users.create_login_url('/profile-view')
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
        print(values)
        render_template(self, 'profile-view.html', values)

class ProfileListHandler(webapp2.RequestHandler):
    def get(self):
        profiles = socialdata.get_recent_profiles()
        values = get_template_parameters()
        values['profiles'] = profiles
        render_template(self, 'profile-list.html', values)
        
# class FileUploadHandler(blobstore_handlers.BloclstoreUploadHandler):
#     def post(self):
#         params = get_template_parameters()

#         if params['user']:
#             upload_files = self.get_uploads()
#             blob_info = upload_files[0]
#             type = blob_info.content_type

#         if type in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
#             name = self.request.get('name')
#             my_image = MyImage()
#             my_image.name = name
#             my_image.user = params['user']

#             my_image.image = blob_info.key()
#             my_image.put()
#             image_id = my_image.key.urlsafe()
#             self.redirect('/image?id=' + image_id)

# class ImageHandler(webapp2.RequestHandler):
#     def get(self):
#         params = get_params()
#         image_id = self.request.get('id')
#         my_image = ndb.Key(urlsafe=image_id).get()
#         params['image_id'] = image_id
#         params['image_name'] = my_image.name
#         render_template(self, 'image.html', params)
        
# class ImageManipulationHandler(webapp2.RequestHandler):
#     def get(self):

#         image_id = self.request.get("id")
#         my_image = ndb.Key(urlsafe=image_id).get()
#         blob_key = my_image.image
#         img = images.Image(blob_key=blob_key)

#         modified = False

#         h = self.request.get('height')
#         w = self.request.get('width')
#         fit = False

#         if self.request.get('fit'):
#             fit = True

#         if h and w:
#             img.resize(width=int(w), height=int(h), crop_to_fit=fit)
#             modified = True

#         optimize = self.request.get('opt')
#         if optimize:
#             img.im_feeling_lucky()
#             modified = True

#         flip = self.request.get('flip')
#         if flip:
#             img.vertical_flip()
#             modified = True

#         mirror = self.request.get('mirror')
#         if mirror:
#             img.horizontal_flip()
#             modified = True

#         rotate = self.request.get('rotate')
#         if rotate:
#             img.rotate(int(rotate))
#             modified = True

#         result = img
#         if modified:
#             result = img.execute_transforms(output_encoding=images.JPEG)

#         self.response.headers['Content-Type'] = 'image/jpeg'
#         self.response.out.write(result)

# class MyImage(ndb.Model):
#     name = ndb.StringProperty()
#     image = ndb.BlobKeyProperty()
#     user = ndb.StringProperty()
    
class CreateExperienceHandler(webapp2.RequestHandler):
    def get(self):
        if not show_experience
        render_template(self, 'add-experience.html', {})

app = webapp2.WSGIApplication([
    ('/profile-list', ProfileListHandler),
    ('/profile-view', ProfileViewHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/profile-edit', ProfileEditHandler),
    # ('/images', ImageHandler),
    # ('/image', ImageHandler),
    # ('/upload', FileUploadHandler),
    # ('/img', ImageManipulationHandler),
    ('/experiences/create', CreateExperienceHandler),
    ('.*', MainHandler)
])