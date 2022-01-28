import math

class mergeSorter:
	def __init__(self, input):
		self.inputLength = len(input) 

		self.ping = input
		self.pong = input.copy()
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

	def sendToOutput(self, workingOutList, value):
		workingOutList[self.workingOutPos] = value
		self.workingOutPos += 1


	# * * * * * * * * * * * * * *
	# * * * * * MERGERS * * * * *
	# * * * * * * * * * * * * * *

	# merges two runs. runs must be adjacent to maintain stability, so are indicated by start, middle and end
	# start points are always inclusive, and end points are always exclusive so it is legit to use mid for both,
	# without causing overlap 
	def merge2(self, start, mid, end):
		# the left run and modified section of the working our list start at start of the relevent section
		leftPos = start
		self.workingOutPos = start
		# the midpoint is defined as the start of the right hand run
		rightPos = mid

		currentList = self.getCurrentList()
		workingOutList = self.getWorkingOutList()

		# while you're still inside both runs
		while leftPos < mid and rightPos < end:
			# if the next LH element is smaller than the next RH element
			if currentList[leftPos] < currentList[rightPos]:
				# use it
				self.sendToOutput(workingOutList, currentList[leftPos])
				leftPos += 1
			else:
				self.sendToOutput(workingOutList, currentList[rightPos])
				rightPos += 1

		# when one option is removed, fill whatever remains
		for i in range(mid - leftPos):			
			self.sendToOutput(workingOutList, currentList[leftPos])
			leftPos += 1

		for i in range(end - rightPos):
			self.sendToOutput(workingOutList, currentList[rightPos])
			rightPos += 1

	# * * * * * * * * * * * * * *
	# * * * * * SORTERS * * * * *
	# * * * * * * * * * * * * * *

	# merge sort, merging two runs at a time
	def mergeSort2(self):
		runLength = 1

		while runLength <= self.inputLength:
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


ourInput = [17,16,13,12,9,3,12,34,65,12,34,76,8,12,31,4]
ourMS = mergeSorter(ourInput)

print("before:")
print(ourMS.getCurrentList())

ourMS.mergeSort2()

print()
print("after:")
print(ourMS.getCurrentList())

