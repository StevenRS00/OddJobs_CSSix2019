from google.appengine.ext import ndb

class Posts(ndb.Model):
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    complexity = ndb.StringProperty(required=False)
    
class Profile(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    phone_number = ndb.StringProperty(required=False)