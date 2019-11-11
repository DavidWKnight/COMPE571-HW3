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

def condenseSchedule(schedule):
	# schedule is a list of lists containing the task the is executed at every point in time
	# each index in schedule represents a single second of execution
	# schedule[0][0] is the name of the task that is running at time t=1
	# schedule[1][1] is the frequency of the task that is running at time t=2
	# schedule[10][2] is the active power of the task that is running at time t=11

	condensedSchedule = []
	condensedSchedule.append(schedule[0])
	executionTimes = [0]

	totalEnergy = 0
	idleTime = 0

	result = ""

	for line in schedule:
		if (condensedSchedule[-1] == line):
			executionTimes[-1] = executionTimes[-1] + 1
		else:
			condensedSchedule.append(line)
			executionTimes.append(1)
		if (line[0] == "IDLE"):
			idleTime = idleTime + 1
	counter = 1
	for i in range(len(condensedSchedule)):
		Energy = calcEnergy(condensedSchedule[i][2], executionTimes[i])
		result += f"{counter}\t{condensedSchedule[i][0]}\t{condensedSchedule[i][1]}\t{executionTimes[i]}\t{Energy}J\n"
		counter = counter + executionTimes[i]
		totalEnergy = totalEnergy + Energy
	
	result += f"Total energy consumed: {totalEnergy}J\n"
	result += f"% of time spent idle: {round((idleTime / len(schedule))*100.0, 2)}%\n"
	result += f"Total execution time: {len(schedule) - idleTime}s\n"
	return result

def RM(taskInfo, taskList):
	print("Hello RM")

def RM_EE(taskInfo, taskList):
	print("Hello RM EE")

TASK_NAME = 0
TASK_DEADLINE = 1
TASK_EXEC_TIME = 2
TASK_ACTIVE_POWER = 3
TASK_FREQUENCY = 4
def findEDF(taskInfo, taskList):
	U = 0
	for task in taskList:
		U = U + task[TASK_EXEC_TIME]/task[DEADLINE]
	if not (U <= 1):
		return ""
	
	runningTasks = []
	schedule = []

	for timeStep in range(int(taskInfo[TIME_TO_EXECUTE])):
		# Check if task needs to be moved back into running tasks list
		#print(taskList[3])
		for task in taskList:
			if (timeStep % task[TASK_DEADLINE] == 0):
				runningTasks.append(task[:])
		# Calculate deadlines
		deadlines = [(task[TASK_DEADLINE]-task[TASK_EXEC_TIME]) for task in runningTasks]
		if (deadlines == []):
			# No tasks need to run, IDLE state
			schedule.append(["IDLE", "IDLE", IDLE_POWER])
		else:
			# Find highest priorty deadline and record it
			highestPriorityTask = deadlines.index(min(deadlines))
			schedule.append([runningTasks[highestPriorityTask][TASK_NAME], runningTasks[highestPriorityTask][TASK_FREQUENCY], runningTasks[highestPriorityTask][TASK_ACTIVE_POWER]])
			runningTasks[highestPriorityTask][TASK_EXEC_TIME] = runningTasks[highestPriorityTask][TASK_EXEC_TIME] - 1
		
			# Remove task from running list if it has finished executing
			if (runningTasks[highestPriorityTask][TASK_EXEC_TIME] <= 0):
				del runningTasks[highestPriorityTask]
		# Reduce deadline for tasks
		for task in runningTasks:
			task[TASK_DEADLINE] = task[TASK_DEADLINE] - 1
			# Sanity check, should not be 0 if we passed schedulability test
			if (task[TASK_DEADLINE] == 0):
				print("EDF: A deadline is due with no time left to complete it")
				return
	return condenseSchedule(schedule)

def EDF(taskInfo, taskList):
	shortTaskList = []
	for task in taskList:
		# Assume 1188MHz fir non EE EDF
		shortTaskList.append([task[NAME_OF_TASK], task[DEADLINE], task[WCET_1188MHz], ACTIVE_POWER_1188MHz, "1188"])
	return findEDF(taskInfo, shortTaskList)	

def EDF_EE(taskInfo, taskList):
	print("Hello EDF EE")

def openFile(filePath):
	with open(filePath, 'r') as inFile:
		# Parse input file
		taskInfo = inFile.readline()
		taskList = inFile.readlines()

		# Split lines into sub strings
		taskInfo = taskInfo.split()
		taskList = [i.split() for i in taskList]
		for task in taskList:
			task[DEADLINE] = int(task[DEADLINE])
			task[WCET_1188MHz] = int(task[WCET_1188MHz])
			task[WCET_918MHz] = int(task[WCET_918MHz])
			task[WCET_648MHz] = int(task[WCET_648MHz])
			task[WCET_384MHz] = int(task[WCET_384MHz])

	return (taskInfo, taskList)

if __name__ == "__main__":
	(taskInfo, taskList) = openFile(sys.argv[1])
	outFilePath = sys.argv[1].split('.')[0]
	output = ""
	if ("RM" in sys.argv and "EE" in sys.argv):
		output = RM_EE(taskInfo, taskList)
		outFilePath += "_RM_EE"
	elif ("RM" in sys.argv):
		output = RM(taskInfo, taskList)
		outFilePath += "_RM"
	elif ("EDF" in sys.argv and "EE" in sys.argv):
		output = EDF_EE(taskInfo, taskList)
		outFilePath += "_EDF_EE"
	elif ("EDF" in sys.argv):
		output = EDF(taskInfo, taskList)
		outFilePath += "_EDF"
	else:
		print("Please input valid command line parameters")
		exit()
	with open(outFilePath + ".out", 'w') as outFile:
		outFile.write(output)