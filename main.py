#main.py

#Import Modules
import user_interface as ui

# main entry point

welcomeOption = ui.welcome()	#welcome screen. Choose OSU catalog or meeting scheduler

if (welcomeOption == 1):
	print 'OSU module gets launched'	#OSU catalog
elif (welcomeOption == 2):
	option = ui.menu()			#Meeting scheduler
	import use_cases as uc					#Use cases functions

	if (option == 1):
		useCaseOne = uc.useCaseOne()		# One on one meeting
	
	if (option == 2):
		useCaseTwo = uc.useCaseTwo()		# Who can attend whole meeting
	
	if (option == 3):
		useCaseThree = uc.useCaseThree()	# Multiple person meeting
