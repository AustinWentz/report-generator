import os
import subprocess

employees = ["AC" , "CJ", "CM", "DA", "DF", "JD", "JL", "KJ", "RR", "SC", "TS", "TR", "TK"]
report_file = raw_input("Please enter the name of the file you would like the report to be generated on: (ex. april.txt) ")

def genEmpReqs():
	print "Loading employee profiles..."
	for employee in employees:
		os.system('grep "' + employee + '" ' + report_file + " > " + employee + ".txt")
def genEmpReps():
	print "Generating employee reports..."
	for employee in employees:
		createRep(employee)
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
	for day in DaysWorked:
		lines = []
		fDay = open('day' + str(day) + '.txt', 'rt')
		
		for line in fDay:
			lines.append(line)
		lines.sort()
		
		f.write("\n")
		f.write("/////Day " + str(day) + "/////\n")
		#f.write("Hours worked: " + str(getHoursWorked(lines)))
		f.write("Samples processed: " + str(len(lines)) + "\n")
		f.write("AU Validity: " + str(int(getValidities('day' + str(day)))) + "\n")
		f.write("Billables processed: " + str(int(getTotalTox('day' + str(day)) - getNonBillables('day' + str(day)))) + "\n")
		f.write("Non-Billables processed: " + str(int(getNonBillables('day' + str(day)))) + "\n")
		f.write("Rejected Tox: " + str(int(getRejected('day' + str(day)))) + "\n")

def getValidities(emp):
	num = subprocess.check_output('grep "VALIDITY" ' + emp + ".txt | wc -l | bc", shell=True)
	return int(num[:-1])
def getNonBillables(emp):
	num = subprocess.check_output('grep "Not Billable" ' + emp + ".txt | wc -l | bc", shell=True)
	return int(num[:-1])
def getRejected(emp):
	num = subprocess.check_output('grep "Rejected" ' + emp + ".txt | wc -l | bc", shell=True)
	return int(num[:1])
def getTotalTox(emp):
	num = subprocess.check_output('grep "Tox" ' + emp + ".txt | wc -l | bc", shell=True)
	return float(num[:-1])	
def delFiles():
	for employee in employees:
		os.system("rm " + employee + ".txt")
def getHoursWorked(entries):
	if (len(entries) == 0):
		return 0
	if (len(entries) == 1):
		return 1

	start = entries[0]
	end = entries[len(entries) - 1]
	startHour = start[11:13]
	startPeriod = start[17:17]
	endHour = end[11:13]
	endPeriod = end[17:17]


def main():
	genEmpReqs()
	genEmpReps()
	print "...DONE"
main()
