import webapp2

app = webapp2.WSGIApplication([
	('/', 'base_page.BaseHandler'),
	('/input', 'base_page.ActorInput'),	
	('/google-api', 'google_api_call.FrankTest'),		
	], debug=True)