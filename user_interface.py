# user_interface.py

# checks for valid integer in range
def getNumber(minVal, maxVal):
	digit = None
	while not digit:
		ipt = raw_input("Enter a positive number between " + str(minVal) + " and " + str(maxVal) + " only: ") 
		if ipt.isdigit():
			digit = True
			option = int(ipt)
			if option < minVal or option > maxVal:
				digit = None
	return option

# gets space delimited emails
def getEmailAddr():
	emails = raw_input("\nEnter email addresses for users delimited by spaces: ") 
	return emails

def getName():
	names = list()
	num = getNumber(1, 10)
	print "Enter names of " + str(num) + " participants, each followed by a space"
	for n in range(0, num):
		ipt = raw_input(str(n+1) + ": ")
		names.append(ipt)
	return names

# display menu
# get option from user
def menu():
	print "Welcome to the meeting scheduling applicaiton"
	print "Choose of of the following options\n"
	print "1) Get available times for a single participant within a time window"
	print "2) Get emails of participants available for the entire time window"
	print "3) Get emails of participants who are available at the same time for at least 30 minutes\n"

	option = getNumber(1, 3)			# get number between 1 and 3
	return option
