import webapp2
import jinja2
import os
from models import Posts, Profile
from google.appengine.api import profiles


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def checkLoggedInAndRegistered(request):
    # Check if profile is logged in
    
    profile = profiles.get_current_profile()
        
    if not profile: 
        request.redirect("/login")
        return
    
    # Check if profile is registered
       
    email_address = profile.nickname()
    registered_profile = Profile.query().filter(Profile.email == email_address).get()
    
    if not registered_profile:
         request.redirect("/register")
         return 
    

class HomeHandler(webapp2.RequestHandler):
    def get(self):  
        checkLoggedInAndRegistered(self)
        
        the_variable_dict = {
            "logout_url":  profiles.create_logout_url('/')
        }
        
        welcome_template = the_jinja_env.get_template('templates/homepage.html')
        self.response.write(welcome_template.render(the_variable_dict))

    def post(self):
        checkLoggedInAndRegistered(self)
        
        profile = profiles.get_current_profile()
        
        post = Posts(
            title=self.request.get('title-first-ln'), 
            description=self.request.get('description-second-ln'),
            owner=profile.nickname(),
            complexity=self.request.get('post-type')
        )
        post_key = post.put()
        self.response.write("Posts created: " + str(post_key) + "<br>")
        self.response.write("<a href='/allposts'>All posts</a> | ")
        self.response.write("<a href='/profileposts'>My posts</a>")
        


class AllPostssHandler(webapp2.RequestHandler):
    def get(self):
        checkLoggedInAndRegistered(self)
        
        
        
        all_posts = Posts.query().fetch()
        
        the_variable_dict = {
            "all_posts": all_posts
        }
        
        all_posts_template = the_jinja_env.get_template('templates/all_posts.html')
        self.response.write(all_posts_template.render(the_variable_dict))

class UserPostssHandler(webapp2.RequestHandler):
    def get(self):
        checkLoggedInAndRegistered(self)
        
        profile = profiles.get_current_profile()
        email_address = profile.nickname()
        
        profile_posts = Posts.query().filter(Posts.owner == email_address).fetch()
        
        the_variable_dict = {
            "profile_posts": profile_posts
        }
        
        profile_posts_template = the_jinja_env.get_template('templates/profile_posts.html')
        self.response.write(profile_posts_template.render(the_variable_dict))
   
        

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        
        login_template = the_jinja_env.get_template('templates/login.html')
        the_variable_dict = {
            "login_url":  profiles.create_login_url('/')
        }
        
        self.response.write(login_template.render(the_variable_dict))
        

class RegistrationHandler(webapp2.RequestHandler):
    def get(self):
        profile = profiles.get_current_profile()
        
        registration_template = the_jinja_env.get_template('templates/registration.html')
        the_variable_dict = {
            "email_address":  profile.nickname()
        }
        
        self.response.write(registration_template.render(the_variable_dict))
    
    def post(self):
        profile = profiles.get_current_profile()
        
        #Create a new CSSI User in our database
        
        cssi_profile = Profile(
            first_name=self.request.get('first_name'), 
            last_name =self.request.get('last_name'),
            
            email=profile.nickname()
        )
        
        cssi_profile.put()
        
        self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
        cssi_profile.first_name)
        
                  
    
app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/allposts', AllPostssHandler), 
    ('/profileposts', UserPostssHandler), 
    ('/login', LoginHandler),
    ('/register', RegistrationHandler)
], debug=True) 