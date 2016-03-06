import unittest 
#import find_open_slots as fos
import use_cases as uc
import sys

print '\n********************** TESTING BEGINS ***************************'
print  '******************************************************************\n'

#Test if meeting matrix produces correct binary data
class testMeetingMatrix(unittest.TestCase):
	startTime = "Feb 23 2016 08:00"
	endTime = "Feb 23 2016 15:00"

	#array = [1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1]

	#Correct binary results for the time window specified to the right of it
	matrixResults = list()
	matrixResults = (
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],	#Feb 23 2016 08:00 to Feb 23 2016 15:00
		[1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],	#Feb 23 2016 08:00 to Feb 23 2016 15:00
		[1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1]	#Feb 23 2016 08:00 to Feb 23 2016 15:00
	)	

	def test_createMeetingMatrix(self):
		for idx1, elem1 in enumerate(self.matrixResults):
			for idx2, elem2 in enumerate(uc.participants):
				print '\n', uc.meetingMatrix[idx2], elem2.getEmail()
				self.assertEqual(uc.meetingMatrix[idx2], elem1, ('Failed at matrixResults index ', idx1))

suite = unittest.TestLoader().loadTestsFromTestCase(testMeetingMatrix)
unittest.TextTestRunner(verbosity=2).run(suite)

print '\n************************* TESTING ENDS ****************************'
print  '******************************************************************* \n'
