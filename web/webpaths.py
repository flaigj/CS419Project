import webapp2

app = webapp2.WSGIApplication([
	('/', 'base_page.BaseHandler'),
	('/time', 'google_api_call.TimeHandler'),
	], debug=True)