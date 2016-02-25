#find_open_slots.py

import google_api_call as google    #Availble time slot for each individual participant
import functions as func			#Helper functions
import datetime

class MeetingAvailability:
	def __init__(self, meetingMatrix, participantData, numOfWindowSlots, timeWindowSlots):
		self.meetingMatrix = meetingMatrix
		self.participants = participantData
		self.numOfWindowSlots = numOfWindowSlots
		self.timeWindowSlots = timeWindowSlots

	def getMeetingMatrix(self):
		return self.meetingMatrix

	def getParticipants(self):
		return self.participants

	def getNumOfWindowSlots(self):
		return self.numOfWindowSlots

	def getTimeWindowSlots(self):
		return self.timeWindowSlots


def createMeetingMatrix():
	#Get time window data from Google API call
	timeWindowData = google.getTimeWindowData()

	#Get participants data from Google API call
	participantData = google.getParticipantData(timeWindowData)

	# parseGoogleTime returns class object for getday - getYear
	#Parse start and end times of timeWindow provided by Actor and store in object GoogleTime
	timeWindowStart = func.parseGoogleTime(timeWindowData[0])
	timeWindowEnd = func.parseGoogleTime(timeWindowData[1])
	
	#Calculate the number of 30 minute slots in timeWindow
	minutesRange = func.hoursRange(timeWindowStart, timeWindowEnd)
	
	#Create Actor's timeWindow slots for meeting times in Posix format
	timeWindowSlots = func.createTimeSlots(timeWindowStart, timeWindowEnd, 30)
	numOfWindowSlots = len(timeWindowSlots)
	numOfParticipants = len(participantData)

	#Create meeting matrix for each timeWindowSlot and participant
	meetingMatrix = list()	#binary matrix displaying availability for all participants
	for i in range(0, numOfParticipants):	
		meetingMatrix.append('Null')			#initiate matrix to null
	
	index2 = 0
	index3 = 0
	for index, elem in enumerate(participantData):		#Each participant
		timeSlots = list()	#temp storage for each participant's time slot
		#print '----------------------------'
		#print elem.getName()
		numOfParticipantSlots = len(participantData[index].getBusyTimeSlot())
		#print 'numOfParticipantSlots = ', numOfParticipantSlots
	
		while(index2 < numOfWindowSlots):		#Actor's desired meeting slots
			windowSlot = timeWindowSlots[index2]
			participantSlot = participantData[index].getBusyTimeSlot()
	
			#Compare participant's time slot to Actor's desired meeting slots
			#print 'index3 = ', index3
			#print 'index2 = ', index2
			if(index3 < numOfParticipantSlots):		#Participant time slot
				participantPosix = func.timeStrToPosix(participantSlot[index3])
				print func.posixToPST(participantPosix)
				print func.posixToPST(windowSlot)
	
				if(participantPosix == windowSlot):
					print 'equal'
					timeSlots.append(1)		#participant not available in meeting slot
					index2 += 1		#next Actor's meeting slot
					#continue	
	
				if(participantPosix < windowSlot):
					print 'less'
					timeSlots.append(0)		#participant available in meeting slot
					index2 += 1		#next Actor's meeting slot
					index3 += 1		#next participant's time slot
					#continue	
	
				if(participantPosix > windowSlot):
					print 'more'
					timeSlots.append(0)		#participant available in meeting slot
					index2 += 1		#next Actor's meeting slot
					index3 += 1		#next participant's time slot
					#continue	
	
			#Go to next participant if all participant time slots is checked
			if(index3 == numOfParticipantSlots or index2 == numOfWindowSlots):
				#Set remainding meetingMatrix to 1, indicating no availability
				for j in range(index2, numOfWindowSlots):
					timeSlots.append(1)		#mark remainder as unvailable
	
				index2 = 0	#reset iterator to first Actor's meeting slot
				index3 = 0	#reset iterator to first time slot for next participant
				
				#Store participant availability in meeting matrix
				meetingMatrix[index] = timeSlots
		
				#print meetingMatrix
				break		#got to next participant


	#store meetingMatrix in MeetingAvailability object
	meetingAvailability = MeetingAvailability(meetingMatrix, participantData, numOfWindowSlots, timeWindowSlots)
	return meetingAvailability
	#return meetingMatrix
