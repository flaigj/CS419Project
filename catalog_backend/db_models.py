# db_models.py
# Sources: Lecture code - CS496

from google.appengine.ext import ndb
import datetime
from time import mktime
import json

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class Course(Model):
	name = ndb.StringProperty(required=True)
	days = ndb.StringProperty(required=True)
	time = ndb.StringProperty(required=True)
	quarter = ndb.StringProperty(required=True)
	dateWindow = ndb.StringProperty(required=True)

	def to_dict(self):
		d = super(Course, self).to_dict()
		d['key'] = self.key.id()
		return d