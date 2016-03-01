#Use cases functions

#Import Modules
import find_open_slots as fos       #Available meeting time among all participants
import functions as func			#Helper functions
import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class FrankTest(webapp2.RequestHandler):
	def post(self):
		startWindow = self.request.get('startWindow')
		endWindow = self.request.get('endWindow')
		email = self.request.get('email')
		usecase = self.request.get('usecase')

		startWindow = "Mon " + startWindow + ":00 GMT-0800 (PST)"
		endWindow = "Mon " + endWindow + ":00 GMT-0800 (PST)"

		#self.response.write(startWindow)
		#self.response.write(endWindow)
		meetingAvailability = fos.createMeetingMatrix(startWindow, endWindow, email)

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

		#===================================================================================
		#useCaseThree
		#===================================================================================
		#Given a more broad window and a list of usernames, provide all time periods where all are available.
		#This is more in the nature of .when can I schedule the meeting?
		#Postcondition: display times when all participants are available durind timeWindow
		def useCaseThree(): 
			availableMeetingSlots = list()
			slots = list()
			for i in range(0, numOfWindowSlots):			#each time slot
				for j in range(0, numOfParticipants):		#each participant
					if(meetingMatrix[j][i] == 1):			#if participant is not available in this slot
						break								#go to next time slot	
					if(j == numOfParticipants - 1):			#if at last participant, make slot available
						availableMeetingSlots.append(i)

			#Display times when all participants are available during timeWindow
			print 'Use Case Three - time slots when all participants are available for 30 minutes:'
			for i in availableMeetingSlots:
				slots.append(str(func.posixToPST(timeWindowSlots[i])))
			return slots


		#===================================================================================
		#useCaseTwo
		#===================================================================================
		#Given a specific time window and a list of usernames, list all users available for the entire duration.
		#This is more in the nature of who can I expect at the meeting?
		def useCaseTwo(): 
			availableParticipants = list()
			slots = list()
			for i in range(0, numOfParticipants):		#each participant
				for j in range(0, numOfWindowSlots):	#each time slot
					if(meetingMatrix[i][j] == 1):		#if participant is not available in this slot
						break							#go to next participant
					if(j == numOfWindowSlots - 1):			#if at last participant, make slot available
						availableParticipants.append(i)

			#Display times when participants are available during the entire timeWindow
			print 'Use Case Two - participant(s) available during the entire time window'
			for i in availableParticipants:
				slots.append(str(participants[i].getEmail()))
			return slots


		#===================================================================================
		#useCaseOne
		#===================================================================================
		#Given a single username in the local domain, provide a list of open times within the window specified. 
		#If no window is specifieed, use a sane default.
		def useCaseOne(): 
			print 'Use case one - Given a time window provide a list of open time within window'
			availableMeetingSlots = list()
			slots = list()
			index = 0
			for i in range(0, numOfWindowSlots):	                  
			   if meetingMatrix[index][i] == 0:			                    
			      availableMeetingSlots.append(i)
			
			for i in availableMeetingSlots:					
			   slots.append(str(func.posixToPST(timeWindowSlots[i])))
			return slots

		slots = list()
		problem = ""
		if (usecase == "1"):
			slots = useCaseOne()
			problem = "Problem 1"
		elif (usecase == "2"):
			slots = useCaseTwo()
			problem = "Problem 2"
		else: 
			slots = useCaseThree()
			problem = "Problem 3"

		template_values = {'matrix':meetingMatrix,'slots':slots,'usecase':usecase,'problem':problem}

		template = JINJA_ENVIRONMENT.get_template('test.html')
		self.response.write(template.render(template_values))
		#Print matrix by participant
		#print '\nMeeting Matrix'
		#for index, elem in enumerate(participants):
		#		print meetingMatrix[index], elem.getEmail()
		#print '\n'

		# create template vars to print matrix in html/jinja
		#template_variables = []
		#for index, elem in enumerate(participants):
		#	testingVar = meetingMatrix[index], elem.getEmail()

		#template_values = {'matrix':meetingMatrix}

		#template = JINJA_ENVIRONMENT.get_template('test.html')
		#self.response.write(template.render(template_values))