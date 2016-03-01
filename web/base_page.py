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





	# def post(self):
	# 	self.template_variables['choosenNum'] = {}
	# 	template = JINJA_ENVIRONMENT.get_template('menu.html')
	# 	# for i in self.request.arguments():
	# 	# 	self.template_variables['form_content'][i] = self.request.get(i)
	# 	# self.response.write(template.render(self.template_variables))
	# 	import use_cases as uc					#Use cases functions
	# 	action = self.request.get('action')
		
	# 	if action == 'choose_type':
	# 		if self.request.get('choose') == '1':
	# 			useCaseOne = uc.useCaseOne()		# One on one meeting
	# 			#self.template_variables['choosenNum'] = "You chose 1"
			
	# 		elif self.request.get('choose') == '2':
	# 			useCaseTwo = uc.useCaseTwo()		# Who can attend whole meeting
	# 			#self.template_variables['choosenNum'] = "You chose 2"
	# 		else:
	# 			useCaseThree = uc.useCaseThree()	# Multiple person meeting
	# 			#self.template_variables['choosenNum'] = "You chose 3"
	# 		#self.response.write(template.render(self.template_variables))