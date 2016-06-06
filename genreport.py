################################
# Created by Austin Wentz      #
# ESA Labs		       #
# Last Updated: June 6, 2016 #
################################
import os
import sys
import subprocess
from datetime import datetime

#list of employees
employees = ["AC", "CB", "CJ", "CM", "DA", "GM", "JD", "JL", "JM", "LJ", "RR", "SC", "TK", "TL", "TR", "TS"]

#defining months of the year
monthsOfTheYear = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

#files to be read from
if (len(sys.argv) == 2):
	report_file = sys.argv[1]
elif (len(sys.argv) == 3):
	report_file = sys.argv[1]
	mistakes_file = sys.argv[2]
else:
	print "Please enter the correct format: python genreport.py <report_file.txt> <mistakes_file.txt(optional)>"
	sys.exit()

#generates <employee>.txt files
def genEmpReqs():
	print "Loading employee profiles..."

	#creating employee.txt files for temporary use
	for employee in employees:
		os.system('grep "' + employee + '" ' + report_file + " > " + employee + ".txt")

#calls createRep() for every employee
def genEmpReps():
	monthlyAcc = []

	print "Analyzing employee mistakes..."

	mistakes = float(getAllMistakes())
	allAcc = getAllAcc()
	highestPerformingEmployee = "None"
	lowestPerformingEmployee = "None"
	highestAcc = 0.0
	lowestAcc = 1000.0

	print "Generating employee reports..."
	
	#adding each employee monthly accession average to a list
	index = 0;
	for employee in employees:
		monthlyAcc.append(createRep(employee))
	
	print "Calculating employee stats..."

	#finding the highest and lowest performing employee based on monthly accession averages
	for employee in employees:
		if (monthlyAcc[index] > highestAcc):
			highestAcc = monthlyAcc[index]
			highestPerformingEmployee = employee
		
		if (monthlyAcc[index] < lowestAcc):
			lowestAcc = monthlyAcc[index]
			lowestPerformingEmployee = employee
		index = index + 1
	
	print "Writing monthly report file..."

	#writing to Monthly_report.txt file
	with open("Monthly_report.txt", 'a') as repFile:
		repFile.write('---------------------\n')
		repFile.write('The highest performing employee of the month based on average accessions per hour was ' + highestPerformingEmployee + ' with and average of ' + str(highestAcc) + ' samples processed per hour.\n')
		repFile.write('The lowest performing employee of the month based on average accessions per hour was ' + lowestPerformingEmployee + ' with and average of ' + str(lowestAcc) + ' samples processed per hour.\n')
		repFile.write('---------------------\n')
		repFile.write('Total mistakes made this month: ' + str(int(mistakes)) + '\n')
		repFile.write('Total number of samples accessioned (AU + Tox + PGx): ' + str(allAcc) + '\n')
		
		#writes mistake percentages
		if (allAcc != 0):
			repFile.write("Total percentage of samples that had mistakes: " + str((mistakes/allAcc) * 100) + "%\n")

