#Obtain available time slots from Google Calendars based on specified time window
import urllib2
import json
import re
import user_interface as ui
import functions as func

#Save each participant's Google Calendar data in an array of type Participants
class Participants:
    def __init__(self, name, openTimeSlot):
        self.name = name
        self.openTimeSlot = openTimeSlot

    def getOpenTimeSlot(self):
        return self.openTimeSlot

    def getName(self):
        return self.name


def getParticipantData(timeWindow):
	participants = list()
	emailInput = ui.getEmailAddr()
	emailList = emailInput.split() #create email list delimited by space character
	startTimestamp = func.createRfcTimestamp(timeWindow[0])
	endTimestamp = func.createRfcTimestamp(timeWindow[1])

	#Make Google API call
	for idxEmail, eleEmail in enumerate(emailList):  #for each email address (Participant)
		slotsBusy = list()
		try:
			response = urllib2.urlopen("https://www.googleapis.com/calendar/v3/calendars/"+emailList[idxEmail]+"/events?timeMin="+startTimestamp+"&timeMax="+endTimestamp+"&key=AIzaSyB7IsERaXNIMiRgMAB_tujhdzNVmxpq0KA").read()
		except urllib2.HTTPError, e:
			print "\nERROR: We could not retrieve the calendar for", emailList[idxEmail]
			print "Please make sure the email address is valid and the calendar is public\n"
			exit(1)	

		responseJson = json.loads(response) #converts to JSON object
		#startTime = responseJson['items'][0]['start']

		#Find Participant's scheduled meetings during timeWindow
		#print responseJson['items'][0]['start']['dateTime']
		#print responseJson['items']
		for idxEvent, eleEvent in enumerate(responseJson['items']):	#for each event
			if(eleEvent['status'] == 'confirmed' and	#ignore cancelled appointments
			'dateTime' in responseJson['items'][idxEvent]['start']):	#ignore all day events
				
				eventRfcTimestamp = responseJson['items'][idxEvent]['start']['dateTime']
				eventSummary = responseJson['items'][idxEvent]['summary']
				#print eventRfcTimestamp, eventSummary
		
				#Convert RFC timestamp to Google timestamp format
				eventGoogleTimestamp = func.rfcToGoogleTimestamp(eventRfcTimestamp)
				#print eventGoogleTimestamp, eventSummary
			
				slotsBusy.append(eventGoogleTimestamp)	
		participants.append( Participants(emailList[idxEmail], slotsBusy) )

	#for idx, ele in enumerate(participants):
	#	print ele.getOpenTimeSlot()
	return participants



def getTimeWindowData():
	#Time window -- Actor's input when making the Google API Call
	#Signature: timeWindow = [startTime, endTime]
	print "Enter a time window in the following format: Jan 28 2016 15:30"
	timeType = ["start", "finish"]
	timeWindow = list()
	for x in range(0, 2):
		ipt = raw_input("Enter a " + timeType[x] + " window: ")
		timeWindow.append("Mon " + ipt + ":00 GMT-0800 (PST)")

	#timeWindow = ["Tue Jan 28 2016 10:30:00 GMT-0800 (PST)",    #dummy data
	#                "Tue Jan 28 2016 15:00:00 GMT-0800 (PST)"]
	
	#Test names return successfully
	#for index, elem in enumerate(participants):
	#	participants[index].getOpenTimeSlot()

	return timeWindow
