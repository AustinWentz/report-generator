#############
# Created by Austin Wentz
# ESA Labs
# Last Updated: May 13th, 2016
############
import os
import subprocess
from datetime import datetime

#list of employees
employees = ["AC" , "CJ", "CM", "DA", "DF", "JD", "JL", "RR", "SC", "TS", "TR", "TK"]
#file to be read from
report_file = raw_input("Please enter the name of the file you would like the report to be generated on: (ex. april.txt) ")

#generates <employee>.txt files
def genEmpReqs():
	print "Loading employee profiles..."
	for employee in employees:
		os.system('grep "' + employee + '" ' + report_file + " > " + employee + ".txt")

#calls createRep() for every employee
def genEmpReps():
	monthlyAcc = []
	highestPerformingEmployee = "None"
	lowestPerformingEmployee = "None"
	highestAcc = 0.0
	lowestAcc = 1000.0

	print "Generating employee reports..."
	
	index = 0;
	for employee in employees:
		monthlyAcc.append(createRep(employee))
		
	for employee in employees:
		if (monthlyAcc[index] > highestAcc):
			highestAcc = monthlyAcc[index]
			highestPerformingEmployee = employee
		
		if (monthlyAcc[index] < lowestAcc):
			lowestAcc = monthlyAcc[index]
			lowestPerformingEmployee = employee
		index = index + 1

	with open("Monthly_report.txt", 'a') as repFile:
		repFile.write('---------------------\n')
		repFile.write('The highest performing employee of the month based on average accessions per hour was ' + highestPerformingEmployee + ' with and average of ' + str(highestAcc) + ' samples proccesed per hour.\n')
		repFile.write('The lowest performing employee of the month based on average accessions per hour was ' + lowestPerformingEmployee + ' with and average of ' + str(lowestAcc) + ' samples proccesed per hour.\n')

#creates <employee_report>.txt files and generates useful statistics
def createRep(name):
	numVal = getValidities(name)
	numNonBillables = getNonBillables(name)
	numRejected = getRejected(name)
	totalTox = getTotalTox(name)
	
	if (totalTox != 0):
		percentRejected = (numRejected / totalTox) * 100
	
	f = open(name + '_report.txt', 'wt')

	f.write("AU Validity: " + str(int(numVal)) + "\n")
	f.write("Billables processed: " + str(int(totalTox - numNonBillables)) + "\n")
	f.write("Non-Billables processed:  " + str(int(numNonBillables)) + "\n")
	f.write("Rejected Tox: " + str(int(numRejected)) + "\n")
	f.write("Total Tox samples processed: " + str(int(totalTox)) + "\n")
	
	if (totalTox != 0):
		f.write("Percentage of Tox samples rejected: " + str(percentRejected) + "%\n")
	f.write("------Day breakdown-----\n")

	DaysWorked = []
	#Day Breakdown
	for day in range(1,32):
		
		if(day < 10):
			try:
				string = subprocess.check_output("""grep '/0""" + str(day) + """/2016' """ + name + ".txt > day" + str(day) + ".txt", shell=True)
				DaysWorked.append(day)
			except Exception:
				pass
		else:
			try:
				string = subprocess.check_output("""grep '/""" + str(day) + """/2016' """ + name + ".txt > day" + str(day) + ".txt", shell=True)
				DaysWorked.append(day)
			except Exception:
				pass
	dailyAccAverage = []

	for day in DaysWorked:
		lines = []
		fDay = open('day' + str(day) + '.txt', 'rt')
		
		for line in fDay:
			lines.append(line)

		sortedLines = sortByHour(lines)

		hoursAcc = getHoursAcc(sortedLines)
		convertedHours = hourConvert(sortedLines)
		samplesProcessed = float(len(lines))

		if (hoursAcc != 0):
			averageAcc = (samplesProcessed/hoursAcc)
			dailyAccAverage.append(averageAcc)
		else:
			averageAcc = 0
		
		checkedHours = {'5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13' : 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0}

		#hour report analyzer
		for con in convertedHours:
			for key in checkedHours:
				if (key == con):
					checkedHours[key] = checkedHours[key] + 1
		
		f.write("\n")
		f.write("/////Day " + str(day) + "/////\n")
		f.write("Hours spent accessioning: " + str(hoursAcc) + "\n")
		f.write("Samples processed: " + str(int(samplesProcessed)) + "\n")
		f.write("Average number of samples processed per hour spent accessioning: " + str(averageAcc) + "\n")
		#f.write("AU Validity: " + str(int(getValidities('day' + str(day)))) + "\n")
		#f.write("Billables processed: " + str(int(getTotalTox('day' + str(day)) - getNonBillables('day' + str(day)))) + "\n")
		#f.write("Non-Billables processed: " + str(int(getNonBillables('day' + str(day)))) + "\n")
		#f.write("Rejected Tox: " + str(int(getRejected('day' + str(day)))) + "\n")
		f.write("----Hour breakdown----\n")
		
		#hour calculator
		for hour in range(5,20):
			if (hour <= 12):
				f.write(str(hour) + " AM: " + str(checkedHours[str(hour)]) + "\n")
			else:
				f.write(str(hour - 12) + " PM: " + str(checkedHours[str(hour)]) + "\n")

	#daily/monthly average	
	sumOfAvg = 0.0
	for average in dailyAccAverage:
		sumOfAvg = sumOfAvg + average
	if (len(dailyAccAverage) != 0):	
		monthlyAccAverage = (sumOfAvg / len(dailyAccAverage))
	else:
		monthlyAccAverage = 0.0

	with open('Monthly_report.txt', 'a') as repFile:
		repFile.write(name + "'s sample average per hour for the month was: " + str(monthlyAccAverage) + "\n")
	
	#file upkeep
	for day in range(1,32):
		os.system("rm day" + str(day) + ".txt")
	f.close()

	return monthlyAccAverage

