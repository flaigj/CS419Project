#Use cases functions

#Import Modules
import find_open_slots as fos       #Available meeting time among all participants
import functions as func			#Helper functions


#All participants and their availability during timeWindow: object MeetingMatrix
meetingAvailability = fos.createMeetingMatrix()

#Meeting matrix: 2d binary array
meetingMatrix = meetingAvailability.getMeetingMatrix()

#Participants in meeting matrix: array of Participant object
participants = meetingAvailability.getParticipants()

#Number of participants
numOfParticipants = len(participants)

#Number of 30 minute slots during timeWindow
numOfWindowSlots = meetingAvailability.getNumOfWindowSlots()

#Time window slots in PST
timeWindowSlots = meetingAvailability.getTimeWindowSlots()

#Print matrix by participant
#print '\nMeeting Matrix'
#for index, elem in enumerate(participants):
#		print meetingMatrix[index], elem.getEmail()
#print '\n'



#===================================================================================
#useCaseThree
#===================================================================================
#Given a more broad window and a list of usernames, provide all time periods where all are available.
#This is more in the nature of .when can I schedule the meeting?
#Postcondition: display times when all participants are available durind timeWindow
def useCaseThree(): 
	availableMeetingSlots = list()
	for i in range(0, numOfWindowSlots):			#each time slot
		for j in range(0, numOfParticipants):		#each participant
			if(meetingMatrix[j][i] == 1):			#if participant is not available in this slot
				break								#go to next time slot	
			if(j == numOfParticipants - 1):			#if at last participant, make slot available
				availableMeetingSlots.append(i)

	#Display times when all participants are available during timeWindow
	print 'Use Case Three - given a more broad window and a list of usernames, provide all times when all participant\'s are available during for at least 30 minutes'
	print '\nAll participant\'s are available during the following times for 30 minutes:'
	for i in availableMeetingSlots:
		slot = func.posixToPST(timeWindowSlots[i])
		print slot
	print '\n'



#===================================================================================
#useCaseTwo
#===================================================================================
#Given a specific time window and a list of usernames, list all users available for the entire duration.
#This is more in the nature of who can I expect at the meeting?
def useCaseTwo(): 
	availableParticipants = list()
	for i in range(0, numOfParticipants):		#each participant
		for j in range(0, numOfWindowSlots):	#each time slot
			if(meetingMatrix[i][j] == 1):		#if participant is not available in this slot
				break							#go to next participant
			if(j == numOfWindowSlots - 1):			#if at last participant, make slot available
				availableParticipants.append(i)

	#Display times when participants are available during the entire timeWindow
	print 'Use Case Two - given a specific time window and a list of usernames, list all users available for the entire duration.'
	print '\nThe following participant\'s are available during the entire time window:'
	for i in availableParticipants:
		print participants[i].getEmail()
	print '\n'



#===================================================================================
#useCaseOne
#===================================================================================
#Given a single username in the local domain, provide a list of open times within the window specified. 
#If no window is specifieed, use a sane default.
def useCaseOne(): 
	print 'Use case one - Given a single username, provide his open times within the window specified.'
	availableMeetingSlots = list()
	index = 0
	for i in range(0, numOfWindowSlots):	                  
	   if meetingMatrix[index][i] == 0:			                    
	      availableMeetingSlots.append(i)

	email = participants[0].getEmail()
	print '\n', email, 'is available at the following times for 30 minutes at each time:'
	for i in availableMeetingSlots:					
	   slot = func.posixToPST(timeWindowSlots[i])						               
	   print slot
	print '\n'
