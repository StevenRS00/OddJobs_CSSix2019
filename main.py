import webapp2
import jinja2
import os
from models import Posts, Profile
from google.appengine.api import users
from google.appengine.ext import db


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def checkLoggedInAndRegistered(request):
    # Check if profile is logged in
    
    profile = users.get_current_user()
        
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
        
        profile_posts = Posts.query()
        
        the_variable_dict = {
            "logout_url":  users.create_logout_url('/'),
            "profile_posts": profile_posts
        }
        
        welcome_template = the_jinja_env.get_template('templates/homepage.html')
        self.response.write(welcome_template.render(the_variable_dict))

    def post(self):
        checkLoggedInAndRegistered(self)
        
        profile = users.get_current_user()
        
        post = Posts(
            title=self.request.get('title-first-ln'), 
            description=self.request.get('description-second-ln'),
            owner=profile.nickname(),
            phone = self.request.get('phone-number'),
            complexity = self.request.get('post-type')
            
        )
        post_key = post.put()
        self.response.write("Posts created: " + str(post_key) + "<br>")
        self.response.write("<a href='/'>Home</a> | ")
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
        
        profile = users.get_current_user()
        email_address = profile.nickname()
        
        profile_posts = Posts.query().filter(Posts.owner == email_address).fetch()
        print("***********************************************")
        print(profile_posts)
        the_variable_dict = {
            "logout_url":  users.create_logout_url('/'),
            "profile_posts": profile_posts,
        }
        
        profile_posts_template = the_jinja_env.get_template('templates/profile_posts.html')
        self.response.write(profile_posts_template.render(the_variable_dict))
        
        
    def post(self):
        checkLoggedInAndRegistered(self)
        
        profile = users.get_current_user()
        
        post = Posts(
        title=self.request.get('title-first-ln'), 
        description=self.request.get('description-second-ln'),
        owner=profile.nickname(),
        phone = self.request.get('phone-number'),
        complexity=self.request.get('post-type'),
        )
        post_key = post.put()
        self.redirect("/profileposts")

   
        
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        
        login_template = the_jinja_env.get_template('templates/login.html')
        the_variable_dict = {
            "login_url":  users.create_login_url('/')
        }
        
        self.response.write(login_template.render(the_variable_dict))
        

class RegistrationHandler(webapp2.RequestHandler):
    def get(self):
        profile = users.get_current_user()
        
        registration_template = the_jinja_env.get_template('templates/registration.html')
        the_variable_dict = {
            "email_address":  profile.nickname()
        }
        
        self.response.write(registration_template.render(the_variable_dict))
    
    def post(self):
        profile = users.get_current_user()
        
        #Create a new CSSI User in our database
        
        cssi_profile = Profile(
            first_name=self.request.get('first_name'), 
            last_name =self.request.get('last_name'),
            
            email=profile.nickname()
        )
        
        cssi_profile.put()
        
        self.redirect('/')
        
                  
                  
class DeletepostHandler(webapp2.RequestHandler):
    def get(self):
        client = users.get_current_user()
        profile_post = Posts.query().fetch()
        print("&&&&&&&&&&&&&&&&")
        print(profile_post[0])
    
    def post(self):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        postid= self.request.get("postid")
        post=Posts.get_by_id(int(postid))
        post.key.delete()
        print(self.request.get("postid"))
        self.redirect("/profileposts")
    
    
app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/allposts', AllPostssHandler), 
    ('/profileposts', UserPostssHandler), 
    ('/login', LoginHandler),
    ('/register', RegistrationHandler),
    ('/deletepost', DeletepostHandler)
], debug=True) 