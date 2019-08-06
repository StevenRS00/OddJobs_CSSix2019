import webapp2
import os
import jinja2
from google.appengine.api import users

jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class home(webapp2.RequestHandler):
    def get(self):
        start_template=jinja_current_directory.get_template("templates/homepage.html")
        self.response.write(start_template.render())

app = webapp2.WSGIApplication([
    ('/', home)
], debug=True)