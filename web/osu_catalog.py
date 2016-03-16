import urllib
import urllib2
import json
import re
import sys 
import os
import jinja2
import webapp2
import cgi
#import user_interface as ui

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class GetCourse(webapp2.RequestHandler):
	def post(self):
		# def getTermNumber():
			# option = ui.getNumber(1, 4)
			# termNum = ""
			# if option == 1:
			# 	termNum = "201602"
			# elif option == 2:
			# 	termNum = "201603"
			# elif option == 3:
			# 	termNum = "201700"
			# if option == 4:
			# 	termNum = "201701"
			# return termNum

			# print "Welcome to the course look up section"
			# print "Quarters should be entered in as 1-4 for WI,SP,SU,AU\n"

			# print "What quarter do you want to look up classes for?"
			# termNum = getTermNumber()

			# subjectCode = raw_input("Enter a subject Code: ")
			# courseNum = raw_input("Enter a Course Number: ")

			# get post variables
			# chooseQTR, courseCode, courseNum as post vars
		termNum = self.request.get('chooseQTR')
		subjectCode = self.request.get('courseCode')
		courseNum = self.request.get('courseNum')

		response = urllib2.urlopen("http://apicatalog-1252.appspot.com/course/").read()
		#response = urllib2.urlopen("http://localhost:8080/course/").read()
		jsonResp = json.loads(response)
		jsonRespStr = str(jsonResp)


		course = subjectCode + courseNum
		# special case database is empty
		inDb = None
		#print jsonRespStr
		# if jsonRespStr == "[]":
		# 	print "datastore is empty"

		idx = 0
		output = ""
		# check to see if in database
		for c in jsonResp:
			if c['name'] == course:
				if c['quarter'] == termNum:
					inDb = True
					output = c['name'] + " " + c['days'] + " " + c['time'] + " " + c['dateWindow']


		# not in database so call api
		if not inDb:
			#course not in database
			responseOsu = urllib2.urlopen("http://catalog.oregonstate.edu/Services/CatalogService.svc/rest/course/" + subjectCode + "/" + courseNum + "/" + termNum + "?campus=" +  "corvallis").read()
			jsonRespOsu = json.loads(responseOsu)
			courseOsu = jsonRespOsu['Offerings'][0]

			meetingTime = courseOsu['MeetingTimes'][0]
			timeSummary = meetingTime['TimeSummarySingleLine']
			days = meetingTime['DaysOfTheWeek']
			time = timeSummary.split("&nbsp;")[0]
			date = timeSummary.split("&nbsp;")[1]

			output = course + " " + days + " "  + date + " " + time

			url = "http://apicatalog-1252.appspot.com/course/"
			# url = "http://localhost:8080/course/"
			data = urllib.urlencode({'name' : subjectCode+courseNum,
			                         'days'  : days,
			                         'time'  : time,
			                         'quarter'  : termNum,
			                         'dateWindow'  : date})

			content = urllib2.urlopen(url=url, data=data).read()
			#print content

		# send output(catalog class); dbContent or json output 
		template_values = {'course':output}

		template = JINJA_ENVIRONMENT.get_template('catalog_class.html')
		self.response.write(template.render(template_values))