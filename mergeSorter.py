# work plan:
# 1. implement tournament merging
# 		advantage being - other than potential modifications from the
#		winner having a new value, you get to retain all the
#		comparisons you've made to find that winner
#		
#		do this in a seperate class for cleanness, maybe move back afterwards for speed
#
#		version 1 - explicitly linked
#		
#		version 2 - binary heap style version, using a list
#			this is a limmited version of an indexed priority queue
#		
# 2. top down mergesort
#		use a stack of tasks, but opperate only on the leftmost
#		element of each member of the stack
#		
#		part of the setup for peeksort.
#
#		use function names to distinguish different styles, and maintain both
#
# 3. run detection
#		saving runs to some data structure
#
# 4. peeksort
# 5. k-way peeksort
# 5. powersort
# 6. experimental tools
#		timing, random run generation, comparison counting, memory
#		transfer counting


# https://stackoverflow.com/questions/5334531/using-javadoc-for-python-documentation



import math
import tournamentTree

class mergeSorter:
	def __init__(self, inputArray):
		self.inputLength = len(inputArray) 

		self.ping = inputArray
		self.pong = inputArray.copy()
		# current list is always from the *last* execution of the loop
		self.pingCurrent = True

	# * * * * * * * * * * * * * * * * * *
	# * * * * * SUPPORT METHODS * * * * *
	# * * * * * * * * * * * * * * * * * *

	def getCurrentList(self):
		if self.pingCurrent:
			return self.ping
		else:
			return self.pong

	def getWorkingOutList(self):
		if not self.pingCurrent:
			return self.ping
		else:
			return self.pong

	# * * * * * * * * * * * * * *
	# * * * * * MERGERS * * * * *
	# * * * * * * * * * * * * * *

	# merges two runs. runs must be adjacent to maintain stability, so
	# are indicated by start, middle and end start points are always
	# inclusive, and end points are always exclusive so it is legit to
	# use mid for both, without causing overlap
	def merge2(self, start, mid, end):
		# the left run and modified section of the working our list
		# start at start of the relevent section
		leftPos = start
		self.workingOutPos = start
		# the midpoint is defined as the start of the right hand run
		rightPos = mid

		currentList = self.getCurrentList()
		workingOutList = self.getWorkingOutList()

		# while you're still inside both runs
		while leftPos < mid and rightPos < end:
			# if the next LH element is smaller than the next RH
			# element
			if currentList[leftPos] < currentList[rightPos]:
				# use it
				workingOutList[self.workingOutPos] = currentList[leftPos]
				self.workingOutPos += 1
				leftPos += 1
			else:
				workingOutList[self.workingOutPos] = currentList[rightPos]
				self.workingOutPos += 1
				rightPos += 1

		# when one option is removed, fill whatever remains
		for i in range(mid - leftPos):			
			workingOutList[self.workingOutPos] = currentList[leftPos]
			self.workingOutPos += 1
			leftPos += 1

		for i in range(end - rightPos):
			workingOutList[self.workingOutPos] = currentList[rightPos]
			self.workingOutPos += 1
			rightPos += 1


	# merges k runs, where k is the number of lists contained within
	# the runs list.
	#
	# the runs list should contain [start, end] pairs, where the start
	# is inclusive and the end is exclusive.
	#
	# runs are assumed to be contiguous (necesary for stability), so
	# at input the  start of each run should be the end of the
	# previous run, though this will be modified as elements are moved
	# to output
	# 
	# uses a simple scan internally to find the minimum element - unnaceptably slow 
	def mergeK_old(self, runs):
		# overwritten portion of workingOutPos starts at the start of
		# the set of runs
		self.workingOutPos = runs[0][0]

		currentList = self.getCurrentList()
		workingOutList = self.getWorkingOutList()

		# while there are still runs
		while len(runs) > 1:
			# find the run with the smallest first index

			# initialise to the first run
			minRun = 0
			for i in range(len(runs) - 1):
				# if the first element is smaller, update it.
				if currentList[runs[i+1][0]] < currentList[runs[minRun][0]]:
					minRun = i + 1

			# move that element to the output
			workingOutList[self.workingOutPos] = currentList[runs[minRun][0]]
			self.workingOutPos += 1

			# increment position in this run
			runs[minRun][0] += 1

			# if the current and end pos of that run are now equal,
			# remove it from the list
			if runs[minRun][0] == runs[minRun][1]:
				runs.pop(minRun)

		# copy remaining run over - no need to pay the overheads of comparing 
		while runs[0][0] != runs[0][1]:
			workingOutList[self.workingOutPos] = currentList[runs[0][0]]
			runs[0][0] += 1
			self.workingOutPos += 1


	# merges k runs, where k is the number of lists contained within
	# the runs list.
	#
	# the runs list should contain [start, end] pairs, where the start
	# is inclusive and the end is exclusive.
	#
	# runs are assumed to be contiguous (necesary for stability), so
	# at input the  start of each run should be the end of the
	# previous run, though this will be modified as elements are moved
	# to output
	def mergeK(self, runs):
		# overwritten portion of workingOutPos starts at the start of
		# the set of runs
		self.workingOutPos = runs[0][0]

		currentList = self.getCurrentList()
		workingOutList = self.getWorkingOutList()

		# while there are still runs
		while len(runs) > 1:
			# find the run with the smallest first index

			# initialise to the first run
			minRun = 0
			for i in range(len(runs) - 1):
				# if the first element is smaller, update it.
				if currentList[runs[i+1][0]] < currentList[runs[minRun][0]]:
					minRun = i + 1

			# move that element to the output
			workingOutList[self.workingOutPos] = currentList[runs[minRun][0]]
			self.workingOutPos += 1

			# increment position in this run
			runs[minRun][0] += 1

			# if the current and end pos of that run are now equal,
			# remove it from the list
			if runs[minRun][0] == runs[minRun][1]:
				runs.pop(minRun)

		# copy remaining run over - no need to pay the overheads of comparing 
		while runs[0][0] != runs[0][1]:
			workingOutList[self.workingOutPos] = currentList[runs[0][0]]
			runs[0][0] += 1
			self.workingOutPos += 1



	# * * * * * * * * * * * * * *
	# * * * * * SORTERS * * * * *
	# * * * * * * * * * * * * * *

	# merge sort, merging two runs at a time
	def mergeSort2(self):
		runLength = 1

		while runLength <= self.inputLength:
			# for all runs
			for i in range(math.ceil(self.inputLength/(2*runLength))):
				# beginning of a run is assumed to be safe
				start = runLength*2*i

				# middle must be less than the end of the list or the second element has no contents
				mid    = runLength*(2*i+1)
				if mid > self.inputLength:
					break

				# end must be capped at the length of the list to prevent overruns
				end   = runLength*(2*i+2)
				if end > self.inputLength:
					end = self.inputLength

				self.merge2(start, mid, end)

			# swap between the ping list and pong list after all operations are complete
			self.pingCurrent = not self.pingCurrent

			runLength *= 2

		return self.getCurrentList()


	# merge sort, merging k runs at a time
	def mergeSortK(self, k):
		runLength = 1

		# while some merges remain
		while runLength <= self.inputLength:

			# for each block of k runs
			for blockNumber in range(math.ceil(self.inputLength/(k*runLength))):
				
				start = runLength*k*blockNumber
				
				# an array in the format [[start,end],[start,end]...]
				mergePlan = []

				# for each run in the block - fill the merge plan
				for runNumber in range(k):
					firstElement = runLength*k*blockNumber + runNumber*runLength
					
					# if the first element is over the end of the
					# array, this mergeplan is complete
					if firstElement >= self.inputLength:
						break
					
					lastElement = firstElement + runLength
					# if the last element overruns, truncate the run
					# to include whatever's left 
					if lastElement > self.inputLength:
						lastElement = self.inputLength

					mergePlan.append([firstElement,lastElement])

				#self.mergeK(mergePlan)

				ourTT = tournamentTree.tournamentTree(self.getCurrentList(), self.getWorkingOutList(), mergePlan)
				ourTT.simpleMerge()

			# swap between the ping list and pong list after all operations are complete
			self.pingCurrent = not self.pingCurrent

			runLength *= k


ourInput = [17,16,13,12,9,3,12,34,65,12,34,76,8,12,31,4]
#ourInput = [16,17,12,13,3,9,12,34,12,65,34,76,8,12,4,31]
ourMS = mergeSorter(ourInput)

print("before:")
print(ourMS.getCurrentList())

#ourMS.mergeSort2()
#ourMS.mergeK([[0,2],[2,4],[4,6]])

ourMS.mergeSortK(4)

print()
print("after:")
print(ourMS.getCurrentList())
#print(ourMS.getWorkingOutList())

