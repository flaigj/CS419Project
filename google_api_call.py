#Obtain available time slots from Google Calendars based on specified time window


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
	#======================= DUMMY DATA ===============================================	
	#Dummy data for testing purposes. This data should be obtained through the google API call
	name_1 = "Frank"
	openTimeSlot_1 = ["Tue Jan 26 2016 08:00:00 GMT-0800 (PST)", 
						"Tue Jan 26 2016 10:00:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 12:00:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 14:00:00 GMT-0800 (PST)"]
	
	name_2 = "Jason"
	openTimeSlot_2 = ["Tue Jan 26 2016 07:00:00 GMT-0800 (PST)", 
						"Tue Jan 26 2016 09:00:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 12:00:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 15:00:00 GMT-0800 (PST)"]
	
	name_3 = "Superman"		#Superman is available during timeWindow for use case 2 testing
	openTimeSlot_3 = ["Tue Jan 26 2016 10:30:00 GMT-0800 (PST)", 
						"Tue Jan 26 2016 11:00:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 11:30:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 12:00:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 12:30:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 13:00:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 13:30:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 14:00:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 14:30:00 GMT-0800 (PST)",
						"Tue Jan 26 2016 15:00:00 GMT-0800 (PST)"]

	#Please return an array of type Participants class
	participants = list()
	participants.append( Participants(name_1, openTimeSlot_1) )
	participants.append( Participants(name_2, openTimeSlot_2) )
	participants.append( Participants(name_3, openTimeSlot_3) )
	#======================= DUMMY DATA ===============================================	

	return participants



def getTimeWindowData():
	#Time window -- Actor's input when making the Google API Call
	#Signature: timeWindow = [startTime, endTime]
	
	timeWindow = ["Tue Jan 26 2016 10:30:00 GMT-0800 (PST)",    #dummy data
	                "Tue Jan 26 2016 15:00:00 GMT-0800 (PST)"]
	
	#Test names return successfully
	#for index, elem in enumerate(participants):
	#	participants[index].getOpenTimeSlot()

	return timeWindow
