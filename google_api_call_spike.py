import urllib2
import json
import re


#Save each participant's Google Calendar data in an array of type Participants
class Participants:
    def __init__(self, name, openTimeSlot):
        self.name = name
        self.openTimeSlot = openTimeSlot

    def getOpenTimeSlot(self):
        print self.openTimeSlot

    def getName(self):
        print self.name

participants = list()


emailInput = "leima@oregonstate.edu groupnineemail@gmail.com" #will take in from user input (only works with valid PUBLIC calendars)
dateInput = "2016-01-28" #will take in from user input
earliestTime = dateInput + "T00:00:00-08:00"  # -08:00 is PST; -07:00 is PDT (might encounter PDT if user picks a far off date)
latestTime = dateInput + "T23:59:00-08:00"

emailList = emailInput.split() #create email list delimited by space character
#print(emailList)

#for each email address
for index, elem in enumerate(emailList):
	# API call to Google Calndars API; timeMin sets the time for the earliest event you want returned
	response = urllib2.urlopen("https://www.googleapis.com/calendar/v3/calendars/"+emailList[index]+"/events?timeMin="+earliestTime+"&timeMax="+latestTime+"&key=AIzaSyB7IsERaXNIMiRgMAB_tujhdzNVmxpq0KA").read()
	responseJson = json.loads(response) #converts to JSON object

	#print(response) # use this to see structure of JSON


	#start with all time slots
	allOpenSlots = ['00:00:00-08:00', '00:30:00-08:00','01:00:00-08:00', '01:30:00-08:00', '02:00:00-08:00', '02:30:00-08:00',
			'03:00:00-08:00', '03:30:00-08:00','04:00:00-08:00', '04:30:00-08:00', '05:00:00-08:00', '05:30:00-08:00',
			'06:00:00-08:00', '06:30:00-08:00','07:00:00-08:00', '07:30:00-08:00', '08:00:00-08:00', '08:30:00-08:00',
			'09:00:00-08:00', '09:30:00-08:00','10:00:00-08:00', '10:30:00-08:00', '11:00:00-08:00', '11:30:00-08:00',
			'12:00:00-08:00', '12:30:00-08:00','13:00:00-08:00', '13:30:00-08:00', '14:00:00-08:00', '14:30:00-08:00',
			'15:00:00-08:00', '15:30:00-08:00','16:00:00-08:00', '16:30:00-08:00', '17:00:00-08:00', '17:30:00-08:00',
			'18:00:00-08:00', '18:30:00-08:00','19:00:00-08:00', '19:30:00-08:00', '20:00:00-08:00', '20:30:00-08:00',
			'21:00:00-08:00', '21:30:00-08:00','22:00:00-08:00', '22:30:00-08:00', '23:00:00-08:00', '23:30:00-08:00']

	
	#traverse through the items to find the start dats of each event and remove them from allOpenSlots array
	for idx, item in enumerate(responseJson['items']):
		startDateTime = responseJson['items'][idx]['start']
		if 'dateTime' in startDateTime: #gets the start time of the first event returned
			takenDateTime = startDateTime['dateTime']
			#print(takenDateTime)

		### what to do if all day event with no time? has 'date' as name (key) instead of 'dateTime'


			#discards the date, leaves time of event
			if "T" in takenDateTime:
			    param, takenTimeSlots = takenDateTime.split("T", 1)

			takenTimeParts = re.split('[-:]', takenTimeSlots)
			#print(takenTimeParts)

			#turn start time string into integer
			takenStartTimeInt = int(takenTimeParts[0]) * 100
			takenStartTimeInt += int(takenTimeParts[1]) * 50 / 30

			#print(takenStartTimeInt)

		endDateTime = responseJson['items'][idx]['end']
		if 'dateTime' in endDateTime: #gets the start time of the first event returned
			takenEndDateTime = endDateTime['dateTime']
			#print(takenEndDateTime)

			if "T" in takenEndDateTime:
				param, takenEndTime = takenEndDateTime.split("T",1)

			takenEndTimeParts = re.split('[-:]', takenEndTime)
			#print(takenEndTimeParts)

			#turns end time string into integer
			takenEndTimeInt = int(takenEndTimeParts[0]) * 100
			takenEndTimeInt += int(takenEndTimeParts[1]) * 50 / 30
			#print(takenEndTimeInt)

			#checks to see if the event lasted for more than a half an hour.
			#if so, we need to remove those times from allOpenSlots array
			eventSpan = takenEndTimeInt - takenStartTimeInt
			if eventSpan > 50: #if the span is greater than a half hour
				increments = (eventSpan/50) - 1
				for i in range(increments):
					takenStartTimeInt += 50
					takenIncrementsStr = ""

					# if it is a XX:00
					if (takenStartTimeInt % 100) == 0:
						if takenStartTimeInt < 1000:
							takenIncrementsStr += "0" + (str(takenStartTimeInt/100))
						else:
							takenIncrementsStr += (str(takenStartTimeInt/100))
						takenIncrementsStr += (":00")

					# if it is a XX:30
					if (takenStartTimeInt % 100) != 0:
						takenStartTimeInt -= 50
						if takenStartTimeInt < 1000:
							takenIncrementsStr += "0" + (str(takenStartTimeInt/100))
						else:
							takenIncrementsStr += (str(takenStartTimeInt/100))
						takenIncrementsStr += (":30")

					#print("takenIncrements"+takenIncrementsStr)

					#convert to string (needs to match the format of the allOpenSlots)
					takenTimeSlots += " " + takenIncrementsStr + ":00-08:00"
					#print("taken time slots"+takenTimeSlots)

					#split into array of times
					occupiedTimeSlotList = takenTimeSlots.split()
					print occupiedTimeSlotList


		#if the time of the user's event is present, remove the slot
		for j, elem in enumerate(occupiedTimeSlotList):
			if occupiedTimeSlotList[j] in allOpenSlots:  ###########remove the array of times in takenTimeSlots
				allOpenSlots.remove(occupiedTimeSlotList[j])

	#print(allOpenSlots)
	#for k, elem in enumerate(allOpenSlots):
	#	allOpenSlots[k] = "Mon "


	participants.append( Participants(emailList[index], allOpenSlots) )



#Test names return successfully
for index, elem in enumerate(participants):
	participants[index].getName()
	participants[index].getOpenTimeSlot()