import urllib
import urllib2
import json
import re
import sys 
import user_interface as ui

def getTermNumber():
	option = ui.getNumber(1, 4)
	termNum = ""
	if option == 1:
		termNum = "201602"
	elif option == 2:
		termNum = "201603"
	elif option == 3:
		termNum = "201700"
	if option == 4:
		termNum = "201701"
	return termNum

def runCatalog():
	print "Welcome to the course look up section"
	print "Quarters should be entered in as 1-4 for WI,SP,SU,AU\n"

	print "What quarter do you want to look up classes for?"
	termNum = getTermNumber()

	subjectCode = raw_input("Enter a subject Code: ")
	courseNum = raw_input("Enter a Course Number: ")


	response = urllib2.urlopen("http://apicatalog-1252.appspot.com/course/").read()
	#response = urllib2.urlopen("http://localhost:8080/course/").read()
	jsonResp = json.loads(response)
	jsonRespStr = str(jsonResp)


	course = subjectCode + courseNum
	# special case database is empty
	inDb = None
	#print jsonRespStr
	if jsonRespStr == "[]":
		print "datastore is empty"

	idx = 0
	# check to see if in database
	for c in jsonResp:
		if c['name'] == course:
			if c['quarter'] == termNum:
				inDb = True
				print c['name'] + " " + c['days'] + " " + c['time'] + " " + c['dateWindow']

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

		print course + " " + days + " "  + date + " " + time

		url = "http://apicatalog-1252.appspot.com/course/"
		# url = "http://localhost:8080/course/"
		data = urllib.urlencode({'name' : subjectCode+courseNum,
		                         'days'  : days,
		                         'time'  : time,
		                         'quarter'  : termNum,
		                         'dateWindow'  : date})

		content = urllib2.urlopen(url=url, data=data).read()
		#print content