import unittest 
#import find_open_slots as fos
import use_cases as uc
import sys

class testMeetingMatrix(unittest.TestCase):
	print '\n********************** TESTING BEGINS ***************************'
	print  '******************************************************************\n'
	startTime = "Feb 23 2016 08:00"
	endTime = "Feb 23 2016 15:00"

	matrixResults = list()
	array = [1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1]
	matrixResults.append(array)

	def test_createMeetingMatrix(self):
		for index, elem in enumerate(uc.participants):
			print '\n', uc.meetingMatrix[index], elem.getEmail()
			self.assertEqual(uc.meetingMatrix[index], self.matrixResults[index])


suite = unittest.TestLoader().loadTestsFromTestCase(testMeetingMatrix)
unittest.TextTestRunner(verbosity=2).run(suite)

print '\n************************* TESTING ENDS ****************************'
print  '******************************************************************* \n'
