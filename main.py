import webapp2
import os
import jinja2
from google.appengine.api import users
from models import Posts
from models import Profile

jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class home(webapp2.RequestHandler):
    def get(self):
        start_template=jinja_current_directory.get_template("templates/homepage.html")
        self.response.write(start_template.render())
        
        
def run_query_posts(name, about, difficulty):
    post = Posts(title = name, description = about, complexity = difficulty)
    post_key = post.put()
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(post_key)
    
def run_query_profile(fname, lname, mail, number):
    profile = Profile(first_name = fname, last_name = lname, email = mail, phone_number = number)
    profile_key = profile.put()
    print("@@@@@@@@@@@@@@@@@@@")
    print(profile_key)

class EnterInfoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user:
            email_address= user.nickname()
            logout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
            self.response.write("You're logged in as " + email_address + "<br>" + logout_link_html)
            
            oj_user = Profile.query().filter(Profile.email == email_address).get()
            if oj_user:
                self.response.write('''
                    Welcome %s %s (%s)! <br> %s <br>''' % (
                      oj_user.first_name,
                      oj_user.last_name,
                      email_address,
                      logout_link_html))  
            else:
                self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            First Name<input type="text" name="first_name">
            <br>
            Last Name<input type="text" name="last_name">
            <br>
            Email <input type="text" name="email"> 
            <br>
            Phone Number <input type="text" name="phone_number"> 
            <br>
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, logout_link_html))
            
        else:
            login_url = users.create_login_url('/')
            login_html_element = '<a href="%s">Sign in</a>' % login_url
            
            self.response.write("Please log in. <b>" + login_html_element)

    def post(self):
        user = users.get_current_user()
        oj_user = Profile(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            phone_number=self.request.get('phone_number'),
            email=user.nickname())
        oj_user.put()
        self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' % oj_user.first_name)


app = webapp2.WSGIApplication([
    ('/', EnterInfoHandler)
], debug=True)