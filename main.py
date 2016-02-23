#main.py

#Import Modules
import user_interface as ui

# main entry point

option = ui.menu()

import use_cases as uc					#Use cases functions

if (option == 1):
	useCaseOne = uc.useCaseOne()		# One on one meeting

if (option == 2):
	useCaseTwo = uc.useCaseTwo()		# Who can attend whole meeting

if (option == 3):
	useCaseThree = uc.useCaseThree()	# Multiple person meeting
