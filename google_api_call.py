#Obtain available time slots from Google Calendars based on specified time window
import urllib2
import json
import re
import user_interface as ui
import functions as func

#Save each participant's Google Calendar data in an array of type Participants
class Participant:
    def __init__(self, email, eventSummary, startTime, endTime):
        self.email = email
        self.eventSummary = eventSummary
        self.startTime = startTime
        self.endTime = endTime

    def getEmail(self):
        return self.email

    def getEventSummary(self):
        return self.eventSummary

    def getStartTime(self):
        return self.startTime

    def getEndTime(self):
        return self.endTime


def getParticipantData(timeWindow):
	participants = list()
	emailInput = ui.getEmailAddr()
	emailList = emailInput.split() #create email list delimited by space character
	startTimestamp = func.createRfcTimestamp(timeWindow[0])
	endTimestamp = func.createRfcTimestamp(timeWindow[1])

	#Get Google API data
	for idxEmail, eleEmail in enumerate(emailList):  #for each email address (Participant)
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
				email = responseJson['items'][idxEvent]['organizer']['email']
				#print eventStartRfcTimestamp, eventSummary
		
				#Convert RFC timestamp to Google timestamp format
				eventStartGoogleTimestamp = func.rfcToGoogleTimestamp(eventStartRfcTimestamp)
				eventEndGoogleTimestamp = func.rfcToGoogleTimestamp(eventEndRfcTimestamp)

				#Determine if event is recurring
				#If googleTS is < timeWindow start, it's a recurring event. Change event date
				eventStartPosixTimestamp = func.timeStrToPosix(eventStartGoogleTimestamp)
				eventEndPosixTimestamp = func.timeStrToPosix(eventEndGoogleTimestamp)
				timeWindowStartPosix = func.timeStrToPosix(timeWindow[0])
				timeWindowEndPosix = func.timeStrToPosix(timeWindow[1])
				if(eventStartPosixTimestamp < timeWindowStartPosix):
					additionalSlots = list()	#if event duration > 30 mins

					#Add recurring event to each day of the time window
					timeWindowDays = func.numOfTimeWindowDays(timeWindowStartPosix, timeWindowEndPosix)
					for i in range(0, timeWindowDays + 1): #days to add 
						if (i == 0):
							eventStart = func.changeEventDate(timeWindow[0], eventStartGoogleTimestamp)
							eventEnd = func.changeEventDate(timeWindow[0], eventEndGoogleTimestamp)
							participants.append(Participant(email, eventSummary,
							eventStart, eventEnd))
						else:
							eventPosix = func.timeStrToPosix(eventStart)
							eventPosix += 86400	#add one day in seconds
							eventStart = func.posixToTimeStr(eventPosix)		
							eventEnd = func.changeEventDate(eventStart, eventEndGoogleTimestamp)

							participants.append(Participant(email, eventSummary,
							eventStart, eventEnd))
						#print i, eventStart, eventSummary

				else:	#event is not recurring
					participants.append(Participant(email, eventSummary,
					eventStartGoogleTimestamp, eventEndGoogleTimestamp))
						

						##If event duration > 30 mins, add additional 30 min slots
						#startTimePosix = func.timeStrToPosix(eventStartGoogleTimestamp)
						#endTimePosix = func.timeStrToPosix(eventEndGoogleTimestamp)
						#durationSeconds = endTimePosix - startTimePosix

						#if durationSeconds == 1800:	#duraction is 30 minutes
						#	#print '\n30 mins\n', eventStartGoogleTimestamp, '\n' 
						#	additionalSlots.append(eventStartGoogleTimestamp)	
						#else:
						#	slotCount = int(durationSeconds / 1800)	#number of 30 minute slots
						#	additionalSlots.append(eventStartGoogleTimestamp)	#1st entry in proper form
						#	for i in range(1, slotCount):
						#		#print '\n60 mins'
						#		#print eventStartGoogleTimestamp, 'google TS before' 
						#		posixTime = func.timeStrToPosix(eventStartGoogleTimestamp)	#Google TS to Posix
						#		increase = increase + 1800
						#		#print 'increase = ', increase
						#		posixTime = posixTime + increase	#increment by 30 minutes
						#		eventStartGoogleTimestamp = func.posixToTimeStr(posixTime)
						#		#print eventStartGoogleTimestamp, 'google TS after' 
						#		additionalSlots.append(eventStartGoogleTimestamp)	
						#		#print 'posixToPST = ', eventStartGoogleTimestamp
							

		print '\n=============================='
		for idx, ele in enumerate(participants):
			print ele.getStartTime(), ele.getEventSummary()



		#participants.append( Participants(emailList[idxEmail], additionalSlots) )

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
