import os

employees = ["AC", "CB", "CJ", "CM", "DA", "GM", "JD", "JL", "JM", "LJ", "RR", "SC", "TL", "TS", "TR", "TK"]

print "Deleting employee and report files..."

for employee in employees:
	os.system("rm " + employee + ".txt")
	os.system("rm " + employee + "_report.txt")

print "Cleaning up loose files..."

for day in range(0,32):
	os.system("rm day" + str(day) + ".txt")

print "Removing monthly report files..."

os.system("rm Monthly_report.txt")

print "...DONE"
