import os

employees = ["AC" , "CJ", "CM", "DA", "DF", "JD", "JL", "KJ", "RR", "SC", "TS", "TR", "TK"]

for employee in employees:
	os.system("rm " + employee + "_report.txt")

os.system("rm Monthly_report.txt")
