import webapp2

app = webapp2.WSGIApplication([
	('/', 'base_page.BaseHandler'),
	('/input', 'base_page.ActorInput'),	
	('/google-api', 'use_cases.RunUseCases'),
	], debug=True)