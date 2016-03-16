import webapp2
import os
import jinja2
import cgi

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class BaseHandler(webapp2.RequestHandler):
	template_variables = {}
	
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('menu.html')
		self.response.write(template.render())

class ActorInput(webapp2.RequestHandler):
	def post(self):	
		template_values = {
			'useCase' : cgi.escape(self.request.get('choose'))
		}

		template = JINJA_ENVIRONMENT.get_template('actor-input.html')
		self.response.write(template.render(template_values))

class CourseInput(webapp2.RequestHandler):
	def post(self):	
		template = JINJA_ENVIRONMENT.get_template('osu_catalog_input.html')
		self.response.write(template.render())