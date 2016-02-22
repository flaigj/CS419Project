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
#monthStrToNum
#===================================================================================
#convert three letter month to string number
#Input: Three letter month
#Return: int representing month
def monthStrToNum(month):
	if "Jan" in month:
	    month = "01"
	elif "Feb" in month:
	    month = "02"
	elif "Mar" in month:
	    month = "03"
	elif "Apr" in month:
	    month = "04"
	elif "May" in month:
	    month = "05"
	elif "Jun" in month:
	    month = "06"
	elif "Jul" in month:
	    month = "07"
	elif "Aug" in month:
	    month = "08"
	elif "Sep" in month:
	    month = "09"
	elif "Oct" in month:
	    month = "10"
	elif "Nov" in month:
	    month = "11"
	elif "Dec" in month:
	    month = "12"
	return month


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
#createRfcTimestamp
#===================================================================================
#Create RFC3339 timestamp from Actor's time and date inputs
#Input: timestamp in timeWindow format
#Return: RFC3339 timestamp
def createRfcTimestamp(timestamp):
	timestampSplit = timestamp.split()
	month = monthStrToNum(timestampSplit[1])
	date = timestampSplit[3] + "-" + month + "-" + timestampSplit[2]
	time = "T" + timestampSplit[4] + "-" + "08:00"
	rfcTimestamp = date + time
	return rfcTimestamp


#===================================================================================
#monthIntToStr
#===================================================================================
#Convert month in int format to str
#Input: month as int
#Return: str representing month
def monthIntToStr(monthInt):
	if "01" in monthInt:
	   month = "Jan"
	elif "02" in monthInt:
	   month = "Feb"
	elif "03" in monthInt:
	   month = "Mar"
	elif "04" in monthInt:
	   month = "Apr"
	elif "05" in monthInt:
	   month = "May"
	elif "06" in monthInt:
	   month = "Jun"
	elif "07" in monthInt:
	   month = "Jul"
	elif "08" in monthInt:
	   month = "Aug"
	elif "09" in monthInt:
	   month = "Sep"
	elif "10" in monthInt:
	   month = "Oct"
	elif "11" in monthInt:
	   month = "Nov"
	elif "12" in monthInt:
	   month = "Dec"

	return month


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