#creates <employee_report>.txt files and generates useful statistics
def createRep(name):
	numVal = getValidities(name)
	numNonBillables = getNonBillables(name)
	totalTox = float(getTotalTox(name))
	totalPgx = getTotalPgx(name)
	totalMistakes = getTotalMistakes(name)
	
	#calculating percentage of mistakes for the employee
	if (totalTox + totalPgx != 0):
		percentMistakes = (totalMistakes / (totalTox + totalPgx)) * 100	
	
	#writing to employee_report.txt
	f = open(name + '_report.txt', 'wt')

	f.write("Employee: " + name + "\n\n")
	f.write("------Monthly Stats------\n")
	f.write("AU Validity: " + str(int(numVal)) + "\n")
	f.write("Billables processed: " + str(int((totalTox + totalPgx) - numNonBillables)) + "\n")
	f.write("Non-Billables processed:  " + str(int(numNonBillables)) + "\n")
	f.write("Total Tox samples processed: " + str(int(totalTox)) + "\n")
	f.write("Total PGx samples processed: " + str(int(totalPgx)) + "\n")
	f.write("Total mistakes made: " + str(int(totalMistakes)) + "\n")
	
	if (totalTox + totalPgx != 0):
		f.write("Percentage of samples processed that had mistakes: " + str(percentMistakes) + "%\n")
	
	#breaking it down by day
	f.write("\n------Day breakdown------\n")

	DaysWorked = []

	#day breakdown
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
		month = (lines[0])[0:2]
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
		
		#breaking it down by the hour	
		f.write("\n")
		f.write("/////" + monthsOfTheYear[month] + " " + str(day) + "/////\n")
		f.write("Hours spent accessioning: " + str(hoursAcc) + "\n")
		f.write("Samples processed: " + str(int(samplesProcessed)) + "\n")
		f.write("Average number of samples processed per hour spent accessioning: " + str(averageAcc) + "\n")
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
#returns: (int) AU for an employee
def getValidities(emp):
	num = subprocess.check_output('grep "VALIDITY" ' + emp + ".txt | wc -l | bc", shell=True)
	return int(num[:-1])

#gets total number of non billables
#returns: (int) Not billable for an employee
def getNonBillables(emp):
	num = subprocess.check_output('grep "Not Billable" ' + emp + ".txt | wc -l | bc", shell=True)
	return int(num[:-1])

#gets total number of Tox samples
#returns: (int) Tox samples for an employee
def getTotalTox(emp):
	num = subprocess.check_output('grep "Tox" ' + emp + ".txt | wc -l | bc", shell=True)
	return float(num[:-1])

#gets total number of PGx samples for en employee
#returns: (int) PGx samples for an employee
def getTotalPgx(emp):
	num = subprocess.check_output('grep "PGx" ' + emp + ".txt | wc -l | bc", shell = True)
	return int(num[:-1])

#gets total number of mistakes for an employee
#returns: (int) mistakes for an employee
def getTotalMistakes(emp):
	try:
		num = subprocess.check_output('grep "' + emp + '" ' + mistakes_file + " | wc -l | bc", shell=True)
		return int(num[:-1])
	except Exception:
		return 0

#gets all tox, pgx, AU Validity
#returns: (int) tox + pgx + AU
def getAllAcc():
	num1 = subprocess.check_output('grep "VALIDITY" ' + report_file + " | wc -l | bc", shell=True)
	numAU = int(num1[:-1])
	num2 = subprocess.check_output('grep "Tox" ' + report_file + " | wc -l | bc", shell=True)
	numTox = int(num2[:-1])
	num3 = subprocess.check_output('grep "PGx" ' + report_file + " | wc -l | bc", shell=True)
	numPgx = int(num3[:-1])
	return numPgx + numTox + numAU

#gets all mistakes form mistakes file
#returns: (int) all entries in mistakes file
def getAllMistakes():
	try:
		num = subprocess.check_output('wc -l ' + mistakes_file, shell=True)
		return int(num[5:-(len(mistakes_file) + 2)])
	except Exception:
		print "The mistakes file was empty!"
		return 0

#file cleanup
def delFiles():
	print "Cleaning up files..."

	for employee in employees:
		os.system("rm " + employee + ".txt")

#gets number of hours an employee worked for a given day
#returns: (int) hours spent accessioning
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
#returns: (list) of hours sorted
def sortByHour(reqs):
	hours = []
	for req in reqs:
		hours.append(req[11:19])
	formatedHours = sorted([datetime.strptime(regex_obtained_str, '%I:%M %p') for regex_obtained_str in hours])
	finalSorted = [hour.strftime('%I:%M %p') for hour in formatedHours]
	
	return finalSorted

#converts hours AM-PM to 24 hour clock
#returns: (int) value on a 24 hour clock
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
