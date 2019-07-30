class NewExperienceHandler(webapp2.RequestHandler):

    def post(self):
        name = self.request.get("name")
        experience = self.request.get("experience")
        user_address = self.request.get("email")
        from_address = "local@mail.appspot.mail.com"
        subject = "New experience created"
        body = experience + "created"

        if new experience created: ####
            mail.send_mail(from_address, user_address, subject, body)
            render_template(self, "newexperience.html")
            # when user creates a new experience, send email


class NewRequestHandler(webapp2.RequestHandler):

    def post(self):
        name = self.request.get("name")
        experience = self.request.get("experience")
        user_address = self.request.get("email")
        "name": name,
        "experience": experience,
        from_address = "local@mail.appspot.mail.com"
        subject = "New Request from: " + name
        body = "Request from " + user_address + ": \n\n" + experience

        # this has to be either an admin address, or:
        # YOUR_APP_ID@mail.appspot.mail.com - YOUR_APP_ID is your project ID

        mail.send_mail(from_address, user_address, body, subject)
        render_template(self, "newrequest.html")

        #functions for each email -def : new experience, request, confirmation


class AcceptOrRejectHandler(webapp2.RequestHandler):

    def post(self):
        #update website
        #then email 

        name = self.request.get("name")
        user_address = self.request.get("email")
        from_address = "local@mail.appspot.mail.com"
        subject = "New Request from: " + name
        body = "Please make a decision on this request."

        if accept button is pressed:####
####
            render_template(self, "accept.html")

        elif:
####


class ConfirmationHandler(webapp2.RequestHandler):

    def post(self):
        name = self.request.get("name")
        from_address = "local@mail.appspot.mail.com"
        user_address = self.request.get("email")
        subject = "New Account Created on LocaL"
        body = name + "has created a new account on LocaL."

        if new user is created: #####
            mail.send_mail(from_address, user_address, subject, body)
            render_template(self, "confirmation.html")
            #if new profile is made, send email to new users


class UserSignupHandler(webapp2.RequestHandler):
    """Serves the email address sign up form."""
    def post(self):
        user_address = self.request.get("email")

        if not mail.is_email_valid(user_address):
            self.get()  # Show the form again.

        else:
            confirmation_url = create_new_user_confirmation(user_address)
            sender_address = (
                local@mail.appspot.mail.com.format(
                    local.get_application_id()))
            subject = "Confirm your registration"
            body = "Thank you for creating an account! Please confirm your" + 
            "email address by clicking on the link below: "

{}
 .format(confirmation_url)
            mail.send_mail(local@mail.appspot.mail.com, user_address, subject, body)


class ContactUsHandler(webapp2.RequestHandler):

    def post(self):
        name = self.request.get("name")
        message = self.request.get("message")
        email = self.request.get("email")

        params = {
          "name": name,
          "message": message,
          "email": email
        }

        # this has to be either an admin address, or:
        # YOUR_APP_ID@mail.appspot.mail.com - YOUR_APP_ID is your project ID
        from_address = "local@mail.appspot.mail.com"
        subject = "Contact from " + name
        body = "Message from " + name + ":\n\n" + message
        mail.send_mail(from_address, email, subject, body)
        render_template(self, "contact.html")