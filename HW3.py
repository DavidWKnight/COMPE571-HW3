import sys

NUMBER_OF_TASKS=0
TIME_TO_EXECUTE=1
ACTIVE_POWER_1188MHz=2
ACTIVE_POWER_918MHz=3
ACTIVE_POWER_648MHz=4
ACTIVE_POWER_384MHz=5
IDLE_POWER=6

NAME_OF_TASK=0
DEADLINE=1
WCET_1188MHz=2
WCET_918MHz=3
WCET_648MHz=4
WCET_384MHz=5

def calcEnergy(milliwatts, seconds):
	return ((int(milliwatts)/1000.0)*int(seconds))

def RM(taskInfo, taskList):
	print("Hello RM")

def RM_EE(taskInfo, taskList):
	print("Hello RM EE")

def EDF(taskInfo, taskList):
	print("Hello EDF")

def EDF_EE(taskInfo, taskList):
	print("Hello EDF EE")

def openFile(filePath):
	with open(filePath, 'r') as inFile:
		taskInfo = inFile.readline()
		taskList = inFile.readlines()

		taskInfo = taskInfo.split()
		taskList = [i.split() for i in taskList]
		taskList.remove([])

	return (taskInfo, taskList)

if __name__ == "__main__":
	(taskInfo, taskList) = openFile(sys.argv[1])
	if ("RM" in sys.argv and "EE" in sys.argv):
		RM_EE(taskInfo, taskList)
	elif ("RM" in sys.argv):
		RM(taskInfo, taskList)
	elif ("EDF" in sys.argv and "EE" in sys.argv):
		EDF_EE(taskInfo, taskList)
	elif ("EDF" in sys.argv):
		EDF(taskInfo, taskList)
	else:
		print("Please input valid command line parameters")
