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

def getEmailAddr():
	emails = raw_input("Enter email addresses for users delimited by spaces: ") 
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
	print "Choose of of the following options"
	print "1) Get meeting times for one on one meeting"
	print "2) Get available people for meeting"
	print "3) Get meeting times for multiple people"

	option = getNumber(1, 3)			# get number between 1 and 3
	return option