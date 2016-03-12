import unittest 
import find_open_slots as fos
import use_cases as uc
import sys

print '\n********************** TESTING BEGINS ***************************'
print  '******************************************************************\n'

#Test if meeting matrix produces correct binary data
#A test input is the combination of timeStart, timeEnd, and emails with the same index.
#Use the same index to obtain the proper matrixResult
#Example: timeStart[1] + timeEnd[1] + emails[1] = matrixResults[1]
class testMeetingMatrix(unittest.TestCase):
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
		#"supermanalwaysfree@gmail.com"
	)

	#Correct binary results for each index combination
	matrixResults = list()
	matrixResults = (
		[1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],	
		[1, 1, 0, 0, 1, 1, 0, 0, 0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	)	

	def test_createMeetingMatrix(self):
		print '\n'
		for i in range(0, len(self.timeStart) ):
			fos.createMeetingMatrix(self.timeStart[i], self.timeEnd[i], self.emails[i])
			ucMatrix = str(uc.meetingMatrix[0])	#index must always be zero
			resultMatrix = str(self.matrixResults[i])

			print 'Index', i, '    ', self.timeStart[i], 'to', self.timeEnd[i], self.emails[i]
			print ucMatrix, 'received'
			print str(self.matrixResults[i]), 'should have received'	
			print '\n'

			self.assertEqual(ucMatrix, resultMatrix, ('Failed at index ', i) )

suite = unittest.TestLoader().loadTestsFromTestCase(testMeetingMatrix)
unittest.TextTestRunner(verbosity=2).run(suite)

print '\n************************* TESTING ENDS ****************************'
print  '******************************************************************* \n'
