# course.py
# Sources: Lecture code - CS496

from google.appengine.ext import ndb
import webapp2
import db_models
import json

class Course(webapp2.RequestHandler):
	def post(self):		
		# create new course with vars
		new_course = db_models.Course()
		name = self.request.get('name', default_value=None)
		days = self.request.get('days', default_value=None)
		time = self.request.get('time', default_value=None)
		quarter = self.request.get('quarter', default_value=None)
		dateWindow = self.request.get('dateWindow', default_value=None)

		# if required fields not entered append to errors
		if name:
			new_course.name = name
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"
		if days:	
			new_course.days = days
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"	
		if time:		
			new_course.time = time
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"
		if dateWindow:		
			new_course.dateWindow = dateWindow
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"
		if quarter:		
			new_course.quarter = quarter
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"

		# add record to datastore
		key = new_course.put()
		out = new_course.to_dict()
		self.response.write(out)
		return

	def get(self, **kwargs):
		q = db_models.Course.query()
		results = [{'name':x.name, 'days':x.days, 'dateWindow':x.dateWindow, 'time':x.time, 'quarter':x.quarter} for x in q.fetch()]
		self.response.write(json.dumps(results))