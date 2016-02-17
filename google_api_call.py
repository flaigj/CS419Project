#Obtain available time slots from Google Calendars based on specified time window
import urllib2
import json
import re
import user_interface as ui

#Save each participant's Google Calendar data in an array of type Participants
class Participants:
    def __init__(self, name, openTimeSlot):
        self.name = name
        self.openTimeSlot = openTimeSlot

    def getOpenTimeSlot(self):
        return self.openTimeSlot

    def getName(self):
        return self.name

def getParticipantData():
	#Google API Call code goes here

	participants = list()
	#participants = ui.getName()
	#emailInput = "leima@oregonstate.edu groupnineemail@gmail.com" #will take in from user input (only works with valid PUBLIC calendars)
	emailInput = ui.getEmailAddr()
	dateInput = "2016-01-28" #will take in from user input
	earliestTime = dateInput + "T00:00:00-08:00"  # -08:00 is PST; -07:00 is PDT (might encounter PDT if user picks a far off date)
	latestTime = dateInput + "T23:59:00-08:00"

	emailList = emailInput.split() #create email list delimited by space character
	#print(emailList)

	#splits the date the user inputted into an array
	dateInputSplit = re.split('[-]', dateInput)

	#convert numerical month to three-letter text
	if "01" in dateInputSplit[1]:
		month = "Jan"
	elif "02" in dateInputSplit[1]:
		month = "Feb"
	elif "03" in dateInputSplit[1]:
		month = "Mar"
	elif "04" in dateInputSplit[1]:
		month = "Apr"
	elif "05" in dateInputSplit[1]:
		month = "May"
	elif "06" in dateInputSplit[1]:
		month = "Jun"
	elif "07" in dateInputSplit[1]:
		month = "Jul"
	elif "08" in dateInputSplit[1]:
		month = "Aug"
	elif "09" in dateInputSplit[1]:
		month = "Sep"
	elif "10" in dateInputSplit[1]:
		month = "Oct"
	elif "11" in dateInputSplit[1]:
		month = "Nov"
	elif "12" in dateInputSplit[1]:
		month = "Dec"

	dateModified = month + " " + dateInputSplit[2] + " " + dateInputSplit[0]
	#print dateModified

	#for each email address
	for index, elem in enumerate(emailList):
		# API call to Google Calendars API; timeMin is set to 00:00 and timeMax is set to 23:59, so we're going to get all events of that day
		response = urllib2.urlopen("https://www.googleapis.com/calendar/v3/calendars/"+emailList[index]+"/events?timeMin="+earliestTime+"&timeMax="+latestTime+"&key=AIzaSyB7IsERaXNIMiRgMAB_tujhdzNVmxpq0KA").read()
		responseJson = json.loads(response) #converts to JSON object

		#print(response) # use this to see structure of JSON


		#start with all time slots
		allOpenSlots = ['00:00:00', '00:30:00','01:00:00', '01:30:00', '02:00:00', '02:30:00',
						'03:00:00', '03:30:00','04:00:00', '04:30:00', '05:00:00', '05:30:00',
						'06:00:00', '06:30:00','07:00:00', '07:30:00', '08:00:00', '08:30:00',
						'09:00:00', '09:30:00','10:00:00', '10:30:00', '11:00:00', '11:30:00',
						'12:00:00', '12:30:00','13:00:00', '13:30:00', '14:00:00', '14:30:00',
						'15:00:00', '15:30:00','16:00:00', '16:30:00', '17:00:00', '17:30:00',
						'18:00:00', '18:30:00','19:00:00', '19:30:00', '20:00:00', '20:30:00',
						'21:00:00', '21:30:00','22:00:00', '22:30:00', '23:00:00', '23:30:00']

		
		#traverse through the items to find the start dates of each event and then remove them from allOpenSlots array
		for idx, item in enumerate(responseJson['items']):
			startDateTime = responseJson['items'][idx]['start']
			if 'dateTime' in startDateTime: #gets the start time of the first event returned
				takenDateTime = startDateTime['dateTime']
				#print(takenDateTime)

			### what to do if all day event with no time? has 'date' as name (key) instead of 'dateTime'


				#discards the date, leaves time of event
				if "T" in takenDateTime:
				    param, takenTimeSlots = takenDateTime.split("T", 1)

				#discards the time offset (e.g. -8:00)
				if "-" in takenDateTime:
				    takenTimeSlotsTrimmed, paramdiscard = takenTimeSlots.split("-", 1)

				    #print ("takenTimeSlotsTrimmed", takenTimeSlotsTrimmed)

				takenTimeParts = re.split('[-:]', takenTimeSlotsTrimmed)
				#print("takenTimeParts", takenTimeParts)

				#turn start time string into integer (8:30 will be 850)
				takenStartTimeInt = int(takenTimeParts[0]) * 100
				takenStartTimeInt += int(takenTimeParts[1]) * 50 / 30

				#print(takenStartTimeInt)

			endDateTime = responseJson['items'][idx]['end']
			if 'dateTime' in endDateTime: #gets the end time of the first event returned
				takenEndDateTime = endDateTime['dateTime']
				#print(takenEndDateTime)

				if "T" in takenEndDateTime:
					param, takenEndTime = takenEndDateTime.split("T",1)

				takenEndTimeParts = re.split('[-:]', takenEndTime)
				#print(takenEndTimeParts)

				#turns end time string into integer (8:30 will be 850)
				takenEndTimeInt = int(takenEndTimeParts[0]) * 100
				takenEndTimeInt += int(takenEndTimeParts[1]) * 50 / 30
				#print(takenEndTimeInt)

				#checks to see if the event lasted for more than a half an hour.
				#if so, we need to remove those times from allOpenSlots array
				eventSpan = takenEndTimeInt - takenStartTimeInt
				if eventSpan > 50: #if the span is greater than a half hour
					halfHourIncrements = (eventSpan/50) - 1

					#loop that adds taken half hour slots to takenIncrementsStr
					for i in range(halfHourIncrements):
						takenStartTimeInt += 50
						takenIncrementsStr = ""

						# if it is a XX:00 (e.g. turn 800 to 8:00)
						if (takenStartTimeInt % 100) == 0:
							if takenStartTimeInt < 1000:
								takenIncrementsStr += "0" + (str(takenStartTimeInt/100))
							else:
								takenIncrementsStr += (str(takenStartTimeInt/100))
							takenIncrementsStr += (":00")

						# if it is a XX:30 (e.g. turn 850 to 8:30)
						if (takenStartTimeInt % 100) != 0:
							takenStartTimeInt -= 50
							if takenStartTimeInt < 1000:
								takenIncrementsStr += "0" + (str(takenStartTimeInt/100))
							else:
								takenIncrementsStr += (str(takenStartTimeInt/100))
							takenIncrementsStr += (":30")

						#print("takenIncrements"+takenIncrementsStr)

						#convert to string (needs to match the format of the allOpenSlots)
						takenTimeSlotsTrimmed += " " + takenIncrementsStr + ":00"
						#print("taken time slots trimmed"+takenTimeSlotsTrimmed)

						#split into array of times
						occupiedTimeSlotList = takenTimeSlotsTrimmed.split()
						#print occupiedTimeSlotList


			#if the time of the user's event is present, remove the slot
			for j, elem in enumerate(occupiedTimeSlotList):
				if occupiedTimeSlotList[j] in allOpenSlots:  ###########remove the array of times in takenTimeSlots
					allOpenSlots.remove(occupiedTimeSlotList[j])

		#print(allOpenSlots)

		#always uses "Mon"
		for k, elem in enumerate(allOpenSlots):
			allOpenSlots[k] = "Mon " + dateModified + " " +allOpenSlots[k] + " GMT-0800 (PST)"


		participants.append( Participants(emailList[index], allOpenSlots) )


	return participants



def getTimeWindowData():
	#Time window -- Actor's input when making the Google API Call
	#Signature: timeWindow = [startTime, endTime]
	print "Enter a time window in the following format: Jan 28 2016 15:30"
	timeType = ["start", "finish"]
	timeWindow = list()
	for x in range(0, 2):
		ipt = raw_input("Enter a " + timeType[x] + " window")
		timeWindow.append("Mon " + ipt + ":00 GMT-0800 (PST)")

	#timeWindow = ["Tue Jan 28 2016 10:30:00 GMT-0800 (PST)",    #dummy data
	#                "Tue Jan 28 2016 15:00:00 GMT-0800 (PST)"]
	
	#Test names return successfully
	#for index, elem in enumerate(participants):
	#	participants[index].getOpenTimeSlot()

	return timeWindow
