#Helper functions

import calendar
import datetime
import time
from pytz import timezone
import pytz

#Data structure to store Google times
#Signature of Google's data return: Tue Jan 26 2016 0800 GMT-0800 (PST)
class GoogleTime:
	def __init__(self, dayStr, month, day, year, time):
		self.dayStr = dayStr
		self.month = month
		self.day = day
		self.year = year
		self.time = time
	
	def getDayStr(self):
		return self.dayStr	
	
	def getMonth(self):
		return self.month
	
	def getDay(self):
		return self.day	

	def getYear(self):
		return self.year	

	def getTime(self):
		return self.time	


#===================================================================================
#parseGoogleTime
#===================================================================================
#Parse through Google's date/time return data and store in GoogleTime
#Input: Participants object 
#Return: GoogleTime object
def parseGoogleTime(googleTime):
	txt = googleTime.split()	#parse googleTime
	time = GoogleTime(txt[0], txt[1], txt[2], txt[3], txt[4]) #store in class object
	return time


#===================================================================================
#monthStringToInt
#===================================================================================
#Convert month in string format to its numeric representation
#Input: month as string (e.g., Jan, january, January, etc...)
#Return: int representing month
def monthStringToInt(monthString):
    #monthInt = monthString.strip()[:3].lower()
    monthInt = monthString.lower()
    conversion = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }

    try:
        out = conversion[monthInt]
        return out
    except:
        raise ValueError('Not a month')


#===================================================================================
#googleTimeToPosix
#===================================================================================
#Convert GoogleTime object to unix time stamp in seconds
#Input: GoogleTime object
#Return: int time in seconds
def googleTimeToPosix(googleTime):
	dateFormat = '%Y %m %d %H:%M:%S' 
	timeStart = datetime.datetime.strptime(googleTime.getYear() + ' ' +
									str(monthStringToInt(googleTime.getMonth())) + ' ' +
									googleTime.getDay() + ' ' +
									googleTime.getTime(), 
									dateFormat)

	time_ts = time.mktime(timeStart.timetuple())	#convert to unix timestamp
	return time_ts 


#===================================================================================
#timeStrToPosix
#===================================================================================
#Convert GoogleTime object to unix time stamp in seconds
#Input: GoogleTime as string
#Return: int time in seconds
def timeStrToPosix(timeStr):
	dateFormat = '%Y %m %d %H:%M:%S' 
	txt = timeStr.split()    #parse timeStr
	timeStart = datetime.datetime.strptime(txt[3] + ' ' +
									str(monthStringToInt(txt[1])) + ' ' +
									txt[2] + ' ' +
									txt[4], 
									dateFormat)
	
	time_ts = time.mktime(timeStart.timetuple())	#convert to unix timestamp
	return time_ts 


#===================================================================================
#hoursRange
#===================================================================================
#Calculate number of minutes between the start and end times 
#Input 1: GoogleTime object start
#Input 2: GoogleTime object end
#Return: minutes between start and end time
def hoursRange(start, end):
	#Convert GoogleTime to unix time in seconds
	timeStartUnix = googleTimeToPosix(start)
	timeEndUnix = googleTimeToPosix(end)
	return int(timeEndUnix - timeStartUnix) / 60	
			

#===================================================================================
#createTimeSlots()
#===================================================================================
#Create n time slots based on beginning and end times, and minutes to increment
#Input 1: start GoogleTime object 
#Input 2: end GoogleTime object
#Input 3: minutes to increment
#Return: array of GoogleTime objects in sequential order in Posix format
def createTimeSlots(timeStart, timeEnd, minutes):
	# convert to unix timestamp
	timeStartUnix = googleTimeToPosix(timeStart)
	timeEndUnix = googleTimeToPosix(timeEnd)

	#Increment timeStart by minutes until timeEnd is reached
	timeWindowSlots = []		
	while timeStartUnix <= timeEndUnix:
		timeWindowSlots.append(timeStartUnix)
		timeStartUnix += (minutes * 60)		#increment by minutes as seconds
			
	return timeWindowSlots


#===================================================================================
#posixToPST
#===================================================================================
#Change POSIX time in seconds to PST in date format
#Input: POSIX in seconds
#Return: PST in date format
def posixToPST(posixTime):
	date = datetime.datetime.fromtimestamp(posixTime)
	return date