#gets total number of AU Validities
def getValidities(emp):
	num = subprocess.check_output('grep "VALIDITY" ' + emp + ".txt | wc -l | bc", shell=True)
	return int(num[:-1])

#gets total number of non billables
def getNonBillables(emp):
	num = subprocess.check_output('grep "Not Billable" ' + emp + ".txt | wc -l | bc", shell=True)
	return int(num[:-1])

#gets total number of Tox samples rejected
def getRejected(emp):
	num = subprocess.check_output('grep "Rejected" ' + emp + ".txt | wc -l | bc", shell=True)
	return int(num[:1])

#gets total number of Tox samples
def getTotalTox(emp):
	num = subprocess.check_output('grep "Tox" ' + emp + ".txt | wc -l | bc", shell=True)
	return float(num[:-1])

#file cleanup
def delFiles():
	for employee in employees:
		os.system("rm " + employee + ".txt")

#gets number of hours an employee worked for a given day
def getHoursAcc(entries):
	if (len(entries) == 0):
		return 0;
	if (len(entries) == 1):
		return 1;

	start = entries[0]
	end = entries[len(entries) - 1]

	if (start[6:7] == 'P'):
		startInt = 12 + (int(start[0:2]) % 12)
	else:
		startInt = int(start[0:2])

	if (end[6:7] == 'P'):
		endInt = 12 + (int(end[0:2]) % 12)
	else:
		endInt = int(end[0:2])

	return ((endInt - startInt) + 1)

#sorts employee day reqs by hour
#returns: list of hours sorted
def sortByHour(reqs):
	hours = []
	for req in reqs:
		hours.append(req[11:19])
	formatedHours = sorted([datetime.strptime(regex_obtained_str, '%I:%M %p') for regex_obtained_str in hours])
	finalSorted = [hour.strftime('%I:%M %p') for hour in formatedHours]
	return finalSorted

#converts hours AM-PM to 24 hour clock
def hourConvert(hours):

	convertedHours = []
	for hour in hours:
		if (hour[6:7] == 'P'):
			temp = 12 + (int(hour[0:2]) % 12)
			convertedHours.append(str(temp))
		else:
			temp = int(hour[0:2])
			convertedHours.append(str(temp))
	
	strippedHours = []
	for hour in convertedHours:
		if (hour[0:1] == '0'):
			strippedHours.append(str(hour[1:2]))
		else:
			strippedHours.append(str(hour[0:2]))
	
	return strippedHours

#driver
def main():
	genEmpReqs()
	genEmpReps()
	delFiles()
	print "...DONE"
main()
