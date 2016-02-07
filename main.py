#Main Program

#Import Modules
import use_cases as uc			#Use cases functions

#Use Case 3
#Given a more broad window and a list of usernames, provide all time periods where all are available
useCaseThree = uc.useCaseThree()


#Use Case 2
#Given a specifc time window and a list of usernames, list all users available for the entire duration.
#This is more in the nature of .who can I expect at the meeting?
useCaseTwo = uc.useCaseTwo()


#Use Case 1
#Given a single username in the local domain, provide a list of open times within the window speci.ed.
#If no window is speci.ed, use a sane default.
useCaseOne = uc.useCaseOne()