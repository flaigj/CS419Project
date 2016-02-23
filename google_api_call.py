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
		increase = 0
		recurringEvent = list()
		for idxEvent, eleEvent in enumerate(responseJson['items']):	#for each event
			if(eleEvent['status'] == 'confirmed' and	#ignore cancelled appointments
			'dateTime' in responseJson['items'][idxEvent]['start']):	#ignore all day events
				
				eventStartRfcTimestamp = responseJson['items'][idxEvent]['start']['dateTime']
				eventEndRfcTimestamp = responseJson['items'][idxEvent]['end']['dateTime']
				eventSummary = responseJson['items'][idxEvent]['summary']
				#print eventStartRfcTimestamp, eventSummary
		
				#Convert RFC timestamp to Google timestamp format
				eventStartGoogleTimestamp = func.rfcToGoogleTimestamp(eventStartRfcTimestamp)
				eventEndGoogleTimestamp = func.rfcToGoogleTimestamp(eventEndRfcTimestamp)

				#Duration of Even
				startTimePosix = func.timeStrToPosix(eventStartGoogleTimestamp)
				endTimePosix = func.timeStrToPosix(eventEndGoogleTimestamp)
				durationSeconds = endTimePosix - startTimePosix
				#print 'durationSeconds = ', durationSeconds,eventStartGoogleTimestamp, eventSummary

				#If googleTS is < timeWindow start, it's a recurring event. Change event date
				eventStartPosixTimestamp = func.timeStrToPosix(eventStartGoogleTimestamp)
				timeWindowStartPosix = func.timeStrToPosix(timeWindow[0])
				timeWindowEndPosix = func.timeStrToPosix(timeWindow[1])
				if(eventStartPosixTimestamp < timeWindowStartPosix):
					#eventStartGoogleTimestamp = timeWindow[0]	#timeWindow already as Google TS

					#Add recurring event to each day of the time window
					timeWindowDays = func.numOfTimeWindowDays(timeWindowStartPosix, timeWindowEndPosix)
					for i in range(0, timeWindowDays + 1): #days to add 
						if (i == 0):
							event = func.changeEventDate(timeWindow[0], eventStartGoogleTimestamp)
							recurringEvent.append(event)
						else:
							eventPosix = func.timeStrToPosix(event)
							eventPosix += 86400	#add one day in seconds
							event = posixToTimeStr(eventPosix)		
							recurringEvent.append(event)
						print i, event

				if durationSeconds == 1800:	#duraction is 30 minutes
					#print '\n30 mins\n', eventStartGoogleTimestamp, '\n' 
					slotsBusy.append(eventStartGoogleTimestamp)	
				else:
					slotCount = int(durationSeconds / 1800)	#number of 30 minute slots
					slotsBusy.append(eventStartGoogleTimestamp)	#1st entry in proper form
					for i in range(1, slotCount):
						#print '\n60 mins'
						#print eventStartGoogleTimestamp, 'google TS before' 
						posixTime = func.timeStrToPosix(eventStartGoogleTimestamp)	#Google TS to Posix
						increase = increase + 1800
						#print 'increase = ', increase
						posixTime = posixTime + increase	#increment by 30 minutes
						eventStartGoogleTimestamp = func.posixToTimeStr(posixTime)
						#print eventStartGoogleTimestamp, 'google TS after' 
						slotsBusy.append(eventStartGoogleTimestamp)	
						#print 'posixToPST = ', eventStartGoogleTimestamp
							



		participants.append( Participants(emailList[idxEmail], slotsBusy) )

	#for idx, ele in enumerate(recurringEvent):
	#	print ele


	#for idx, ele in enumerate(participants):
	#	print ele.getOpenTimeSlot()
	exit(0)
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
