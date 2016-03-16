import webapp2

app = webapp2.WSGIApplication([
	('/', 'base_page.BaseHandler'),
	('/input', 'base_page.ActorInput'),	
	('/google-api', 'use_cases.RunUseCases'),
	('/catalog_input', 'base_page.CourseInput'),
	('/catalog-api', 'osu_catalog.GetCourse'),
	], debug=True)