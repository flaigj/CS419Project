# main.py
# Sources: Lecture code - CS496

import webapp2
from google.appengine.api import oauth

app = webapp2.WSGIApplication([
	('/course', 'course.Course'),
	], debug=True)

app.router.add(webapp2.Route(r'/course/', 'course.Course'))