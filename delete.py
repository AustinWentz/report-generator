import os

employees = ["AC" , "CJ", "CM", "DA", "DF", "JD", "JL", "KJ", "RR", "SC", "TS", "TR", "TK"]

for employee in employees:
	os.system("rm " + employee + ".txt")
	os.system("rm " + employee + "_report.txt")
for days in range(1,32):
	os.system("rm day" + str(days) + ".txt")

os.system("rm Monthly_report.txt")
