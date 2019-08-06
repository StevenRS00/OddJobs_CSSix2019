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
    print("profile_key")
        


app = webapp2.WSGIApplication([
    ('/', home)
], debug=True)