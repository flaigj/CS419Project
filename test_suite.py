import subprocess
import os
import use_cases as uc

#Test if meeting matrix produces correct binary data
#A test input is the combination of timeStart, timeEnd, and emails with the same index.
#Use the same index to obtain the proper matrixResult
#Example: timeStart[1] + timeEnd[1] + emails[1] = matrixResults[1]
def testMeetingMatrix():
	timeStart = list()	
	timeStart = (
		"Feb 23 2016 08:00",
		"Feb 24 2016 10:00",
		"Mar 05 2016 0:00"
	)

	timeEnd = list()	
	timeEnd = (
		"Feb 23 2016 15:00",
		"Feb 24 2016 14:00",
		"Mar 05 2016 23:30"
	)

	emails = list()
	emails = (
		"groupnineemail@gmail.com",
		"groupnineemail@gmail.com",
		"groupnineemail@gmail.com"
	)

	#Correct binary results for each index combination
	matrixResults = list()
	matrixResults = (
		[1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],	
		[1, 1, 0, 0, 1, 1, 0, 0, 0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	)	
	

	print 'this is testMeetingMatrix()'

def startMainProgram():
	#subprocess.call('/nfs/stak/students/e/eslamif/cs419/git_group/main.py')	
	script = """
		python main.py "Feb 23 2016 08:00" "Feb 23 2016 15:00" "groupnineemail@gmail.com"
	"""	

	os.system("bash -c '%s'" %script)

def startTestSuite():
	print '\n********************** TESTING BEGINS ***************************'
	print  '******************************************************************\n'

	startMainProgram()
	
	print '\n********************** TESTING ENDS ****************************'
	print  '****************************************************************** \n'

startTestSuite()
