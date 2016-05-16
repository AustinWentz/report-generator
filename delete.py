import os

employees = ["AC" , "CJ", "CM", "DA", "DF", "JD", "JL", "JM", "RR", "SC", "TS", "TR", "TK"]

for employee in employees:
	os.system("rm " + employee + ".txt")
	os.system("rm " + employee + "_report.txt")

for day in range(0,32):
	os.system("rm day" + str(day) + ".txt")

os.system("rm Monthly_report.txt")
